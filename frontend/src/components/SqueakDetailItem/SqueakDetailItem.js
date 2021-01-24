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
import MakeSqueakDialog from "../../components/MakeSqueakDialog";
import DeleteSqueakDialog from "../../components/DeleteSqueakDialog";

import {
  syncSqueakRequest,
} from "../../squeakclient/requests"

import {
  getBlockDetailUrl,
} from "../../bitcoin/blockexplorer"

import moment from 'moment';
import {navigateTo, BUY_VIEW, PROFILE_VIEW, SQUEAK_DETAIL_VIEW} from "../../navigation/routes";

export default function SqueakDetailItem({
  hash,
  squeak,
  network,
  handleReplyClick,
  handleDeleteClick,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();
  const [replyDialogOpen, setReplyDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  const handleClickOpen = () => {
    setReplyDialogOpen(true);
  };

  const handleClose = () => {
     setReplyDialogOpen(false);
  };

  const handleClickOpenDeleteDialog = () => {
    setDeleteDialogOpen(true);
    console.log("deleteDialogOpen: " + deleteDialogOpen);
  };

  const handleCloseDeleteDialog = () => {
     setDeleteDialogOpen(false);
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
    navigateTo(history, PROFILE_VIEW, [squeak.getAuthorAddress()]);
  }

  const onReplyClick = (event) => {
    event.preventDefault();
    console.log("Handling reply click...");
    if (!squeak) {
      return;
    }
    handleClickOpen();
  }

  const onDeleteClick = (event) => {
    event.preventDefault();
    console.log("Handling delete click...");
    if (!squeak) {
      return;
    }
    handleClickOpenDeleteDialog();
  }

  const onZoomInClick = (event) => {
    event.preventDefault();
    console.log("Handling zoomin click...");
    if (!squeak) {
      return;
    }
    //handleClickOpenDeleteDialog();
    navigateTo(history, SQUEAK_DETAIL_VIEW, [hash]);
  }

  const onUnlockClick = (event) => {
    event.preventDefault();
    console.log("Handling unlock click...");
    if (!squeak) {
      return;
    }
    navigateTo(history, BUY_VIEW, [squeak.getSqueakHash()]);
  }

  const onDownloadClick = (event) => {
    event.preventDefault();
    console.log("Handling download click...");
    // goToBuyPage(squeak.getSqueakHash());
    console.log("syncSqueakRequest with hash: " + hash);
    syncSqueakRequest(hash, (response) => {
      console.log("response:");
      console.log(response);
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
      ? squeak.getAuthorName()
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

  function MakeSqueakDialogContent() {
    return (
      <>
        <MakeSqueakDialog
          open={replyDialogOpen}
          handleClose={handleClose}
          replytoSqueak={squeak}
          ></MakeSqueakDialog>
      </>
    )
  }

  function DeleteSqueakDialogContent() {
    return (
      <>
        <DeleteSqueakDialog
          open={deleteDialogOpen}
          handleClose={handleCloseDeleteDialog}
          squeakToDelete={squeak}
          ></DeleteSqueakDialog>
      </>
    )
  }

  return (
    <>
    <Box
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
    </Box>
    {MakeSqueakDialogContent()}
    {DeleteSqueakDialogContent()}
    </>
  )
}
