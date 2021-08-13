import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
   Grid,
   Button,
   Box,
} from "@material-ui/core";

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

import {
  getSqueakProfileByAddressRequest,
  getAddressSqueakDisplaysRequest,
  connectSqueakPeerRequest,
  disconnectSqueakPeerRequest,
  getConnectedPeerRequest,
} from "../../squeakclient/requests"
import {
  goToSqueakAddressPage,
  goToProfilePage,
} from "../../navigation/navigation"


export default function PeerAddressPage() {
  var classes = useStyles();
  const history = useHistory();
  const { host, port } = useParams();
  const [connectedPeer, setConnectedPeer] = useState([]);
  // const [squeakProfile, setSqueakProfile] = useState(null);
  // const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);
  // const [disconnectPeerDialogOpen, setDisconnectPeerDialogOpen] = useState(false);

  // const getSqueakProfile = (address) => {
  //       getSqueakProfileByAddressRequest(address, setSqueakProfile);
  // };

  // const handleClickOpenCreateContactProfileDialog = () => {
  //   setCreateContactProfileDialogOpen(true);
  // };
  //
  // const handleCloseCreateContactProfileDialog = () => {
  //   setCreateContactProfileDialogOpen(false);
  // };

  const getConnectedPeer = () => {
    getConnectedPeerRequest(host, port, setConnectedPeer);
  };

    // const handleClickOpenDisconnectPeerDialog = () => {
    //   setDisconnectPeerDialogOpen(true);
    // };
    //
    // const handleCloseDisconnectPeerDialog = () => {
    //   setDisconnectPeerDialogOpen(false);
    // };

  // useEffect(()=>{
  //   getSqueakProfile(address)
  // },[address]);

  // function NoProfileContent() {
  //   return (
  //     <div>
  //       No profile for address.
  //       <Button variant="contained" onClick={() => {
  //           handleClickOpenCreateContactProfileDialog();
  //         }}>Create Profile</Button>
  //     </div>
  //   )
  // }
  //
  // function ProfileContent() {
  //   return (
  //     <div className={classes.root}>
  //       Profile:
  //       <Button variant="contained" onClick={() => {
  //           goToProfilePage(history, squeakProfile.getProfileId());
  //         }}>{squeakProfile.getProfileName()}</Button>
  //     </div>
  //   )
  // }

  // function DisconnectPeerDialogContent() {
  //   return (
  //     <>
  //       <ConnectPeerDialog
  //         open={connectPeerDialogOpen}
  //         handleClose={handleCloseConnectPeerDialog}
  //         ></ConnectPeerDialog>
  //     </>
  //   )
  // }

  useEffect(() => {
    getConnectedPeer()
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
    console.log(connectedPeer);
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
    console.log(connectedPeer);
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
    console.log(connectedPeer);
    return (
      <>
      <Typography variant="h2" component="h2">
        {'Peer Address: ' + host + ":" + port}
      </Typography>
      </>
    )
  }

  return (
    <>
      {AddressContent()}
      {ConnectionStatusContent()}
      {ConnectionActionContent()}
    </>
  );
}
