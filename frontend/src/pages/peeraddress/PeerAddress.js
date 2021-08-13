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
import PageTitle from "../../components/PageTitle";
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

import FaceIcon from '@material-ui/icons/Face';

import {
  getSqueakProfileByAddressRequest,
  getAddressSqueakDisplaysRequest,
} from "../../squeakclient/requests"
import {
  goToSqueakAddressPage,
  goToProfilePage,
} from "../../navigation/navigation"


export default function PeerAddressPage() {
  var classes = useStyles();
  const history = useHistory();
  const { host, port } = useParams();
  // const [squeakProfile, setSqueakProfile] = useState(null);
  // const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);

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

  // function CreatePeerProfileDialogContent() {
  //   return (
  //     <>
  //       <CreateContactProfileDialog
  //         open={createContactProfileDialogOpen}
  //         handleClose={handleCloseCreateContactProfileDialog}
  //         initialAddress={address}
  //         ></CreateContactProfileDialog>
  //     </>
  //   )
  // }

  return (
    <>
      <PageTitle title={'Peer Address: ' + host + ":" + port} />
    </>
  );
}
