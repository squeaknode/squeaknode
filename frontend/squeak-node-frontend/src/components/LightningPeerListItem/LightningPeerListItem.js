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
  handlePeerClick,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const onPeerClick = (event) => {
    event.preventDefault();
    console.log("Handling peer click...");
    if (handlePeerClick) {
      handlePeerClick();
    }
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
