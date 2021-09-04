import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import {
  Grid,
  Button,
  Typography,
} from '@material-ui/core';
import FormLabel from '@material-ui/core/FormLabel';

// styles
import { makeStyles } from '@material-ui/core/styles';

// components
import Widget from '../../components/Widget';

// data

import {
  getPaymentSummaryRequest,
} from '../../squeakclient/requests';
import {
  goToSentPaymentsPage,
  goToReceivedPaymentsPage,
} from '../../navigation/navigation';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

export default function Payments() {
  const classes = useStyles();
  const [paymentSummary, setPaymentSummary] = useState(null);
  const history = useHistory();

  const loadPaymentSummary = () => {
    getPaymentSummaryRequest((paymentsSummaryReply) => {
      setPaymentSummary(paymentsSummaryReply.getPaymentSummary());
    });
  };

  useEffect(() => {
    loadPaymentSummary();
  }, []);

  function PaymentSummaryContent() {
    return (
      <>
        {SentPaymentContent()}
        {ReceivedPaymentContent()}
      </>
    );
  }

  function SentPaymentContent() {
    return (
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Widget disableWidgetMenu>
            <Grid item>
              <FormLabel>
                Total amount spent
              </FormLabel>
              <Typography size="md">
                {paymentSummary.getAmountSpentMsat() / 1000}
                {' '}
                sats
              </Typography>
            </Grid>
            <Grid item>
              <FormLabel>
                Number of sent payments
              </FormLabel>
              <Typography size="md">
                {paymentSummary.getNumSentPayments()}
              </Typography>
              {ViewSentPaymentsButton()}
            </Grid>
          </Widget>
        </Grid>
      </Grid>
    );
  }

  function ReceivedPaymentContent() {
    return (
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Widget disableWidgetMenu>
            <Grid item>
              <FormLabel>
                Total amount earned
              </FormLabel>
              <Typography size="md">
                {paymentSummary.getAmountEarnedMsat() / 1000}
                {' '}
                sats
              </Typography>
            </Grid>
            <Grid item>
              <FormLabel>
                Number of received payments
              </FormLabel>
              <Typography size="md">
                {paymentSummary.getNumReceivedPayments()}
              </Typography>
              {ViewReceivedPaymentsButton()}
            </Grid>
          </Widget>
        </Grid>
      </Grid>
    );
  }

  function ViewSentPaymentsButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                goToSentPaymentsPage(history);
              }}
            >
              View Sent Payments
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function ViewReceivedPaymentsButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                goToReceivedPaymentsPage(history);
              }}
            >
              View Received Payments
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          {paymentSummary && PaymentSummaryContent()}
        </Grid>
        <Grid item xs={12} sm={3} />
      </Grid>
    );
  }

  return (
    <>
      {GridContent()}
    </>
  );
}
