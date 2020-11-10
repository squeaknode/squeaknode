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

// data
import mock from "../dashboard/mock";


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
            Show sent payments here.
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
            Show sent payments here.
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
