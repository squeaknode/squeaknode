import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import {
  Grid,
  Tabs,
  Tab,
  AppBar,
  Box,
} from '@material-ui/core';

// styles
import { makeStyles } from '@material-ui/core/styles';

// components
import Widget from '../../components/Widget';
import SentPayment from '../../components/SentPayment';

// data

import {
  getSentPaymentsRequest,
} from '../../squeakclient/requests';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

export default function SentPayments() {
  const classes = useStyles();
  const [value, setValue] = useState(0);
  const [sentPayments, setSentPayments] = useState([]);
  const history = useHistory();

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const loadSentPayments = () => {
    getSentPaymentsRequest((sentPaymentsReply) => {
      setSentPayments(sentPaymentsReply.getSentPaymentsList());
    });
  };

  useEffect(() => {
    loadSentPayments();
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
      </Grid>
    );
  }

  return (
    <>
      {GridContent()}
    < />
  );
}
