import React, { useState, useEffect, useCallback } from 'react';
import {
  Grid,
  Tabs,
  Tab,
  AppBar,
  Box,
  Button,
  CircularProgress,
} from '@material-ui/core';

import ReplayIcon from '@material-ui/icons/Replay';

// components
import Widget from '../../components/Widget';
import SentPayment from '../../components/SentPayment';

// styles
import useStyles from './styles';

// data

import {
  getSentPaymentsRequest,
} from '../../squeakclient/requests';

const SENT_PAYMENTS_PER_PAGE = 10;


export default function SentPayments() {
  const classes = useStyles();
  const [value, setValue] = useState(0);
  const [sentPayments, setSentPayments] = useState([]);
  const [waitingForSentPayments, setWaitingForSentPayments] = React.useState(false);


  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  // const loadSentPayments = () => {
  //   getSentPaymentsRequest((sentPaymentsReply) => {
  //     setSentPayments(sentPaymentsReply.getSentPaymentsList());
  //   });
  // };
  const loadSentPayments = useCallback((limit, lastSentPayment) => {
    setWaitingForSentPayments(true);
    getSentPaymentsRequest(limit, lastSentPayment, handleLoadedSentPayments);
  },
  []);

  const handleLoadedSentPayments = (reply) => {
    const loadedSentPayments = reply.getSentPaymentsList();
    setWaitingForSentPayments(false);
    setSentPayments((prevSentPayments) => {
      if (!prevSentPayments) {
        return loadedSentPayments;
      }
      return prevSentPayments.concat(loadedSentPayments);
    });
  };

  useEffect(() => {
    loadSentPayments(SENT_PAYMENTS_PER_PAGE, null);
  }, []);

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
            <Tab label="Sent Payments" {...a11yProps(0)} />
          </Tabs>
        </AppBar>
        <TabPanel value={value} index={0}>
          {SentPaymentsContent()}
        </TabPanel>
      </>
    );
  }

  function SentPaymentsContent() {
    return (
      <>
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Widget disableWidgetMenu>
              <div>
                {sentPayments.map((sentPayment) => (
                  <Box
                    p={1}
                    key={sentPayment.getSentPaymentId()}
                  >
                    <SentPayment
                      sentPayment={sentPayment}
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
        {ViewMoreSentPaymentsButton()}
      </Grid>
    );
  }

  function ViewMoreSentPaymentsButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.wrapper}>
            {!waitingForSentPayments
            && (
            <Button
              variant="contained"
              color="primary"
              disabled={waitingForSentPayments}
              onClick={() => {
                const latestSentPayment = sentPayments.slice(-1).pop();
                loadSentPayments(SENT_PAYMENTS_PER_PAGE, latestSentPayment);
              }}
            >
              <ReplayIcon />
              View more squeaks
            </Button>
            )}
            {waitingForSentPayments && <CircularProgress size={48} className={classes.buttonProgress} />}
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
