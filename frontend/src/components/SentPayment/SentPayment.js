import React, { useState } from "react";
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

import LockIcon from '@material-ui/icons/Lock';
import DownloadIcon from '@material-ui/icons/CloudDownload';

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';

import {
  goToSqueakPage,
  goToPeerPage,
  goToLightningNodePage,
} from "../../navigation/navigation"


export default function SentPayment({
  sentPayment,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const onSqueakClick = (event) => {
    event.preventDefault();
    var hash = sentPayment.getSqueakHash();
    console.log("Handling squeak click for hash: " + hash);
    goToSqueakPage(history, hash);
  }

  const onPeerClick = (event) => {
    event.preventDefault();
    const peerId = getPeerId();
    if (peerId == null) {
      return;
    }
    console.log("Handling peer click for peerId: " + peerId);
    goToPeerPage(history, peerId);
  }

  const onLightningNodeClick = (event) => {
    event.preventDefault();
    var nodePubkey = sentPayment.getNodePubkey();
    console.log("Handling lightning node click for nodePubkey: " + nodePubkey);
    goToLightningNodePage(history, nodePubkey);
  }

  const getPeerId = () => {
    if (!sentPayment.getHasPeer()) {
      return null;
    }
    const peer = sentPayment.getPeer();
    return peer.getPeerId();
  }

  const getPeerDisplay = () => {
    if (!sentPayment.getHasPeer()) {
      return "Unknown peer";
    }
    const peer = sentPayment.getPeer();
    const peerName = peer.getPeerName();
    const peerId = peer.getPeerId();
    return peerName ? peerName : peerId;
  }

  function PeerDisplay() {
    if (sentPayment.getHasPeer()) {
      return HasPeerDisplay(sentPayment.getPeer());
    } else {
      return HasNoPeerDisplay();
    }
  }

  function HasPeerDisplay(peer) {
    const peerId = peer.getPeerId();
    const peerName = peer.getPeerName();
    const peerDisplayName = peerName ? peerName : peerId;
    return (
      <Link href="#"
        onClick={onPeerClick}
        >{peerDisplayName}
      </Link>
    )
  }

  function HasNoPeerDisplay() {
    return (
      <>
        Unknown Peer
      </>
    )
  }

  console.log(sentPayment);
  return (
    <Box
      p={1}
      m={0}
      style={{ backgroundColor: "lightgray" }}
      >
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
                <Box fontWeight="fontWeightBold">
                  {sentPayment.getPriceMsat()} msats
                </Box>
            </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              {moment(sentPayment.getTimeS() * 1000).format("DD MMM YYYY hh:mm a")}
            </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              Squeak hash:
                <Link href="#"
                  onClick={onSqueakClick}
                  >
                  <span> </span>{sentPayment.getSqueakHash()}
                  </Link>
            </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              Peer: {PeerDisplay()}
            </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              Lightning node:
                <Link href="#"
                  onClick={onLightningNodeClick}
                  >
                  <span> </span>{sentPayment.getNodePubkey()}
                </Link>
            </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              Valid:
                <span> </span>{sentPayment.getValid().toString()}
            </Grid>
          </Grid>
    </Box>
  )
}
