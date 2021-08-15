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
import SqueakActionBar from "../../components/SqueakActionBar";


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

  const [buyDialogOpen, setBuyDialogOpen] = useState(false);
  const [unlockedSnackbarOpen, setUnlockedSnackbarOpen] = useState(false);


  const blockDetailUrl = () => {
    return getBlockDetailUrl(squeak.getBlockHash(), network);
  };

  const handleClickOpenBuyDialog = () => {
    setBuyDialogOpen(true);
  };

  const handleCloseBuyDialog = () => {
    setBuyDialogOpen(false);
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

      function SqueakUnlockedActionContent() {
        return (
          <Snackbar open={unlockedSnackbarOpen} autoHideDuration={6000} onClose={handleCloseUnlockedSnackbar}>
            <Alert onClose={handleCloseUnlockedSnackbar} severity="success">
              Squeak unlocked!
            </Alert>
          </Snackbar>
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
          <SqueakActionBar
            hash={hash}
            squeak={squeak}
            network={network}
            reloadSqueak={reloadSqueak}
          ></SqueakActionBar>
    </Paper>
    {BuyDialogContent()}
    {SqueakUnlockedActionContent()}
    </>
  )
}
