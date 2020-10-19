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

export default function PendingOpenChannelItem({
  pendingOpenChannel,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const getTxId = (channel) => {
    var channelPoint = channel.getChannelPoint();
    if (channelPoint == null) {
      return null;
    }
    var pieces = channelPoint.split(":");
    return pieces[0];
  }

  const getOutputIndex = (channel) => {
    var channelPoint = channel.getChannelPoint();
    if (channelPoint == null) {
      return null;
    }
    var pieces = channelPoint.split(":");
    if (pieces.length < 2) {
      return null;
    }
    return pieces[1];
  }

  const goToChannelPage = (txId, outputIndex) => {
    history.push("/app/channel/" + txId + "/" + outputIndex);
  };

  const onChannelClick = (event) => {
    event.preventDefault();
    console.log("Handling channel click...");
    var channel = pendingOpenChannel.getChannel();
    var txId = getTxId(channel);
    var outputIndex = getOutputIndex(channel);
    goToChannelPage(txId, outputIndex);
  }

  function ChannelContent() {
    var channel = pendingOpenChannel.getChannel();
    return (
      <Typography component="div">
        <Box fontSize="h3.fontSize" m={1}>
          Pending Open Channel
        </Box>
        <Box m={1}>
          Capacity: {channel.getCapacity()}
        </Box>
        <Box m={1}>
          Local Balance: {channel.getLocalBalance()}
        </Box>
        <Box m={1}>
          Remote Balance: {channel.getRemoteBalance()}
        </Box>
        <Box m={1}>
          Pubkey: {channel.getRemoteNodePub()}
        </Box>
        <Box m={1}>
          Channel Point: {channel.getChannelPoint()}
        </Box>
      </Typography>
    )
  }

  return (
    <Box
      p={1}
      m={0}
      style={{backgroundColor: '#e0e0e0'}}
      onClick={onChannelClick}
      >
        <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            {ChannelContent()}
          </Grid>
          </Grid>
    </Box>
  )
}
