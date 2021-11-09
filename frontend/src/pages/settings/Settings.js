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
  getDefaultSellPriceRequest,
} from '../../squeakclient/requests';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));


export default function Settings() {
  const classes = useStyles();
  const [value, setValue] = useState(0);
  const [defaultSellPriceMsat, setDefaultSellPriceMsat] = useState([]);
  const [waitingForDefaultSellPriceMsat, setWaitingForDefaultSellPriceMsat] = useState(false);

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const loadDefaultPriceMsat = useCallback(() => {
    setWaitingForDefaultSellPriceMsat(true);
    console.log("getting priceMsat...");
    getDefaultSellPriceRequest((resp => {
      setWaitingForDefaultSellPriceMsat(false);
      console.log("setting priceMsat: " + resp);
      setDefaultSellPriceMsat(resp);
    }));
  },
  []);

  useEffect(() => {
    loadDefaultPriceMsat();
  }, [loadDefaultPriceMsat]);

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
            <Tab label="Settings" {...a11yProps(0)} />
          </Tabs>
        </AppBar>
        <TabPanel value={value} index={0}>
          Settings content here
          {defaultSellPriceMsat}
        </TabPanel>
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
