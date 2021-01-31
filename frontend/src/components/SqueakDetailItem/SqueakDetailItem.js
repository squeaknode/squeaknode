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
  Divider,
  Button,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

import LockIcon from '@material-ui/icons/Lock';

import ReplyIcon from '@material-ui/icons/Reply';
import RepeatIcon from '@material-ui/icons/Repeat';
import FavoriteIcon from '@material-ui/icons/Favorite';
import DeleteIcon from '@material-ui/icons/Delete';
import DownloadIcon from '@material-ui/icons/CloudDownload';
import ZoomInIcon from '@material-ui/icons/ZoomIn';

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";



import {
  syncSqueakRequest,
} from "../../squeakclient/requests"

import {
  getBlockDetailUrl,
} from "../../bitcoin/blockexplorer"

import moment from 'moment';

export default function SqueakDetailItem({
  hash,
  squeak,
  network,
  handleReplyClick,
  handleDeleteClick,
  handleViewDetailsClick,
  handleUnlockClick,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const goToSqueakAddressPage = () => {
    history.push("/app/squeakaddress/" + squeak.getAuthorAddress());
  };

  const reloadRoute = () => {
    history.go(0);
  };

  const blockDetailUrl = () => {
    // return "https://blockstream.info/testnet/block/" + squeak.getBlockHash();
    return getBlockDetailUrl(squeak.getBlockHash(), network);
  };

  const onAddressClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log("Handling address click...");
    if (!squeak) {
      return;
    }
    goToSqueakAddressPage(squeak.getAuthorAddress());
  }

  const onReplyClick = (event) => {
    event.preventDefault();
    console.log("Handling reply click...");
    if (!squeak) {
      return;
    }
    handleReplyClick();
  }

  const onDeleteClick = (event) => {
    event.preventDefault();
    console.log("Handling delete click...");
    if (!squeak) {
      return;
    }
    handleDeleteClick();
  }

  const onZoomInClick = (event) => {
    event.preventDefault();
    console.log("Handling zoomin click...");
    if (!squeak) {
      return;
    }
    //handleClickOpenDeleteDialog();
    // goToSqueakDetailPage();
    handleViewDetailsClick();
  }

  const onUnlockClick = (event) => {
    event.preventDefault();
    console.log("Handling unlock click...");
    if (!squeak) {
      return;
    }
    // goToBuyPage(squeak.getSqueakHash());
    handleUnlockClick();
  }

  const onDownloadClick = (event) => {
    event.preventDefault();
    console.log("Handling download click...");
    syncSqueakRequest(hash, (response) => {
      reloadRoute();
    });
  }

  function SqueakUnlockedContent() {
    return (
      <Typography
        variant="h4"
        style={{whiteSpace: 'pre-line'}}
        >{squeak.getContentStr()}
      </Typography>
    )
  }

  function SqueakLockedContent() {
    return (
      <>
        <LockIcon />
        <Button
          variant="contained"
          onClick={onUnlockClick}
          >Buy to unlock
        </Button>

      </>
    )
  }

  function SqueakMissingContent() {
    return (
      <>
        <DownloadIcon />
        <Button
          variant="contained"
          onClick={onDownloadClick}
          >Download
        </Button>
      </>
    )
  }

  function SqueakContent() {
    if (!squeak) {
      return (
        <>
          {SqueakMissingContent()}
        </>
      )
    }

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
    if (!squeak) {
      return SqueakLockedBackgroundColor();
    }
    return squeak.getIsUnlocked()
            ? SqueakUnlockedBackgroundColor()
            : SqueakLockedBackgroundColor()
  }

  function getAddressDisplay() {
    if (!squeak) {
      return "Author unknown"
    }
    return squeak.getIsAuthorKnown()
      ? squeak.getAuthor().getProfileName()
      : squeak.getAuthorAddress()
  }

  function SqueakTime() {
    if (!squeak) {
      return (
        <Box color="secondary.main" fontWeight="fontWeightBold">
          Unknown time
        </Box>
      )
    }

    return (
      <Box color="secondary.main" fontWeight="fontWeightBold">
        {moment(squeak.getBlockTime()*1000).fromNow()}
        <span> </span>(Block
        <Link
          href={blockDetailUrl()}
          target="_blank"
          rel="noopener"
          onClick={(event) => event.stopPropagation()}>
          <span> </span>#{squeak.getBlockHeight()}
        </Link>
        )
      </Box>
    )
  }


  return (
    <>
    <Paper elevation={3} className={classes.paper}
      p={1}
      m={0}
      style={SqueakBackgroundColor()}
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
                    {getAddressDisplay()}
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
              {SqueakTime()}
            </Grid>
          </Grid>
          <Divider />
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item xs={3} sm={1}>
              <Box
                p={1}
                onClick={onReplyClick}
                >
              <ReplyIcon />
            </Box>
            </Grid>
            <Grid item xs={3} sm={1}>
                <Box
                  p={1}
                  >
                  <RepeatIcon />
                </Box>
            </Grid>
            <Grid item xs={3} sm={1}>
                <Box
                  p={1}
                  >
                  <FavoriteIcon />
                </Box>
            </Grid>
            <Grid item xs={3} sm={1}>
                <Box
                  p={1}
                  onClick={onDeleteClick}
                  >
                  <DeleteIcon />
                </Box>
            </Grid>
            <Grid item xs={3} sm={1}>
                <Box
                  p={1}
                  onClick={onZoomInClick}
                  >
                  <ZoomInIcon />
                </Box>
            </Grid>
          </Grid>
    </Paper>
    </>
  )
}
