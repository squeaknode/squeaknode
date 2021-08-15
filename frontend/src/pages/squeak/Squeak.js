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
import Paper from '@material-ui/core/Paper';

import FaceIcon from '@material-ui/icons/Face';

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakDetailItem from "../../components/SqueakDetailItem";
import SqueakThreadItem from "../../components/SqueakThreadItem";
import SqueakUserAvatar from "../../components/SqueakUserAvatar";
import SqueakThread from "../../components/SqueakThread";
import SqueakReplies from "../../components/SqueakReplies";


import {
  getSqueakDisplayRequest,
  getAncestorSqueakDisplaysRequest,
  getReplySqueakDisplaysRequest,
  getNetworkRequest,
} from "../../squeakclient/requests"
import {
  goToSqueakAddressPage,
} from "../../navigation/navigation"


export default function SqueakPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [squeak, setSqueak] = useState(null);
  const [ancestorSqueaks, setAncestorSqueaks] = useState([]);
  const [replySqueaks, setReplySqueaks] = useState([]);
  const [network, setNetwork] = useState("");

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

  const unknownAncestorHash = () => {
      if (!ancestorSqueaks) {
        return null;
      }
      var oldestKnownAncestor = ancestorSqueaks[0];
      if (!oldestKnownAncestor) {
        return null;
      }
      return oldestKnownAncestor.getReplyTo();
  };

  const getCurrentSqueak = () => {
      getSqueak(hash);
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
        goToSqueakAddressPage(history, squeak.getAuthorAddress());
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
    squeak={null}
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
      <SqueakThread
        squeaks={ancestorSqueaks.slice(0, -1)}
        network={network}
        setSqueaksFn={setAncestorSqueaks}
      ></SqueakThread>
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
    squeakProfile={squeak && squeak.getAuthor()}
  />
</TimelineSeparator>
<TimelineContent>
<SqueakDetailItem
  key={hash}
  hash={hash}
  squeak={squeak}
  reloadSqueak={getCurrentSqueak}
  network={network}>
</SqueakDetailItem>
<Divider />
</TimelineContent>
</TimelineItem>
    )
  }

  function RepliesContent() {
    return (
      <SqueakReplies
        squeaks={replySqueaks}
        network={network}
        setSqueaksFn={setReplySqueaks}
      ></SqueakReplies>
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

  function GridContent() {
    return (
      <Grid container spacing={0}>
      <Grid item xs={12} sm={9}>
        <Paper className={classes.paper}>
        {SqueakContent()}
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
      {GridContent()}
    </>
  );
}
