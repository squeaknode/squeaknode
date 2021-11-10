import React, { useState, useEffect, useCallback } from 'react';
import {
  Grid,
  Button,
  Tabs,
  Tab,
  AppBar,
  Box,
  CircularProgress,
  FormLabel,
  Typography,
} from '@material-ui/core';

// styles
import { makeStyles } from '@material-ui/core/styles';

// components
import ReplayIcon from '@material-ui/icons/Replay';
import Widget from '../../components/Widget';
import ReceivedPayment from '../../components/ReceivedPayment';
import SetSellPriceDialog from '../../components/SetSellPriceDialog';


import {
  getSellPriceRequest,
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
  const [sellPriceMsat, setSellPriceMsat] = useState(null);
  const [waitingForSellPriceMsat, setWaitingForSellPriceMsat] = useState(false);
  const [setSellPriceDialogOpen, setSetSellPriceDialogOpen] = useState(false);


  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleCloseSetSellPriceDialog = () => {
    setSetSellPriceDialogOpen(false);
  };

  const handleClickSetSellPriceDialog = () => {
    setSetSellPriceDialogOpen(true);
  };


  const loadSellPrice = useCallback(() => {
    setWaitingForSellPriceMsat(true);
    getSellPriceRequest((resp => {
      setWaitingForSellPriceMsat(false);
      console.log(resp);
      setSellPriceMsat(resp);
    }));
  },
  []);

  useEffect(() => {
    loadSellPrice();
  }, [loadSellPrice]);

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

  function SentPaymentContent() {
    const usingDefault = !sellPriceMsat.getPriceMsatIsSet();
    const priceSats = sellPriceMsat.getPriceMsat() / 1000;
    const defaultPriceSats = sellPriceMsat.getDefaultPriceMsat() / 1000;
    console.log('sell price' + priceSats);
    console.log('default sell price' + defaultPriceSats);
    console.log('use default' + usingDefault);
    return (
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Widget disableWidgetMenu>
            <Grid item>
              <FormLabel>
                Sell price
              </FormLabel>
              <Typography size="md">
                {usingDefault
                  ? defaultPriceSats
                  : priceSats}
                {' sats'}
                {usingDefault && ' (using default)'}
              </Typography>
              {SetSellPriceButtonContent()}
            </Grid>
          </Widget>
        </Grid>
      </Grid>
    );
  }

  function SettingsTabs() {
    return (
      <>
        <AppBar position="static" color="default">
          <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
            <Tab label="Settings" {...a11yProps(0)} />
          </Tabs>
        </AppBar>
        <TabPanel value={value} index={0}>
          {sellPriceMsat && SentPaymentContent()}
        </TabPanel>
      </>
    );
  }


  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          {SettingsTabs()}
        </Grid>
        <Grid item xs={12} sm={3} />
      </Grid>
    );
  }

  function SetSellPriceDialogContent() {
    return (
      <>
        <SetSellPriceDialog
          open={setSellPriceDialogOpen}
          handleClose={handleCloseSetSellPriceDialog}
          reloadSellPriceFn={loadSellPrice}
        />
      </>
    );
  }

  function SetSellPriceButtonContent() {
    return (
      <>
        <Box p={1}>
          <Button
            variant="contained"
            onClick={handleClickSetSellPriceDialog}
          >
            Set Sell Price
          </Button>
        </Box>
      </>
    );
  }

  return (
    <>
      {!waitingForSellPriceMsat && GridContent()}
      {SetSellPriceDialogContent()}
    < />
  );
}