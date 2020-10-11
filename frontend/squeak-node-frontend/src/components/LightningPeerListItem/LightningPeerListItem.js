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

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';

export default function LightningPeerListItem({
  peer,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const onPeerClick = (event) => {
    event.preventDefault();
    console.log("Handling peer click...");
    goToLightningNodePage();
  }

  const goToLightningNodePage = () => {
    var pubkey = peer.getPubKey();
    var host = getPeerHost();
    var port = getPeerPort();
    history.push("/app/lightningnode/" + pubkey + "/" + host + "/" + port);
  };

  const getPeerHost = () => {
    var address = peer.getAddress();
    if (address == null) {
      return null;
    }
    var pieces = address.split(":");
    return pieces[0];
  }

  const getPeerPort = () => {
    var address = peer.getAddress();
    if (address == null) {
      return null;
    }
    var pieces = address.split(":");
    if (pieces.length < 2) {
      return null;
    }
    return pieces[1];
  }

  function PeerContent() {
    return (
      <Typography
        size="md"
        >{peer.getPubKey()}
      </Typography>
    )
  }

  return (
    <Box
      p={1}
      m={0}
      style={{backgroundColor: 'lightgray'}}
      onClick={onPeerClick}
      >
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            <Typography
              size="md"
              >Pubkey: {peer.getPubKey()}
            </Typography>
          </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            <Typography
              size="md"
              >Address: {peer.getAddress()}
            </Typography>
          </Grid>
          </Grid>
    </Box>
  )
}
