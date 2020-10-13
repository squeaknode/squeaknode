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

export default function ChannelItem({
  channel,
  handleChannelClick,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const onChannelClick = (event) => {
    event.preventDefault();
    console.log("Handling channel click...");
    if (handleChannelClick) {
      handleChannelClick();
    }
  }

  function ChannelContent() {
    return (
      <Typography
        size="md"
        style={{whiteSpace: 'pre-line', overflow: "hidden", textOverflow: "ellipsis", height: '6rem'}}
        >{channel.getCapacity()}
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
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
                <Box color="secondary.main" fontWeight="fontWeightBold">
                  {channel.getChannelPoint()}
                </Box>
            </Grid>
          </Grid>
    </Box>
  )
}
