import React, { useState } from "react";
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Snackbar,
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
import MuiAlert from '@material-ui/lab/Alert';

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";
import MakeSqueakDialog from "../../components/MakeSqueakDialog";
import DeleteSqueakDialog from "../../components/DeleteSqueakDialog";
import BuySqueakDialog from "../../components/BuySqueakDialog";
import SqueakDetailsDialog from "../../components/SqueakDetailsDialog";


import {
  syncSqueakRequest,
  likeSqueakRequest,
  unlikeSqueakRequest,
} from "../../squeakclient/requests"

import {
  getBlockDetailUrl,
} from "../../bitcoin/blockexplorer"

import moment from 'moment';

import {
  goToSqueakAddressPage,
} from "../../navigation/navigation"

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

export default function SqueakDetailItem({
  hash,
  squeak,
  network,
  reloadSqueak,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const [replyDialogOpen, setReplyDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [buyDialogOpen, setBuyDialogOpen] = useState(false);
  const [viewDetailsDialogOpen, setViewDetailsDialogOpen] = useState(false);
  const [unlockedSnackbarOpen, setUnlockedSnackbarOpen] = useState(false);


  const blockDetailUrl = () => {
    return getBlockDetailUrl(squeak.getBlockHash(), network);
  };

  const handleClickOpenReplyDialog = () => {
    setReplyDialogOpen(true);
  };

  const handleCloseReplyDialog = () => {
     setReplyDialogOpen(false);
  };

  const handleClickOpenDeleteDialog = () => {
    setDeleteDialogOpen(true);
    console.log("deleteDialogOpen: " + deleteDialogOpen);
  };

  const handleCloseDeleteDialog = () => {
     setDeleteDialogOpen(false);
  };

  const handleClickOpenBuyDialog = () => {
    setBuyDialogOpen(true);
  };

  const handleCloseBuyDialog = () => {
    setBuyDialogOpen(false);
  };

  const handleClickOpenViewDetailsDialog = () => {
    setViewDetailsDialogOpen(true);
  };

  const handleCloseViewDetailsDialog = () => {
    setViewDetailsDialogOpen(false);
  };

  const handleLikeSqueak = () => {
    console.log("liked.");
    likeSqueakRequest(hash, (response) => {
      reloadSqueak();
    });
  };

  const handleUnlikeSqueak = () => {
    console.log("unliked.");
    unlikeSqueakRequest(hash, (response) => {
      reloadSqueak();
    });
  };

  const onAddressClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log("Handling address click...");
    if (!squeak) {
      return;
    }
    goToSqueakAddressPage(history, squeak.getAuthorAddress());
  }

  const onReplyClick = (event) => {
    event.preventDefault();
    console.log("Handling reply click...");
    if (!squeak) {
      return;
    }
    handleClickOpenReplyDialog();
  }

  const onLikeClick = (event) => {
    event.preventDefault();
    console.log("Handling like click...");
    if (!squeak) {
      return;
    }
    handleLikeSqueak();
  }

  const onUnlikeClick = (event) => {
    event.preventDefault();
    console.log("Handling like click...");
    if (!squeak) {
      return;
    }
    handleUnlikeSqueak();
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
    handleClickOpenViewDetailsDialog();
  }

  const onUnlockClick = (event) => {
    event.preventDefault();
    console.log("Handling unlock click...");
    if (!squeak) {
      return;
    }
    handleClickOpenBuyDialog();
  }

  const onDownloadClick = (event) => {
    event.preventDefault();
    console.log("Handling download click...");
    syncSqueakRequest(hash, (response) => {
      reloadSqueak();
    });
  }

  const handleCloseUnlockedSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setUnlockedSnackbarOpen(false);
  };

  const handlePaymentComplete = () => {
    reloadSqueak();
    setUnlockedSnackbarOpen(true);
  };

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


      function MakeSqueakDialogContent() {
        return (
          <>
            <MakeSqueakDialog
              open={replyDialogOpen}
              handleClose={handleCloseReplyDialog}
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

      function BuyDialogContent() {
        return (
          <>
            <BuySqueakDialog
              open={buyDialogOpen}
              handleClose={handleCloseBuyDialog}
              handlePaymentComplete={handlePaymentComplete}
              hash={hash}
              ></BuySqueakDialog>
          </>
        )
      }

      function ViewDetailsDialogContent() {
        return (
          <>
            <SqueakDetailsDialog
              open={viewDetailsDialogOpen}
              handleClose={handleCloseViewDetailsDialog}
              hash={hash}
              squeak={squeak}
              ></SqueakDetailsDialog>
          </>
        )
      }

      function SqueakUnlockedActionContent() {
        return (
          <Snackbar open={unlockedSnackbarOpen} autoHideDuration={6000} onClose={handleCloseUnlockedSnackbar}>
            <Alert onClose={handleCloseUnlockedSnackbar} severity="success">
              Squeak unlocked!
            </Alert>
          </Snackbar>
        )
      }

      function LikeIconContent() {
        if (squeak && !squeak.getLiked()) {
          return (
            <Box
              p={1}
              onClick={onLikeClick}
              >
              <FavoriteIcon />
            </Box>
          )
        } else {
          return (
            <Box
              p={1}
              onClick={onUnlikeClick}
              >
              <FavoriteIcon
              color="secondary"
                />
            </Box>
          )
        }
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
              {LikeIconContent()}
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
    {MakeSqueakDialogContent()}
    {DeleteSqueakDialogContent()}
    {BuyDialogContent()}
    {ViewDetailsDialogContent()}
    {SqueakUnlockedActionContent()}
    </>
  )
}
