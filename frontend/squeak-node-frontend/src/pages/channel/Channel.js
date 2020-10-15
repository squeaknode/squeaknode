import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  AppBar,
  Tabs,
  Tab,
  Box,
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
import OpenChannelDialog from "../../components/OpenChannelDialog";
import ChannelItem from "../../components/ChannelItem";

import {
  GetInfoRequest,
  WalletBalanceRequest,
  ListPeersRequest,
  ListChannelsRequest,
  LightningAddress,
  ConnectPeerRequest,
  DisconnectPeerRequest,
} from "../../proto/lnd_pb"
import { client } from "../../squeakclient/squeakclient"


export default function LightningNodePage() {
  var classes = useStyles();
  var theme = useTheme();

  const history = useHistory();
  const { txId, outputIndex } = useParams();
  const [value, setValue] = useState(0);
  const [peers, setPeers] = useState(null);
  const [channels, setChannels] = useState(null);
  const [openChannelDialogOpen, setOpenChannelDialogOpen] = useState(false);

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const listPeers = () => {
        console.log("called listPeers");

        var listPeersRequest = new ListPeersRequest()
        console.log(listPeersRequest);

        client.lndListPeers(listPeersRequest, {}, (err, response) => {
          if (err) {
            console.log(err.message);
            alert('Error getting peers: ' + err.message);
            return;
          }
          console.log(response);
          console.log("response.getPeersList()");
          console.log(response.getPeersList());
          setPeers(response.getPeersList());
        });
  };
  const listChannels = () => {
        console.log("called listChannels");

        var listChannelsRequest = new ListChannelsRequest()
        console.log(listChannelsRequest);

        client.lndListChannels(listChannelsRequest, {}, (err, response) => {
          if (err) {
            console.log(err.message);
            alert('Error getting channels: ' + err.message);
            return;
          }
          console.log(response);
          console.log("response.getChannelsList()");
          console.log(response.getChannelsList());
          setChannels(response.getChannelsList());
        });
  };

  const connectPeer = (pubkey, host) => {
    console.log("called connectPeer");

    var connectPeerRequest = new ConnectPeerRequest()
    var address = new LightningAddress();
    address.setPubkey(pubkey);
    address.setHost(host);
    connectPeerRequest.setAddr(address);
    console.log(connectPeerRequest);

    client.lndConnectPeer(connectPeerRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error connecting peer: ' + err.message);
        return;
      }

      console.log(response);
      reloadRoute();
    });
  };

  const disconnectPeer = (pubkey) => {
    console.log("called disconnectPeer");

    var disconnectPeerRequest = new DisconnectPeerRequest()
    disconnectPeerRequest.setPubKey(pubkey);
    console.log(disconnectPeerRequest);

    client.lndDisconnectPeer(disconnectPeerRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error disconnecting peer: ' + err.message);
        return;
      }

      console.log(response);
      reloadRoute();
    });
  };

  const reloadRoute = () => {
    history.go(0);
  };

  useEffect(()=>{
    listPeers()
  },[]);
  useEffect(()=>{
    listChannels()
  },[]);

  function ChannelInfoGridItem() {
    return (
      <Grid item xs={12}>
      <Widget disableWidgetMenu>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="center"
      >
        <Grid item>
          <Typography color="text" colorBrightness="secondary">
            channel point
          </Typography>
          <Typography size="md">{txId + ":" + outputIndex}</Typography>
        </Grid>
      </Grid>

      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="center"
      >
        <Grid item>
          <Typography color="text" colorBrightness="secondary">
            channel status
          </Typography>
          <Typography size="md">{"channel status here"}</Typography>
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

  function ChannelTabs() {
    return (
      <>
      <AppBar position="static" color="default">
        <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
          <Tab label="Channel Info" {...a11yProps(0)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {ChannelInfoGridItem()}
      </TabPanel>
      </>
    )
  }

  return (
    <>
      <PageTitle title={'Channel'} />
      {ChannelTabs()}
    </>
  );
}
