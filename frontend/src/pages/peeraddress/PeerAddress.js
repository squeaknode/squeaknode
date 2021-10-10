import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import {
  Grid,
  Button,
  Box,
  CircularProgress,
} from '@material-ui/core';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';

// styles

// components

import Typography from '@material-ui/core/Typography';
import ComputerIcon from '@material-ui/icons/Computer';
import CloudOff from '@material-ui/icons/CloudOff';

import moment from 'moment';
import CreatePeerDialog from '../../components/CreatePeerDialog';

import useStyles from './styles';

import {
  connectSqueakPeerRequest,
  disconnectSqueakPeerRequest,
  getConnectedPeerRequest,
  getPeerByAddressRequest,
  // subscribeConnectedPeerRequest,
} from '../../squeakclient/requests';
import {
  goToPeerPage,
} from '../../navigation/navigation';

export default function PeerAddressPage() {
  const classes = useStyles();
  const history = useHistory();
  const { host, port, useTor } = useParams();
  const [savedPeer, setSavedPeer] = useState(null);
  const [connectedPeer, setConnectedPeer] = useState(null);
  const [waitingForConnectedPeer, setWaitingForConnectedPeer] = useState(false);
  const [createSavedPeerDialogOpen, setCreateSavedPeerDialogOpen] = useState(false);

  const getPeer = useCallback(() => {
    getPeerByAddressRequest(host, port, setSavedPeer);
  },
  [host, port]);
  const getConnectedPeer = useCallback(() => {
    setWaitingForConnectedPeer(true);
    console.log("useTor: " + useTor);
    const useTorBool = useTor === 'true';
    getConnectedPeerRequest(host, port, useTorBool, handleLoadedConnectedPeer);
  },
  [host, port, useTor]);

  const disconnectPeer = useCallback(() => {
    setWaitingForConnectedPeer(true);
    disconnectSqueakPeerRequest(host, port, () => {
      getConnectedPeer();
    });
  },
  [host, port, getConnectedPeer]);

  const connectPeer = useCallback(() => {
    setWaitingForConnectedPeer(true);
    connectSqueakPeerRequest(host, port, () => {
      getConnectedPeer();
    },
    handleConnectPeerError);
  },
  [host, port, getConnectedPeer]);

  // const subscribeConnectedPeer = useCallback(() => subscribeConnectedPeerRequest(host, port, (connectedPeer) => {
  //   setConnectedPeer(connectedPeer);
  // }),
  // [host, port]);

  const handleClickOpenCreateSavedPeerDialog = () => {
    setCreateSavedPeerDialogOpen(true);
  };

  const handleCloseCreateSavedPeerDialog = () => {
    setCreateSavedPeerDialogOpen(false);
  };

  useEffect(() => {
    getPeer();
  }, [getPeer]);
  useEffect(() => {
    getConnectedPeer();
  }, [getConnectedPeer]);
  // useEffect(() => {
  //   const stream = subscribeConnectedPeer();
  //   return () => stream.cancel();
  // }, [subscribeConnectedPeer]);

  const handleLoadedConnectedPeer = (resp) => {
    setWaitingForConnectedPeer(false);
    setConnectedPeer(resp);
  };

  const handleConnectPeerError = (err) => {
    setWaitingForConnectedPeer(false);
    alert(`Connect peer failure: ${err}`);
  };

  function DisconnectPeerButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                disconnectPeer();
              }}
            >
              Disconnect Peer
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
                connectPeer();
              }}
            >
              Connect Peer
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function ConnectionActionContent() {
    return (
      <>
        <Grid item xs={12}>
          {(connectedPeer)
            ? DisconnectPeerButton()
            : ConnectPeerButton()}
        </Grid>
      </>
    );
  }

  function AddressContent() {
    return (
      <>
        <Typography variant="h2" component="h2">
          {`Peer Address: ${host}:${port}`}
        </Typography>
      </>
    );
  }

  function ConnectedPeerDetails() {
    const connectTimeS = connectedPeer.getConnectTimeS();
    const momentTimeString = moment(connectTimeS * 1000).fromNow();
    const lastMsgReceivedTimeS = connectedPeer.getLastMessageReceivedTimeS();
    const lastMsgReceivedString = moment(lastMsgReceivedTimeS * 1000).fromNow();
    const numMsgsReceived = connectedPeer.getNumberMessagesReceived();
    const numBytesReceived = connectedPeer.getNumberBytesReceived();
    const numMsgsSent = connectedPeer.getNumberMessagesSent();
    const numBytesSent = connectedPeer.getNumberBytesSent();
    return (
      <>
        <Box>
          {`Connect time: ${momentTimeString}`}
        </Box>
        <Box>
          {`Last message received: ${lastMsgReceivedString}`}
        </Box>
        <Box>
          {`Number of messages received: ${numMsgsReceived}`}
        </Box>
        <Box>
          {`Number of bytes received: ${numBytesReceived}`}
        </Box>
        <Box>
          {`Number of messages sent: ${numMsgsSent}`}
        </Box>
        <Box>
          {`Number of bytes sent: ${numBytesSent}`}
        </Box>
      </>
    );
  }

  function ConnectedPeerContent() {
    console.log(connectedPeer);
    return (
      <Card
        className={classes.root}
      >
        <CardHeader
          avatar={<ComputerIcon fontSize="large" style={{ fill: 'green' }} />}
          title={`Peer Address: ${`${host}:${port}`}`}
          subheader={ConnectedPeerDetails()}
        />
      </Card>
    );
  }

  function DisconnectedPeerContent() {
    console.log(connectedPeer);
    return (
      <Card
        className={classes.root}
      >
        <CardHeader
          avatar={<CloudOff fontSize="large" style={{ fill: 'red' }} />}
          title={`Peer Address: ${`${host}:${port}`}`}
          subheader="Disconnected"
        />
      </Card>
    );
  }

  function ConnectionContent() {
    return (
      <>
        {ConnectionActionContent()}
        {(connectedPeer)
          ? ConnectedPeerContent()
          : DisconnectedPeerContent()}
      </>
    );
  }

  function WaitingIndicator() {
    return (
      <CircularProgress size={48} className={classes.buttonProgress} />
    );
  }

  function SavedPeerContent() {
    return (
      <>
        {savedPeer
          ? PeerContent()
          : NoPeerContent()}
        {CreateSavedPeerDialogContent()}
      </>

    );
  }

  function NoPeerContent() {
    return (
      <div>
        No saved peer for this address.
        <Button
          variant="contained"
          onClick={() => {
            handleClickOpenCreateSavedPeerDialog();
          }}
        >
          Save Peer
        </Button>
      </div>
    );
  }

  function PeerContent() {
    return (
      <div className={classes.root}>
        Saved Peer:
        <Button
          variant="contained"
          onClick={() => {
            goToPeerPage(history, savedPeer.getPeerId());
          }}
        >
          {savedPeer.getPeerName()}
        </Button>
      </div>
    );
  }

  function CreateSavedPeerDialogContent() {
    return (
      <>
        <CreatePeerDialog
          open={createSavedPeerDialogOpen}
          handleClose={handleCloseCreateSavedPeerDialog}
          initialHost={host}
          initialPort={port}
        />
      </>
    );
  }

  return (
    <>
      {AddressContent()}
      {SavedPeerContent()}
      {waitingForConnectedPeer
        ? WaitingIndicator()
        : ConnectionContent()}
    </>
  );
}
