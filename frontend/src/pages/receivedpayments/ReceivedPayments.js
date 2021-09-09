import React, { useState, useEffect, useCallback } from 'react';
import {
  Grid,
  Button,
  Tabs,
  Tab,
  AppBar,
  Box,
  CircularProgress,
} from '@material-ui/core';

// styles
import { makeStyles } from '@material-ui/core/styles';

// components
import ReplayIcon from '@material-ui/icons/Replay';
import Widget from '../../components/Widget';
import ReceivedPayment from '../../components/ReceivedPayment';

// data

import {
  getReceivedPaymentsRequest,
  reprocessReceivedPaymentsRequest,
} from '../../squeakclient/requests';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

const RECEIVED_PAYMENTS_PER_PAGE = 10;

export default function ReceivedPayments() {
  const classes = useStyles();
  const [value, setValue] = useState(0);
  const [receivedPayments, setReceivedPayments] = useState([]);
  const [waitingForReceivedPayments, setWaitingForReceivedPayments] = React.useState(false);

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const loadReceivedPayments = useCallback((limit, lastReceivedPayment) => {
    setWaitingForReceivedPayments(true);
    getReceivedPaymentsRequest(limit, lastReceivedPayment, handleLoadedReceivedPayments);
  },
  []);

  const handleLoadedReceivedPayments = (reply) => {
    const loadedReceivedPayments = reply.getReceivedPaymentsList();
    setWaitingForReceivedPayments(false);
    setReceivedPayments((prevReceivedPayments) => {
      if (!prevReceivedPayments) {
        return loadedReceivedPayments;
      }
      return prevReceivedPayments.concat(loadedReceivedPayments);
    });
  };

  const reprocessReceivedPayments = () => {
    reprocessReceivedPaymentsRequest((response) => {
      console.log('Successfully called reprocess received payments.');
    });
  };

  useEffect(() => {
    loadReceivedPayments(RECEIVED_PAYMENTS_PER_PAGE, null);
  }, [loadReceivedPayments]);

  function TabPanel(props) {
    const {
      children, value, index, ...other
    } = props;

    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <div>{children}</div>
        )}
      </div>
    );
  }

  function PaymentsTabs() {
    return (
      <>
        <AppBar position="static" color="default">
          <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
            <Tab label="Received Payments" {...a11yProps(0)} />
          </Tabs>
        </AppBar>
        <TabPanel value={value} index={0}>
          {ReceivedPaymentsContent()}
        </TabPanel>
      </>
    );
  }

  function ReprocessReceivedPaymentsButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                reprocessReceivedPayments();
              }}
            >
              Reprocess Received Payments
            </Button>
            This only needs to be used if the LND node is replaced.
          </div>
        </Grid>
      </>
    );
  }

  function ReceivedPaymentsContent() {
    return (
      <>
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Widget disableWidgetMenu>

              {ReprocessReceivedPaymentsButton()}

              <div>
                {receivedPayments.map((receivedPayment) => (
                  <Box
                    p={1}
                    key={receivedPayment.getReceivedPaymentId()}
                  >
                    <ReceivedPayment
                      receivedPayment={receivedPayment}
                    />
                  </Box>
                ))}
              </div>
            </Widget>
          </Grid>
        </Grid>
      </>
    );
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          {PaymentsTabs()}
        </Grid>
        <Grid item xs={12} sm={3} />
        {ViewMoreReceivedPaymentsButton()}
      </Grid>
    );
  }

  function ViewMoreReceivedPaymentsButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.wrapper}>
            {!waitingForReceivedPayments
            && (
            <Button
              variant="contained"
              color="primary"
              disabled={waitingForReceivedPayments}
              onClick={() => {
                const latestReceivedPayment = receivedPayments.slice(-1).pop();
                loadReceivedPayments(RECEIVED_PAYMENTS_PER_PAGE, latestReceivedPayment);
              }}
            >
              <ReplayIcon />
              View more
            </Button>
            )}
            {waitingForReceivedPayments && <CircularProgress size={48} className={classes.buttonProgress} />}
          </div>
        </Grid>
      </>
    );
  }

  return (
    <>
      {GridContent()}
    < />
  );
}
