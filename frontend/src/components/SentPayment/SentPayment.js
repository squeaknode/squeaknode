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
  goToPeerAddressPage,
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
    goToPeerAddressPage(
      history,
      sentPayment.getPeerAddress().getHost(),
      sentPayment.getPeerAddress().getPort(),
    );
  }

  const onLightningNodeClick = (event) => {
    event.preventDefault();
    var nodePubkey = sentPayment.getNodePubkey();
    console.log("Handling lightning node click for nodePubkey: " + nodePubkey);
    goToLightningNodePage(history, nodePubkey);
  }

  function PeerDisplay() {
    const peerAddress =  sentPayment.getPeerAddress();
    const host = peerAddress.getHost();
    const peerAddressText =  peerAddress.getHost() + ":" + peerAddress.getPort();
    return (
      <Box>
        <Typography
          size="md"
          >Peer: <Link href="#" onClick={onPeerClick}>
            {peerAddressText}
          </Link>
        </Typography>
      </Box>
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
