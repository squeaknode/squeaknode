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
import TimelineDot from '@material-ui/lab/TimelineDot';
import Paper from '@material-ui/core/Paper';

import FaceIcon from '@material-ui/icons/Face';

import {
  getSqueakProfileByAddressRequest,
  getAddressSqueakDisplaysRequest,
  getNetworkRequest,
} from "../../squeakclient/requests"
import {
  goToSqueakAddressPage,
  goToProfilePage,
} from "../../navigation/navigation"


export default function SqueakAddressPage() {
  var classes = useStyles();
  const history = useHistory();
  const { address } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [squeaks, setSqueaks] = useState([]);
  const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);
  const [network, setNetwork] = useState("");

  const getSqueakProfile = (address) => {
        getSqueakProfileByAddressRequest(address, setSqueakProfile);
  };
  const getSqueaks = (address) => {
      getAddressSqueakDisplaysRequest(address, setSqueaks);
  };
  const getNetwork = () => {
      getNetworkRequest(setNetwork);
  };

  const handleClickOpenCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(true);
  };

  const handleCloseCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(false);
  };

  useEffect(()=>{
    getSqueakProfile(address)
  },[address]);
  useEffect(()=>{
    getSqueaks(address)
  },[address]);
  useEffect(()=>{
    getNetwork()
  },[]);

  function NoProfileContent() {
    return (
      <div>
        No profile for address.
        <Button variant="contained" onClick={() => {
            handleClickOpenCreateContactProfileDialog();
          }}>Create Profile</Button>
      </div>
    )
  }

  function ProfileContent() {
    return (
      <div className={classes.root}>
        Profile:
        <Button variant="contained" onClick={() => {
            goToProfilePage(history, squeakProfile.getProfileId());
          }}>{squeakProfile.getProfileName()}</Button>
      </div>
    )
  }

  function NoSqueaksContent() {
    return (
      <div>
        Unable to load squeaks.
      </div>
    )
  }

  function TimelineUserAvatar(squeak) {
    const handleAvatarClick = () => {
      console.log("Avatar clicked...");
      goToSqueakAddressPage(history, squeak.getAuthorAddress());
    };
    return (
      <TimelineDot
      onClick={handleAvatarClick}
      style={{cursor: 'pointer'}}
      >
        <FaceIcon />
      </TimelineDot>
    )
  }

  function SqueaksContent() {
    return (
      <>
        <div>
          {squeaks.map(squeak =>
            <Timeline
              align="left"
              key={squeak.getSqueakHash()}
            >

            <TimelineItem>
      <TimelineOppositeContent
    className={classes.oppositeContent}
    color="textSecondary"
      ></TimelineOppositeContent>
      <TimelineSeparator>
        <SqueakUserAvatar
          squeakProfile={squeak.getAuthor()}
        />
      </TimelineSeparator>
      <TimelineContent>
      <SqueakThreadItem
        hash={squeak.getSqueakHash()}
        key={squeak.getSqueakHash()}
        squeak={squeak}
        network={network}>
      </SqueakThreadItem>
      </TimelineContent>
      </TimelineItem>

            </Timeline>
          )}
        </div>
      </>
    )
  }

  function CreateContactProfileDialogContent() {
    return (
      <>
        <CreateContactProfileDialog
          open={createContactProfileDialogOpen}
          handleClose={handleCloseCreateContactProfileDialog}
          initialAddress={address}
          ></CreateContactProfileDialog>
      </>
    )
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
      <Grid item xs={12} sm={9}>
        <Paper className={classes.paper}>
        {(squeaks)
          ? SqueaksContent()
          : NoSqueaksContent()
        }
        </Paper>
      </Grid>
      <Grid item xs={12} sm={3}>
        <Paper className={classes.paper}>
        </Paper>
      </Grid>
      </Grid>
    )
  }

  return (
    <>
      {squeakProfile
        ? ProfileContent()
        : NoProfileContent()
      }
      {GridContent()}
      {CreateContactProfileDialogContent()}
    </>
  );
}
