import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  AppBar,
  Tabs,
  Tab,
} from "@material-ui/core";
import { useTheme } from "@material-ui/styles";
import {
  ResponsiveContainer,
  ComposedChart,
  AreaChart,
  LineChart,
  Line,
  Area,
  PieChart,
  Pie,
  Cell,
  YAxis,
  XAxis,
} from "recharts";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import { Typography } from "../../components/Wrappers";

import { GetInfoRequest, WalletBalanceRequest } from "../../proto/lnd_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function LightningPage() {
  var classes = useStyles();
  var theme = useTheme();

  const [lndInfo, setLndInfo] = useState(null);
  const [walletBalance, setWalletBalance] = useState(null);
  const [value, setValue] = useState(0);

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const getLndInfo = () => {
        console.log("called getLndInfo");

        var getInfoRequest = new GetInfoRequest()
        console.log(getInfoRequest);

        client.lndGetInfo(getInfoRequest, {}, (err, response) => {
          console.log(response);
          setLndInfo(response);
        });
  };
  const getWalletBalance = () => {
        console.log("called getWalletBalance");

        var walletBalanceRequest = new WalletBalanceRequest()
        console.log(walletBalanceRequest);

        client.lndWalletBalance(walletBalanceRequest, {}, (err, response) => {
          console.log(response);
          setWalletBalance(response);
        });
  };

  useEffect(()=>{
    getLndInfo()
  },[]);
  useEffect(()=>{
    getWalletBalance()
  },[]);

  function NoInfoContent() {
    return (
      <div>
        Unable to fetch lightning info.
      </div>
    )
  }

  function InfoContentOld() {
    return (
      <div>
        <p>identity_pubkey: {lndInfo.getIdentityPubkey()}</p>
        <p>alias: {lndInfo.getAlias()}</p>
        <p>num_pending_channels: {lndInfo.getNumPendingChannels()}</p>
        <p>num_active_channels: {lndInfo.getNumActiveChannels()}</p>
        <p>num_inactive_channels: {lndInfo.getNumInactiveChannels()}</p>
        <p>num_peers: {lndInfo.getNumPeers()}</p>
        <p>block_height: {lndInfo.getBlockHeight()}</p>
        <p>block_hash: {lndInfo.getBlockHash()}</p>
        <p>synced_to_chain: {lndInfo.getSyncedToChain().toString()}</p>
        <p>synced_to_graph: {lndInfo.getSyncedToGraph().toString()}</p>
      </div>
    )
  }

  function InfoContent() {
    return (
      <>
        <Grid container spacing={4}>
          {PubkeyGridItem()}
        </Grid>
        <Grid container spacing={4}>
          {StatusGridItem()}
          {ChannelsGridItem()}
          {BalanceGridItem()}
        </Grid>
      </>
    )
  }

  function PubkeyGridItem() {
    return (
      <Grid item xs={12}>
        <Widget
          title="Node info"
          disableWidgetMenu
          upperTitle
          bodyClass={classes.fullHeightBody}
          className={classes.card}
        >
          <div className={classes.visitsNumberContainer}>
          <Typography color="text" colorBrightness="secondary">
            pubkey
          </Typography>
            <Typography size="md" weight="medium">
              {lndInfo.getIdentityPubkey()}
            </Typography>
          </div>
        </Widget>
      </Grid>
    )
  }

  function StatusGridItem() {
    return (
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget
            title="Node status"
            disableWidgetMenu
            upperTitle
            bodyClass={classes.fullHeightBody}
            className={classes.card}
          >
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  synced to chain
                </Typography>
                <Typography size="md">{lndInfo.getSyncedToChain().toString()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  synced to graph
                </Typography>
                <Typography size="md">{lndInfo.getSyncedToGraph().toString()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  block height
                </Typography>
                <Typography size="md">{lndInfo.getBlockHeight()}</Typography>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
    )
  }

  function ChannelsGridItem() {
    return (
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget
            title="Channels"
            disableWidgetMenu
            upperTitle
            bodyClass={classes.fullHeightBody}
            className={classes.card}
          >
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  num pending channels
                </Typography>
                <Typography size="md">{lndInfo.getNumPendingChannels()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  num active channels
                </Typography>
                <Typography size="md">{lndInfo.getNumActiveChannels()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  num inactive channels
                </Typography>
                <Typography size="md">{lndInfo.getNumInactiveChannels()}</Typography>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
    )
  }

  function BalanceGridItem() {
    return (
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget
            title="Balance"
            disableWidgetMenu
            upperTitle
            bodyClass={classes.fullHeightBody}
            className={classes.card}
          >
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  total balance
                </Typography>
                <Typography size="md">{walletBalance.getTotalBalance()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  confirmed balance
                </Typography>
                <Typography size="md">{walletBalance.getConfirmedBalance()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  unconfirmed balance
                </Typography>
                <Typography size="md">{walletBalance.getUnconfirmedBalance()}</Typography>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
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

  function LightningTabs() {
    return (
      <>
      <AppBar position="static" color="default">
        <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
          <Tab label="Balance" {...a11yProps(0)} />
          <Tab label="Node Info" {...a11yProps(1)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {(lndInfo && walletBalance)
          ? InfoContent()
          : NoInfoContent()
        }
      </TabPanel>
      <TabPanel value={value} index={1}>
        foooo
      </TabPanel>
      </>
    )
  }

  return (
    <>
      <PageTitle title="Lightning" />
      {LightningTabs()}
    </>
  );
}
