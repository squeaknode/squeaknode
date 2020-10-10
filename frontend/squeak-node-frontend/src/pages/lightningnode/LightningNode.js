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

import {
  GetInfoRequest,
  WalletBalanceRequest,
  ListPeersRequest,
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
  const [peers, setPeers] = useState([]);

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

  const handleClickDisconnectPeer = () => {
    disconnectPeer(pubkey);
  };

  const isConnected = () => {
    var hasPeerConnection = false;
    var i;
    for (i = 0; i < peers.length; i++) {
      console.log("pubkey");
      console.log(pubkey);
      console.log("peers[i].getPubKey()");
      console.log(peers[i].getPubKey());
      if (pubkey == peers[i].getPubKey()) {
        hasPeerConnection = true;
      }
    }
    console.log(hasPeerConnection);
    return hasPeerConnection;
  };

  const listPeers = () => {
        console.log("called listPeers");

        var listPeersRequest = new ListPeersRequest()
        console.log(listPeersRequest);

        client.lndListPeers(listPeersRequest, {}, (err, response) => {
          console.log(response);
          console.log("response.getPeersList()");
          console.log(response.getPeersList());
          setPeers(response.getPeersList());
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

       </Widget>
      </Grid>
    )
  }

  function IsConnected() {
    return (
      isConnected().toString()
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
          <Tab label="Pending Channels" {...a11yProps(2)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {PubkeyContent()}
      </TabPanel>
      <TabPanel value={value} index={1}>
        fooo
      </TabPanel>
      <TabPanel value={value} index={2}>
        barrr
      </TabPanel>
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
    </>
  );
}
