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

  useEffect(() => {
    loadSentPayments()
  }, []);
  useEffect(() => {
    loadReceivedPayments()
  }, []);


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
    console.log("receivedPayments:");
    console.log(receivedPayments);
    return (
      <>
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Widget disableWidgetMenu>
          <div>
            Received payments here.
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
    {PaymentsTabs()}
   < />);
}
