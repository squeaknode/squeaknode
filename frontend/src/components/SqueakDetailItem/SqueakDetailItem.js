import React, { useState } from 'react';
import {
  Paper,
  Typography,
  Snackbar,
  Grid,
  Box,
  Link,
  Button,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

import LockIcon from '@material-ui/icons/Lock';

import DownloadIcon from '@material-ui/icons/CloudDownload';
import MuiAlert from '@material-ui/lab/Alert';

// styles
import useStyles from './styles';

import BuySqueakDialog from '../BuySqueakDialog';
import SqueakActionBar from '../SqueakActionBar';
import SqueakTime from '../SqueakTime';
import SqueakUserAvatar from '../SqueakUserAvatar';
import PrivateSqueakIndicator from '../PrivateSqueakIndicator';


import {
  goToPubkeyPage,
} from '../../navigation/navigation';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

export default function SqueakDetailItem({
  hash,
  squeak,
  network,
  reloadSqueak,
  handleDownloadAncestorsClick,
  ...props
}) {
  const classes = useStyles();

  const history = useHistory();

  const [buyDialogOpen, setBuyDialogOpen] = useState(false);
  const [unlockedSnackbarOpen, setUnlockedSnackbarOpen] = useState(false);

  const handleClickOpenBuyDialog = () => {
    setBuyDialogOpen(true);
  };

  const handleCloseBuyDialog = () => {
    setBuyDialogOpen(false);
  };

  const onAddressClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling address click...');
    if (!squeak) {
      return;
    }
    goToPubkeyPage(history, squeak.getAuthorPubkey());
  };

  const onUnlockClick = (event) => {
    event.preventDefault();
    console.log('Handling unlock click...');
    if (!squeak) {
      return;
    }
    handleClickOpenBuyDialog();
  };

  const onDownloadClick = (event) => {
    event.preventDefault();
    console.log('Handling download click...');
    handleDownloadAncestorsClick();
  };

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

  function PrivateMessageRecipient() {
    return (
      <PrivateSqueakIndicator squeak={squeak}>
      </PrivateSqueakIndicator>
    );
  }

  function SqueakUnlockedContent() {
    return (
      <Typography
        variant="h4"
        style={{ whiteSpace: 'pre-line' }}
      >
        {squeak.getContentStr()}
      </Typography>
    );
  }

  function SqueakLockedContent() {
    return (
      <>
        <LockIcon />
        <Button
          variant="contained"
          onClick={onUnlockClick}
        >
          Buy to unlock
        </Button>

      </>
    );
  }

  function SqueakMissingContent() {
    return (
      <>
        <DownloadIcon />
        <Button
          variant="contained"
          onClick={onDownloadClick}
        >
          Download
        </Button>
      </>
    );
  }

  function SqueakContent() {
    if (!squeak) {
      return (
        <>
          {SqueakMissingContent()}
        </>
      );
    }
    return (
      <>
        {squeak.getIsUnlocked()
          ? SqueakUnlockedContent()
          : SqueakLockedContent()}
      </>
    );
  }

  function SqueakLockedBackgroundColor() {
    return { backgroundColor: 'lightgray' };
  }

  function SqueakUnlockedBackgroundColor() {
    return { backgroundColor: 'white' };
  }

  function SqueakBackgroundColor() {
    if (!squeak || !squeak.getContentStr()) {
      return SqueakLockedBackgroundColor();
    }
    return SqueakUnlockedBackgroundColor();
  }

  function getAddressDisplay() {
    if (!squeak) {
      return 'Author unknown';
    }
    return squeak.getIsAuthorKnown()
      ? squeak.getAuthor().getProfileName()
      : squeak.getAuthorPubkey();
  }

  function BuyDialogContent() {
    return (
      <>
        <BuySqueakDialog
          key={hash}
          open={buyDialogOpen}
          handleClose={handleCloseBuyDialog}
          handlePaymentComplete={handlePaymentComplete}
          hash={hash}
        />
      </>
    );
  }

  function SqueakUnlockedActionContent() {
    return (
      <Snackbar open={unlockedSnackbarOpen} autoHideDuration={6000} onClose={handleCloseUnlockedSnackbar}>
        <Alert onClose={handleCloseUnlockedSnackbar} severity="success">
          Squeak unlocked!
        </Alert>
      </Snackbar>
    );
  }

  return (
    <>
      <Paper
        elevation={3}
        className={classes.paper}
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
              {squeak
                ? (
                  <SqueakUserAvatar
                    squeakAddress={squeak.getAuthorPubkey()}
                    squeakProfile={squeak.getAuthor()}
                  />
                ) : (
                  <SqueakUserAvatar
                    squeakAddress={null}
                    squeakProfile={null}
                  />
                )}
            </Box>
          </Grid>
          <Grid item>
            <Box p={2} fontWeight="fontWeightBold">
              <Link
                href="#"
                onClick={onAddressClick}
              >
                <Typography
                  variant="h3"
                  style={{ whiteSpace: 'pre-line' }}
                >
                  {getAddressDisplay()}
                </Typography>
              </Link>
            </Box>
          </Grid>
        </Grid>
        {squeak.getIsPrivate() && PrivateMessageRecipient()}
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
            <SqueakTime
              hash={hash}
              squeak={squeak}
              network={network}
            />
          </Grid>
        </Grid>
        {squeak
          && (
          <SqueakActionBar
            hash={hash}
            squeak={squeak}
            network={network}
            reloadSqueak={reloadSqueak}
          />
          )}
      </Paper>
      {BuyDialogContent()}
      {SqueakUnlockedActionContent()}
    </>
  );
}
