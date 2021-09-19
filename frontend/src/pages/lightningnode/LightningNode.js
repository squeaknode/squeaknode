import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import {
  Grid,
  Button,
  AppBar,
  Tabs,
  Tab,
  Box,
  CircularProgress,
} from '@material-ui/core';

// styles
import useStyles from './styles';

// components
import Widget from '../../components/Widget';
import { Typography } from '../../components/Wrappers';
import OpenChannelDialog from '../../components/OpenChannelDialog';
import ChannelItem from '../../components/ChannelItem';
import PendingOpenChannelItem from '../../components/PendingOpenChannelItem';

import {
  lndListPeersRequest,
  lndListChannelsRequest,
  lndPendingChannelsRequest,
  lndConnectPeerRequest,
  lndDisconnectPeerRequest,
} from '../../squeakclient/requests';

export default function LightningNodePage() {
  const classes = useStyles();

  const { pubkey, host, port } = useParams();
  const [value, setValue] = useState(0);
  const [peers, setPeers] = useState(null);
  const [channels, setChannels] = useState(null);
  const [pendingChannels, setPendingChannels] = useState(null);
  const [openChannelDialogOpen, setOpenChannelDialogOpen] = useState(false);
  const [waitingForLightningNode, setWaitingForLightningNode] = useState(false);

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
    const lightningHost = `${host}:${port}`;
    connectPeer(pubkey, lightningHost);
  };

  const handleClickOpenChannel = () => {
    console.log('Handle click open channel.');
    setOpenChannelDialogOpen(true);
  };

  const handleCloseOpenChannelDialog = () => {
    setOpenChannelDialogOpen(false);
  };

  const handleClickDisconnectPeer = () => {
    disconnectPeer(pubkey);
  };

  const handleListPeersResp = (resp) => {
    setWaitingForLightningNode(false);
    setPeers(resp);
  };

  const isConnected = () => {
    if (peers == null) {
      return false;
    }
    let i;
    for (i = 0; i < peers.length; i++) {
      if (pubkey === peers[i].getPubKey()) {
        return true;
      }
    }
    return false;
  };

  const hasChannelToPeer = () => {
    if (channels == null) {
      return false;
    }
    let i;
    for (i = 0; i < channels.length; i++) {
      if (pubkey === channels[i].getRemotePubkey()) {
        return true;
      }
    }
    return false;
  };

  const listPeers = useCallback(() => {
    lndListPeersRequest(handleListPeersResp);
  },
  []);
  const listChannels = () => {
    lndListChannelsRequest(setChannels);
  };
  const getPendingChannels = () => {
    lndPendingChannelsRequest(setPendingChannels);
  };
  const connectPeer = (pubkey, host) => {
    setWaitingForLightningNode(true);
    lndConnectPeerRequest(pubkey, host,
      () => {
        // reloadRoute(history);
        listPeers();
      },
      (err) => {
        setWaitingForLightningNode(false);
        alert(err.message);
      });
  };
  const disconnectPeer = (pubkey) => {
    setWaitingForLightningNode(true);
    lndDisconnectPeerRequest(pubkey, () => {
      // reloadRoute(history);
      listPeers();
    });
  };

  useEffect(() => {
    listPeers();
  }, [listPeers]);
  useEffect(() => {
    listChannels();
  }, []);
  useEffect(() => {
    getPendingChannels();
  }, []);

  function ConnectPeerButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickConnectPeer();
              }}
            >
              Connect Peer
            </Button>
          </div>
        </Grid>
      </>
    );
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
              }}
            >
              Disconnect Peer
            </Button>
          </div>
        </Grid>
      </>
    );
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
              }}
            >
              Open Channel
            </Button>
          </div>
        </Grid>
      </>
    );
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
                : ConnectPeerButton()}
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
              {!hasChannelToPeer()
            && OpenChannelButton()}
            </Grid>
          </Grid>

        </Widget>
      </Grid>
    );
  }

  function ChannelsGridItem() {
    const nodeChannels = channels.filter((channel) => channel.getRemotePubkey() === pubkey);
    const nodePendingOpenChannels = pendingChannels.getPendingOpenChannelsList().filter((pendingOpenChannel) => pendingOpenChannel.getChannel().getRemoteNodePub() === pubkey);
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
              {nodePendingOpenChannels.map((pendingOpenChannel) => (
                <Box
                  p={1}
                  key={pendingOpenChannel.getChannel().getChannelPoint()}
                >
                  <PendingOpenChannelItem
                    key={pendingOpenChannel.getChannel().getChannelPoint()}
                    pendingOpenChannel={pendingOpenChannel}
                  />
                </Box>
              ))}
              {nodeChannels.map((channel) => (
                <Box
                  p={1}
                  key={channel.getChannelPoint()}
                >
                  <ChannelItem
                    key={channel.getChannelPoint()}
                    channel={channel}
                  />
                </Box>
              ))}
            </Grid>
          </Grid>
        </Widget>
      </Grid>
    );
  }

  function IsConnected() {
    return (
      isConnected().toString()
    );
  }

  function HasChannelToPeer() {
    return (
      hasChannelToPeer().toString()
    );
  }

  function NoPubkeyContent() {
    return (
      <div>
        No pubkey.
      </div>
    );
  }

  function PubkeyContent() {
    return (
      <>
        <Grid container spacing={4}>
          {NodeInfoGridItem()}
        </Grid>
      </>
    );
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
      );
    }

    return (
      <>
        <Grid container spacing={4}>
          {ChannelsGridItem()}
        </Grid>
      </>
    );
  }

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

  function LightningNodeTabs() {
    return (
      <>
        <AppBar position="static" color="default">
          <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
            <Tab label="Node Info" {...a11yProps(0)} />
            <Tab label="Channels" {...a11yProps(1)} />
          </Tabs>
        </AppBar>
        <TabPanel value={value} index={0}>
        {waitingForLightningNode
          ? WaitingIndicator()
          : PubkeyContent()}
        </TabPanel>
        <TabPanel value={value} index={1}>
          {ChannelsContent()}
        </TabPanel>
      </>
    );
  }

  function OpenChannelDialogContent() {
    return (
      <>
        <OpenChannelDialog
          open={openChannelDialogOpen}
          pubkey={pubkey}
          handleClose={handleCloseOpenChannelDialog}
        />
      </>
    );
  }

  function WaitingIndicator() {
    return (
      <CircularProgress size={48} className={classes.buttonProgress} />
    );
  }

  return (
    <>
      {pubkey
        ? LightningNodeTabs()
        : NoPubkeyContent()}
      {OpenChannelDialogContent()}
    </>
  );
}
