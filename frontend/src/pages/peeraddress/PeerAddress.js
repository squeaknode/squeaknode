import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
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

import moment from 'moment';
import useStyles from './styles';

import {
  connectSqueakPeerRequest,
  disconnectSqueakPeerRequest,
  getConnectedPeerRequest,
  // subscribeConnectedPeerRequest,
} from '../../squeakclient/requests';

export default function PeerAddressPage() {
  const classes = useStyles();
  const { host, port } = useParams();
  const [connectedPeer, setConnectedPeer] = useState(null);
  const [waitingForConnectedPeer, setWaitingForConnectedPeer] = useState(false);

  const getConnectedPeer = useCallback(() => {
    setWaitingForConnectedPeer(true);
    getConnectedPeerRequest(host, port, handleLoadedConnectedPeer);
  },
  [host, port]);

  // const subscribeConnectedPeer = useCallback(() => subscribeConnectedPeerRequest(host, port, (connectedPeer) => {
  //   setConnectedPeer(connectedPeer);
  // }),
  // [host, port]);

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
                disconnectSqueakPeerRequest(host, port, () => {
                  // TODO: nothing maybe
                },
                handleConnectPeerError);
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
                connectSqueakPeerRequest(host, port, () => {
                // TODO: nothing maybe
                });
              }}
            >
              Connect Peer
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function ConnectionStatusContent() {
    return (
      <>
        <Grid item xs={12}>
          Status:
          {' '}
          {(connectedPeer)
            ? 'Connected'
            : 'Disconnected'}
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

  function PeerConnectionDetails() {
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

  function PeerConnectionInfoContent() {
    console.log(connectedPeer);
    return (
      <Card
        className={classes.root}
      >
        <CardHeader
          avatar={<ComputerIcon />}
          title={`Peer Address: ${`${host}:${port}`}`}
          subheader={PeerConnectionDetails()}
        />
      </Card>
    );
  }

  function ConnectionContent() {
    return (
      <>
        {ConnectionStatusContent()}
        {ConnectionActionContent()}
        {(connectedPeer) && PeerConnectionInfoContent()}
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
      {AddressContent()}
      {waitingForConnectedPeer
        ? WaitingIndicator()
        : ConnectionContent()}
    </>
  );
}
