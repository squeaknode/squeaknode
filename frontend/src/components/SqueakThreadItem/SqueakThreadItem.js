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

export default function SqueakThreadItem({
  squeak,
  handleAddressClick,
  handleSqueakClick,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const blockDetailUrl = "https://blockstream.info/testnet/block/" + squeak.getBlockHash();

  const onAddressClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log("Handling address click...");
    if (handleAddressClick) {
      handleAddressClick();
    }
  }

  const onSqueakClick = (event) => {
    event.preventDefault();
    console.log("Handling squeak click...");
    if (handleSqueakClick) {
      handleSqueakClick();
    }
  }

  function SqueakUnlockedContent() {
    return (
      <Typography
        size="md"
        style={{whiteSpace: 'pre-line', overflow: "hidden", textOverflow: "ellipsis", height: '6rem'}}
        >{squeak.getContentStr()}
      </Typography>
    )
  }

  function SqueakLockedContent() {
    return (
      <>
        <LockIcon />
      </>
    )
  }

  function SqueakContent() {
    return (
      <>
      {squeak.getIsUnlocked()
          ? SqueakUnlockedContent()
          : SqueakLockedContent()
        }
      </>
    )
  }

  function SqueakLockedBackgroundColor() {
    return {backgroundColor: 'lightgray'};
  }

  function SqueakUnlockedBackgroundColor() {
    return {backgroundColor: 'white'};
  }

  function SqueakBackgroundColor() {
    return squeak.getIsUnlocked()
            ? SqueakUnlockedBackgroundColor()
            : SqueakLockedBackgroundColor()
  }

  return (
    <Box
      p={1}
      m={0}
      style={SqueakBackgroundColor()}
      onClick={onSqueakClick}
      >
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
                <Box fontWeight="fontWeightBold">
                  <Link href="#"
                    onClick={onAddressClick}>
                    {squeak.getIsAuthorKnown()
                      ? squeak.getAuthorName()
                      : squeak.getAuthorAddress()}
                  </Link>
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
            {SqueakContent()}
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
                  {moment(squeak.getBlockTime()*1000).fromNow()}
                  <span> </span>(Block
                  <Link href={blockDetailUrl}
                    onClick={(event) => event.stopPropagation()}>
                    <span> </span>#{squeak.getBlockHeight()}
                  </Link>
                  )
                </Box>
            </Grid>
          </Grid>
    </Box>
  )
}
