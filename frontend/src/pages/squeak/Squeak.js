import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  Divider,
  Snackbar,
  Box,
} from "@material-ui/core";

import Timeline from '@material-ui/lab/Timeline';
import TimelineItem from '@material-ui/lab/TimelineItem';
import TimelineSeparator from '@material-ui/lab/TimelineSeparator';
import TimelineConnector from '@material-ui/lab/TimelineConnector';
import TimelineContent from '@material-ui/lab/TimelineContent';
import TimelineOppositeContent from '@material-ui/lab/TimelineOppositeContent';
import TimelineDot from '@material-ui/lab/TimelineDot';
import MuiAlert from '@material-ui/lab/Alert';

import FaceIcon from '@material-ui/icons/Face';

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakDetailItem from "../../components/SqueakDetailItem";
import SqueakThreadItem from "../../components/SqueakThreadItem";
import SqueakUserAvatar from "../../components/SqueakUserAvatar";

import MakeSqueakDialog from "../../components/MakeSqueakDialog";
import DeleteSqueakDialog from "../../components/DeleteSqueakDialog";
import BuySqueakDialog from "../../components/BuySqueakDialog";
import SqueakDetailsDialog from "../../components/SqueakDetailsDialog";


import {
  getSqueakDisplayRequest,
  getAncestorSqueakDisplaysRequest,
  getReplySqueakDisplaysRequest,
  getNetworkRequest,
} from "../../squeakclient/requests"


function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}


export default function SqueakPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [squeak, setSqueak] = useState(null);
  const [ancestorSqueaks, setAncestorSqueaks] = useState([]);
  const [replySqueaks, setReplySqueaks] = useState([]);
  const [network, setNetwork] = useState("");

  const [replyDialogOpen, setReplyDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [buyDialogOpen, setBuyDialogOpen] = useState(false);
  const [viewDetailsDialogOpen, setViewDetailsDialogOpen] = useState(false);
  const [unlockedSnackbarOpen, setUnlockedSnackbarOpen] = useState(false);

  const getSqueak = (hash) => {
      getSqueakDisplayRequest(hash, setSqueak);
  };
  const getAncestorSqueaks = (hash) => {
      getAncestorSqueakDisplaysRequest(hash, setAncestorSqueaks);
  };
  const getReplySqueaks = (hash) => {
      getReplySqueakDisplaysRequest(hash, setReplySqueaks);
  };
  const getNetwork = () => {
      getNetworkRequest(setNetwork);
  };

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
  };

  const unknownAncestorHash = () => {
      if (!ancestorSqueaks) {
        return null;
      }
      var oldestKnownAncestor = ancestorSqueaks[0];
      if (!oldestKnownAncestor) {
        return null;
      }
      console.log(oldestKnownAncestor);
      console.log("oldestKnownAncestor");
      return oldestKnownAncestor.getReplyTo();
  };

  const handleClickOpen = () => {
    setReplyDialogOpen(true);
  };

  const handleClose = () => {
     setReplyDialogOpen(false);
  };

  const handleClickOpenDeleteDialog = () => {
    setDeleteDialogOpen(true);
    console.log("deleteDialogOpen: " + deleteDialogOpen);
  };

  const handleCloseDeleteDialog = () => {
     setDeleteDialogOpen(false);
  };

  const handleClickOpenBuyDialog = () => {
    setBuyDialogOpen(true);
  };

  const handleCloseBuyDialog = () => {
    setBuyDialogOpen(false);
  };

  const handleClickOpenViewDetailsDialog = () => {
    setViewDetailsDialogOpen(true);
  };

  const handleCloseViewDetailsDialog = () => {
    setViewDetailsDialogOpen(false);
  };

  const handleCloseUnlockedSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setUnlockedSnackbarOpen(false);
  };

  const handlePaymentComplete = () => {
    getSqueak(hash);
    setUnlockedSnackbarOpen(true);
  };


  useEffect(()=>{
    getSqueak(hash)
  },[hash]);
  useEffect(()=>{
    getAncestorSqueaks(hash)
  },[hash]);
  useEffect(()=>{
    getReplySqueaks(hash)
  },[hash]);
  useEffect(()=>{
    getNetwork()
  },[]);

  function NoSqueakContent() {
    return (
      <div>
        Unable to load squeak.
      </div>
    )
  }

  function TimelineUserAvatar(squeak) {
    const handleAvatarClick = () => {
      console.log("Avatar clicked...");
      if (squeak) {
        goToSqueakAddressPage(squeak.getAuthorAddress());
      }
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

  function UnkownReplyToContent() {
    var squeakHash = unknownAncestorHash();
    if (!squeakHash) {
      return (
        <></>
      )
    }
    return (
      <TimelineItem>
<TimelineOppositeContent
  className={classes.oppositeContent}
  color="textSecondary"
></TimelineOppositeContent>
<TimelineSeparator>
  <SqueakUserAvatar
    squeak={squeak}
  />
  <TimelineConnector />
</TimelineSeparator>
<TimelineContent>
<SqueakThreadItem
  hash={squeakHash}
  key={squeakHash}
  squeak={null}>
</SqueakThreadItem>
</TimelineContent>
</TimelineItem>
    )
  }

  function AncestorsContent() {
    return (
      <>
        {ancestorSqueaks.slice(0, -1)
          //.reverse()
          .map(ancestorSqueak =>
            <TimelineItem>
  <TimelineOppositeContent
    className={classes.oppositeContent}
    color="textSecondary"
  ></TimelineOppositeContent>
  <TimelineSeparator>
    <SqueakUserAvatar
      squeak={ancestorSqueak}
    />
    <TimelineConnector />
  </TimelineSeparator>
  <TimelineContent>
  <Box
    key={ancestorSqueak.getSqueakHash()}
    >
  <SqueakThreadItem
    hash={ancestorSqueak.getSqueakHash()}
    key={ancestorSqueak.getSqueakHash()}
    squeak={ancestorSqueak}
    network={network}>
  </SqueakThreadItem>
  </Box>
  </TimelineContent>
</TimelineItem>
        )}
      </>
    )
  }

  function CurrentSqueakContent() {
    return (
      <TimelineItem>
<TimelineOppositeContent
  className={classes.oppositeContent}
  color="textSecondary"
></TimelineOppositeContent>
<TimelineSeparator>
  <SqueakUserAvatar
    squeak={squeak}
  />
</TimelineSeparator>
<TimelineContent>
<SqueakDetailItem
  hash={hash}
  squeak={squeak}
  handleReplyClick={handleClickOpen}
  handleDeleteClick={handleClickOpenDeleteDialog}
  handleViewDetailsClick={handleClickOpenViewDetailsDialog}
  handleUnlockClick={handleClickOpenBuyDialog}
  network={network}>
</SqueakDetailItem>
<Divider />
</TimelineContent>
</TimelineItem>
    )
  }

  function RepliesContent() {
    console.log("replySqueaks: " + replySqueaks);
    return (
      <>
        {replySqueaks
          .map(replySqueak =>
            <TimelineItem>
  <TimelineOppositeContent
    className={classes.oppositeContent}
    color="textSecondary"
  ></TimelineOppositeContent>
  <TimelineSeparator>
    <SqueakUserAvatar
      squeak={replySqueak}
    />
  </TimelineSeparator>
  <TimelineContent>
  <Box
    p={1}
    key={replySqueak.getSqueakHash()}
    >
  <SqueakThreadItem
    hash={replySqueak.getSqueakHash()}
    key={replySqueak.getSqueakHash()}
    squeak={replySqueak}
    network={network}>
  </SqueakThreadItem>
  </Box>
  </TimelineContent>
</TimelineItem>
        )}
      </>
    )
  }

  function SqueakContent() {
    return (
      <Timeline align="left">

        {UnkownReplyToContent()}
        {AncestorsContent()}
        {CurrentSqueakContent()}
        {RepliesContent()}

      </Timeline>
    )
  }


    function MakeSqueakDialogContent() {
      return (
        <>
          <MakeSqueakDialog
            open={replyDialogOpen}
            handleClose={handleClose}
            replytoSqueak={squeak}
            ></MakeSqueakDialog>
        </>
      )
    }

    function DeleteSqueakDialogContent() {
      return (
        <>
          <DeleteSqueakDialog
            open={deleteDialogOpen}
            handleClose={handleCloseDeleteDialog}
            squeakToDelete={squeak}
            ></DeleteSqueakDialog>
        </>
      )
    }

    function BuyDialogContent() {
      return (
        <>
          <BuySqueakDialog
            open={buyDialogOpen}
            handleClose={handleCloseBuyDialog}
            handlePaymentComplete={handlePaymentComplete}
            hash={hash}
            ></BuySqueakDialog>
        </>
      )
    }

    function ViewDetailsDialogContent() {
      return (
        <>
          <SqueakDetailsDialog
            open={viewDetailsDialogOpen}
            handleClose={handleCloseViewDetailsDialog}
            hash={hash}
            squeak={squeak}
            ></SqueakDetailsDialog>
        </>
      )
    }


    function SqueakUnlockedContent() {
      return (
        <Snackbar open={unlockedSnackbarOpen} autoHideDuration={6000} onClose={handleCloseUnlockedSnackbar}>
          <Alert onClose={handleCloseUnlockedSnackbar} severity="success">
            Squeak unlocked!
          </Alert>
        </Snackbar>
      )
    }

  return (
    <>
      <PageTitle title="Squeak" />
      {SqueakContent()}
      {MakeSqueakDialogContent()}
      {DeleteSqueakDialogContent()}
      {BuyDialogContent()}
      {ViewDetailsDialogContent()}
      {SqueakUnlockedContent()}
    </>
  );
}
