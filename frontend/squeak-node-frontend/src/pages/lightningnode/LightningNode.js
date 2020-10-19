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
import PendingOpenChannelItem from "../../components/PendingOpenChannelItem";

import {
  GetInfoRequest,
  WalletBalanceRequest,
  ListPeersRequest,
  ListChannelsRequest,
  PendingChannelsRequest,
  LightningAddress,
  ConnectPeerRequest,
  DisconnectPeerRequest,
} from "../../proto/lnd_pb"
import { client } from "../../squeakclient/squeakclient"


export default function LightningNodePage() {
  var classes = useStyles();
  var theme = useTheme();

  const history = useHistory();
  const { pubkey, host, port } = useParams();
  const [value, setValue] = useState(0);
  const [peers, setPeers] = useState(null);
  const [channels, setChannels] = useState(null);
  const [pendingChannels, setPendingChannels] = useState(null);
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

  const handleClickConnectPeer = () => {
    var lightningHost = host + ":" + port;
    connectPeer(pubkey, lightningHost);
  };

  const handleClickOpenChannel = () => {
    console.log("Handle click open channel.");
    setOpenChannelDialogOpen(true);
  };

  const handleCloseOpenChannelDialog = () => {
    setOpenChannelDialogOpen(false);
  };

  const handleClickDisconnectPeer = () => {
    disconnectPeer(pubkey);
  };

  const isConnected = () => {
    if (peers == null) {
      return false;
    }
    var i;
    for (i = 0; i < peers.length; i++) {
      if (pubkey == peers[i].getPubKey()) {
        return true;
      }
    }
    return false;
  };

  const hasChannelToPeer = () => {
    if (channels == null) {
      return false;
    }
    var i;
    for (i = 0; i < channels.length; i++) {
      if (pubkey == channels[i].getRemotePubkey()) {
        return true;
      }
    }
    return false;
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
  const getPendingChannels = () => {
        console.log("called pendingChannels");

        var pendingChannelsRequest = new PendingChannelsRequest()
        console.log(pendingChannelsRequest);

        client.lndPendingChannels(pendingChannelsRequest, {}, (err, response) => {
          if (err) {
            console.log(err.message);
            alert('Error getting pending channels: ' + err.message);
            return;
          }
          console.log(response);
          setPendingChannels(response);
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
  useEffect(()=>{
    getPendingChannels()
  },[]);

  function ConnectPeerButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickConnectPeer();
            }}>Connect Peer
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function DisconnectPeerButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickDisconnectPeer();
            }}>Disconnect Peer
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function OpenChannelButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickOpenChannel();
            }}>Open Channel
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function NodeInfoGridItem() {
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
            pubkey
          </Typography>
          <Typography size="md">{pubkey}</Typography>
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
            host
          </Typography>
          <Typography size="md">{host}</Typography>
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
            port
          </Typography>
          <Typography size="md">{port}</Typography>
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
            connected
          </Typography>
          <Typography size="md">
          {IsConnected()}
          </Typography>
          {isConnected()
            ? DisconnectPeerButton()
            : ConnectPeerButton()
          }
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
            channel to peer
          </Typography>
          <Typography size="md">
          {HasChannelToPeer()}
          </Typography>
          {hasChannelToPeer()
            ? ""
            : OpenChannelButton()
          }
        </Grid>
      </Grid>

       </Widget>
      </Grid>
    )
  }

  function ChannelsGridItem() {
    var nodeChannels = channels.filter(channel => channel.getRemotePubkey() == pubkey);
    var nodePendingOpenChannels = pendingChannels.getPendingOpenChannelsList().filter(pendingOpenChannel => pendingOpenChannel.getChannel().getRemoteNodePub() == pubkey);
    return (
      <Grid item xs={12}>
      <Widget disableWidgetMenu>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="center"
      >
        <Grid item xs={12}>
        {nodePendingOpenChannels.map(pendingOpenChannel =>
          <Box
            p={1}
            key={pendingOpenChannel.getChannel().getChannelPoint()}
            >
          <PendingOpenChannelItem
            key={pendingOpenChannel.getChannel().getChannelPoint()}
            pendingOpenChannel={pendingOpenChannel}>
          </PendingOpenChannelItem>
          </Box>
        )}
        {nodeChannels.map(channel =>
          <Box
            p={1}
            key={channel.getChannelPoint()}
            >
          <ChannelItem
            key={channel.getChannelPoint()}
            channel={channel}>
          </ChannelItem>
          </Box>
        )}
        </Grid>
      </Grid>
      </Widget>
      </Grid>
    )
  }

  function IsConnected() {
    return (
      isConnected().toString()
    )
  }

  function HasChannelToPeer() {
    return (
      hasChannelToPeer().toString()
    )
  }

  function NoPubkeyContent() {
    return (
      <div>
        No pubkey.
      </div>
    )
  }

  function PubkeyContent() {
    return (
      <>
        <Grid container spacing={4}>
          {NodeInfoGridItem()}
        </Grid>
      </>
    )
  }

  function ChannelsContent() {
    if (channels == null || pendingChannels == null) {
      return (
        <>
          <Grid container spacing={4}>
          <Grid item xs={12}>
          <Widget disableWidgetMenu>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="center"
          >
            <Grid item xs={12}>
              Unable to load channels
            </Grid>
          </Grid>
          </Widget>
          </Grid>
          </Grid>
        </>
      )
    }

    return (
      <>
        <Grid container spacing={4}>
          {ChannelsGridItem()}
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

  function LightningNodeTabs() {
    return (
      <>
      <AppBar position="static" color="default">
        <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
          <Tab label="Node Info" {...a11yProps(0)} />
          <Tab label="Channels" {...a11yProps(1)} />
          <Tab label="Routes" {...a11yProps(2)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {PubkeyContent()}
      </TabPanel>
      <TabPanel value={value} index={1}>
        {ChannelsContent()}
      </TabPanel>
      <TabPanel value={value} index={2}>
        Show routes here
      </TabPanel>
      </>
    )
  }

  function OpenChannelDialogContent() {
    return (
      <>
        <OpenChannelDialog
          open={openChannelDialogOpen}
          pubkey={pubkey}
          handleClose={handleCloseOpenChannelDialog}
          ></OpenChannelDialog>
      </>
    )
  }

  return (
    <>
      <PageTitle title={'Lightning Node: ' + pubkey} />
      {pubkey
        ? LightningNodeTabs()
        : NoPubkeyContent()
      }
      {OpenChannelDialogContent()}
    </>
  );
}
