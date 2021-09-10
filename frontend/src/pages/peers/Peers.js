import React, { useState, useEffect } from 'react';
import {
  Grid,
  Button,
  Tabs,
  Tab,
  AppBar,
  Box,
  Typography,
} from '@material-ui/core';

// styles
import { makeStyles } from '@material-ui/core/styles';

// components
import Widget from '../../components/Widget';
import CreatePeerDialog from '../../components/CreatePeerDialog';
import ConnectPeerDialog from '../../components/ConnectPeerDialog';
import PeerListItem from '../../components/PeerListItem';
import SavedPeerListItem from '../../components/SavedPeerListItem';
import ShowExternalAddressDialog from '../../components/ShowExternalAddressDialog';

// data

import {
  getPeersRequest,
  getConnectedPeersRequest,
} from '../../squeakclient/requests';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

export default function Peers() {
  const classes = useStyles();
  const [connectedPeers, setConnectedPeers] = useState([]);
  const [peers, setPeers] = useState([]);
  const [createPeerDialogOpen, setCreatePeerDialogOpen] = useState(false);
  const [connectPeerDialogOpen, setConnectPeerDialogOpen] = useState(false);
  const [value, setValue] = useState(0);
  const [showExternalAddressDialogOpen, setShowExternalAddressDialogOpen] = useState(false);

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const getConnectedPeers = () => {
    getConnectedPeersRequest(setConnectedPeers);
  };

  // const subscribeConnectedPeers = () => subscribeConnectedPeersRequest(setConnectedPeers);

  const getSqueakPeers = () => {
    getPeersRequest(setPeers);
  };

  const handleClickOpenCreatePeerDialog = () => {
    setCreatePeerDialogOpen(true);
  };

  const handleCloseCreatePeerDialog = () => {
    setCreatePeerDialogOpen(false);
  };

  const handleClickOpenConnectPeerDialog = () => {
    setConnectPeerDialogOpen(true);
  };

  const handleCloseConnectPeerDialog = () => {
    setConnectPeerDialogOpen(false);
  };

  const handleClickOpenShowExternalAddressDialog = () => {
    setShowExternalAddressDialogOpen(true);
  };

  const handleCloseShowExternalAddressDialog = () => {
    setShowExternalAddressDialogOpen(false);
  };

  useEffect(() => {
    getConnectedPeers();
  }, []);
  // useEffect(() => {
  //   const stream = subscribeConnectedPeers();
  //   return () => stream.cancel();
  // }, []);
  useEffect(() => {
    getSqueakPeers();
  }, []);

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

  function CreatePeerButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickOpenCreatePeerDialog();
              }}
            >
              Create Peer
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function ConnectPeerButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickOpenConnectPeerDialog();
              }}
            >
              Connect Peer
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function ShowExternalAddressButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickOpenShowExternalAddressDialog();
              }}
            >
              Show External Address
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function PeersCountSummary() {
    return (
      <Grid item xs={12}>
        <Box
          p={1}
        >
          <Typography variant="h5" component="h5">
            {`Number of connected peers: ${connectedPeers.length}`}
          </Typography>
        </Box>
      </Grid>
    );
  }

  function PeersGridItem() {
    return (
      <Grid item xs={12}>
        {connectedPeers.map((peer) => (
          <Box
            p={1}
            key={peer.getPeerAddress()}
          >
            <PeerListItem
              key={peer.getPeerAddress()}
              handlePeerClick={() => console.log('clicked peer')}
              peer={peer}
            />
          </Box>
        ))}
      </Grid>
    );
  }

  function SavedPeersGridItem() {
    return (
      <Grid item xs={12}>
        {peers.map((peer) => (
          <Box
            p={1}
            key={peer.getPeerName()}
          >
            <SavedPeerListItem
              key={peer.getPeerName()}
              handlePeerClick={() => console.log('clicked peer')}
              peer={peer}
            />
          </Box>
        ))}
      </Grid>
    );
  }

  function PeersTabs() {
    return (
      <>
        <AppBar position="static" color="default">
          <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
            <Tab label="Connected Peers" {...a11yProps(0)} />
            <Tab label="Saved Peers" {...a11yProps(1)} />
          </Tabs>
        </AppBar>
        <TabPanel value={value} index={0}>
          {ConnectedPeersContent()}
        </TabPanel>
        <TabPanel value={value} index={1}>
          {SavedPeersContent()}
        </TabPanel>
      </>
    );
  }

  function ConnectedPeersContent() {
    return (
      <>
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Widget disableWidgetMenu>
              {ConnectPeerButton()}
              {ShowExternalAddressButton()}
              {PeersCountSummary()}
              {PeersGridItem()}
            </Widget>
          </Grid>
        </Grid>
      </>
    );
  }

  function SavedPeersContent() {
    return (
      <>
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Widget disableWidgetMenu>
              {CreatePeerButton()}
              {SavedPeersGridItem()}
            </Widget>
          </Grid>
        </Grid>
      </>
    );
  }

  function CreatePeerDialogContent() {
    return (
      <>
        <CreatePeerDialog
          open={createPeerDialogOpen}
          handleClose={handleCloseCreatePeerDialog}
        />
      </>
    );
  }

  function ConnectPeerDialogContent() {
    return (
      <>
        <ConnectPeerDialog
          open={connectPeerDialogOpen}
          handleClose={handleCloseConnectPeerDialog}
        />
      </>
    );
  }

  function ShowExternalAddressDialogContent() {
    return (
      <>
        <ShowExternalAddressDialog
          open={showExternalAddressDialogOpen}
          handleClose={handleCloseShowExternalAddressDialog}
        />
      </>
    );
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          {PeersTabs()}
        </Grid>
        <Grid item xs={12} sm={3} />
      </Grid>
    );
  }

  return (
    <>
      {GridContent()}
      {CreatePeerDialogContent()}
      {ConnectPeerDialogContent()}
      {ShowExternalAddressDialogContent()}
    < />
  );
}
