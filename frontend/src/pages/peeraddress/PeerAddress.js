import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
   Grid,
   Button,
   Box,
} from "@material-ui/core";
import Card from '@material-ui/core/Card';
import CardHeader from "@material-ui/core/CardHeader";


// styles
import useStyles from "./styles";

// components
import Widget from "../../components/Widget";
import SqueakThreadItem from "../../components/SqueakThreadItem";
import CreateContactProfileDialog from "../../components/CreateContactProfileDialog";
import SqueakUserAvatar from "../../components/SqueakUserAvatar";

import Timeline from '@material-ui/lab/Timeline';
import TimelineItem from '@material-ui/lab/TimelineItem';
import TimelineSeparator from '@material-ui/lab/TimelineSeparator';
import TimelineConnector from '@material-ui/lab/TimelineConnector';
import TimelineContent from '@material-ui/lab/TimelineContent';
import TimelineOppositeContent from '@material-ui/lab/TimelineOppositeContent';
import Typography from '@material-ui/core/Typography';

import FaceIcon from '@material-ui/icons/Face';
import ComputerIcon from '@material-ui/icons/Computer';

import moment from 'moment';

import {
  getSqueakProfileByAddressRequest,
  getAddressSqueakDisplaysRequest,
  connectSqueakPeerRequest,
  disconnectSqueakPeerRequest,
  getConnectedPeerRequest,
  subscribeConnectedPeersRequest,
  subscribeConnectedPeerRequest,
} from "../../squeakclient/requests"
import {
  goToSqueakAddressPage,
  goToProfilePage,
} from "../../navigation/navigation"


export default function PeerAddressPage() {
  var classes = useStyles();
  const history = useHistory();
  const { host, port } = useParams();
  const [connectedPeer, setConnectedPeer] = useState(null);

  const getConnectedPeer = () => {
    getConnectedPeerRequest(host, port, setConnectedPeer);
  };

  const subscribeConnectedPeer = () => {
    subscribeConnectedPeerRequest(host, port, (connectedPeer) => {
      console.log(connectedPeer);
      setConnectedPeer(connectedPeer);
    });
  };

  useEffect(() => {
    getConnectedPeer();
  }, []);
  useEffect(() => {
    subscribeConnectedPeer();
  }, []);

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
               });
            }}>Disconnect Peer
          </Button>
        </div>
      </Grid>
      </>
    )
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
            }}>Connect Peer
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function ConnectionStatusContent() {
    return (
      <>
      <Grid item xs={12}>
        Status: {(connectedPeer)
          ? "Connected"
          : "Disconnected"
        }
      </Grid>
      </>
    )
  }

  function ConnectionActionContent() {
    return (
      <>
      <Grid item xs={12}>
        {(connectedPeer)
          ? DisconnectPeerButton()
          : ConnectPeerButton()
        }
      </Grid>
      </>
    )
  }

  function AddressContent() {
    return (
      <>
      <Typography variant="h2" component="h2">
        {'Peer Address: ' + host + ":" + port}
      </Typography>
      </>
    )
  }

  function PeerConnectionDetails() {
    const connectTimeS = connectedPeer.getConnectTimeS();
    const momentTimeString = moment(connectTimeS*1000).fromNow();
    const lastMsgReceivedTimeS = connectedPeer.getLastMessageReceivedTimeS();
    const lastMsgReceivedString = moment(lastMsgReceivedTimeS*1000).fromNow();
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
    )
  }

  function PeerConnectionContent() {
    console.log(connectedPeer);
    return (
      <Card
         className={classes.root}
      >
        <CardHeader
           avatar={<ComputerIcon/>}
           title={`Peer Address: ${host + ":" + port}`}
           subheader={PeerConnectionDetails()}
        />
      </Card>
    )
  }

  return (
    <>
      {AddressContent()}
      {ConnectionStatusContent()}
      {ConnectionActionContent()}
      {(connectedPeer) && PeerConnectionContent()}
    </>
  );
}
