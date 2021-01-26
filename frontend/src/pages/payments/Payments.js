import React, {useState, useEffect} from 'react';
import {useHistory} from "react-router-dom";
import {
    Grid,
    Button,
    Paper,
    Tabs,
    Tab,
    AppBar,
    Box,
    Typography,
  } from "@material-ui/core";
import MUIDataTable from "mui-datatables";
import FormLabel from "@material-ui/core/FormLabel";

// styles
import {makeStyles} from '@material-ui/core/styles';

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import Table from "../dashboard/components/Table/Table";
import SentPayment from "../../components/SentPayment";
import ReceivedPayment from "../../components/ReceivedPayment";


// data
import mock from "../dashboard/mock";

import {
  getSentPaymentsRequest,
  getReceivedPaymentsRequest,
  getPaymentSummaryRequest
} from "../../squeakclient/requests"

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1)
    }
  }
}));

export default function Payments() {
  const classes = useStyles();
  const [value, setValue] = useState(0);
  const [paymentSummary, setPaymentSummary] = useState(null);
  const [sentPayments, setSentPayments] = useState([]);
  const [receivedPayments, setReceivedPayments] = useState([]);
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

  const loadReceivedPayments = () => {
    getReceivedPaymentsRequest((receivedPaymentsReply) => {
      setReceivedPayments(receivedPaymentsReply.getReceivedPaymentsList());
    });
  };

  const loadPaymentSummary = () => {
    getPaymentSummaryRequest((paymentsSummaryReply) => {
      setPaymentSummary(paymentsSummaryReply.getPaymentSummary());
    });
  };

  useEffect(() => {
    loadSentPayments();
  }, []);
  useEffect(() => {
    loadReceivedPayments();
  }, []);
  useEffect(() => {
    loadPaymentSummary();
  }, []);

  function PaymentSummaryContent() {
    return (
      <>
      <Grid container spacing={4}>
      <Grid item xs={6}>
        <Widget disableWidgetMenu>
        <Grid item>
          <FormLabel>
            Total amount spent
          </FormLabel>
          <Typography size="md">
            {paymentSummary.getAmountSpentMsat() / 1000} sats
          </Typography>
        </Grid>
        <Grid item>
          <FormLabel>
            Number of sent payments
          </FormLabel>
          <Typography size="md">
            {paymentSummary.getNumSentPayments()}
          </Typography>
        </Grid>
        </Widget>
      </Grid>
        <Grid item xs={6}>
          <Widget disableWidgetMenu>
          <Grid item>
            <FormLabel>
              Total amount earned
            </FormLabel>
            <Typography size="md">
              {paymentSummary.getAmountEarnedMsat() / 1000} sats
            </Typography>
          </Grid>
          <Grid item>
            <FormLabel>
              Number of received payments
            </FormLabel>
            <Typography size="md">
              {paymentSummary.getNumReceivedPayments()}
            </Typography>
          </Grid>
          </Widget>
        </Grid>
      </Grid>
      </>
    )
  }


  function TabPanel(props) {
    const { children, value, index, ...other } = props;

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
          <Tab label="Received Payments" {...a11yProps(1)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {SentPaymentsContent()}
      </TabPanel>
      <TabPanel value={value} index={1}>
        {ReceivedPaymentsContent()}
      </TabPanel>
      </>
    )
  }

  function SentPaymentsContent() {
    return (
      <>
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Widget disableWidgetMenu>
          <div>
          {sentPayments.map(sentPayment =>
            <Box
              p={1}
              key={sentPayment.getSentPaymentId()}
              >
            <SentPayment
              sentPayment={sentPayment}>
            </SentPayment>
            </Box>
          )}
          </div>
          </Widget>
        </Grid>
      </Grid>
      </>
    )
  }

  function ReceivedPaymentsContent() {
    return (
      <>
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Widget disableWidgetMenu>
          <div>
          {receivedPayments.map(receivedPayment =>
            <Box
              p={1}
              key={receivedPayment.getReceivedPaymentId()}
              >
            <ReceivedPayment
              receivedPayment={receivedPayment}>
            </ReceivedPayment>
            </Box>
          )}
          </div>
          </Widget>
        </Grid>
      </Grid>
      </>
    )
  }

  return (
    <>
     < PageTitle title = "Payments" />
     {paymentSummary && PaymentSummaryContent()}
     {PaymentsTabs()}
   < />);
}
