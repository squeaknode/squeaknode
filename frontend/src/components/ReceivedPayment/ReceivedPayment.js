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

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';

import {
  goToSqueakPage,
  goToPeerAddressPage,
} from "../../navigation/navigation"


export default function ReceivedPayment({
  receivedPayment,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const onSqueakClick = (event) => {
    event.preventDefault();
    var hash = receivedPayment.getSqueakHash();
    console.log("Handling squeak click for hash: " + hash);
    goToSqueakPage(history, hash);
  }

  const onPeerClick = (event) => {
    event.preventDefault();
    goToPeerAddressPage(
      history,
      receivedPayment.getPeerHost(),
      receivedPayment.getPeerPort(),
    );
  }

  function PeerDisplay() {
    const peerAddress = receivedPayment.getPeerHost() + ":" + receivedPayment.getPeerPort();
    return (
      <Box>
        <Typography
          size="md"
          >Peer: <Link href="#" onClick={onPeerClick}>
            {peerAddress}
          </Link>
        </Typography>
      </Box>
    )
  }

  console.log("receivedPayment:");
  console.log(receivedPayment);
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
                  {receivedPayment.getPriceMsat()} msats
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
              {moment(receivedPayment.getTimeS() * 1000).format("DD MMM YYYY hh:mm a")}
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
                  <span> </span>{receivedPayment.getSqueakHash()}
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
              {PeerDisplay()}
            </Grid>
          </Grid>
    </Box>
  )
}
