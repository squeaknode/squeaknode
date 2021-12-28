import React from 'react';
import {
  Paper,
  Typography,
  Grid,
  Box,
  Link,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

import LockIcon from '@material-ui/icons/Lock';
import DownloadIcon from '@material-ui/icons/CloudDownload';

// styles
import useStyles from './styles';

import SqueakActionBar from '../SqueakActionBar';
import SqueakTime from '../SqueakTime';
import PrivateSqueakIndicator from '../PrivateSqueakIndicator';

import {
  goToSqueakPage,
  goToPubkeyPage,
} from '../../navigation/navigation';

export default function SqueakThreadItem({
  hash,
  squeak,
  network,
  reloadSqueak,
  showActionBar,
  ...props
}) {
  const classes = useStyles();

  const history = useHistory();

  const onAddressClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling address click...');
    if (!squeak) {
      return;
    }
    goToPubkeyPage(history, squeak.getAuthorPubkey());
  };
  //
  // const onRecipientAddressClick = (event) => {
  //   event.preventDefault();
  //   event.stopPropagation();
  //   console.log('Handling recipient click...');
  //   if (!squeak || !squeak.getIsPrivate()) {
  //     return;
  //   }
  //   goToPubkeyPage(history, squeak.getRecipientPubkey());
  // };

  const onSqueakClick = (event) => {
    event.preventDefault();
    console.log(`Handling squeak click for hash: ${hash}`);
    goToSqueakPage(history, hash);
  };

  function PrivateMessageRecipient() {
    return (
      // <Grid
      //   container
      //   direction="row"
      //   justify="flex-start"
      //   alignItems="flex-start"
      // >
      //   <Grid item>
      //     <ForwardIcon/>
      //     <Link
      //       href="#"
      //       onClick={onRecipientAddressClick}
      //     >
      //       {getRecipientAddressDisplay()}
      //     </Link>
      //   </Grid>
      // </Grid>
      <PrivateSqueakIndicator squeak={squeak}>
      </PrivateSqueakIndicator>
    );
  }

  function SqueakUnlockedContent() {
    return (
      <Typography
        size="md"
        style={{
          whiteSpace: 'pre-line', overflow: 'hidden', textOverflow: 'ellipsis', height: '6rem',
        }}
      >
        {squeak.getContentStr()}
      </Typography>
    );
  }

  function SqueakLockedContent() {
    return (
      <>
        <LockIcon />
      </>
    );
  }

  function SqueakMissingContent() {
    return (
      <>
        <DownloadIcon />
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

  function getAddressDisplay() {
    if (!squeak) {
      return 'Author unknown';
    }
    return squeak.getIsAuthorKnown()
      ? squeak.getAuthor().getProfileName()
      : squeak.getAuthorPubkey();
  }

  // function getRecipientAddressDisplay() {
  //   if (!squeak) {
  //     return 'Recipient unknown';
  //   }
  //   return squeak.getIsRecipientKnown()
  //     ? squeak.getRecipient().getProfileName()
  //     : squeak.getRecipientPubkey();
  // }

  function SqueakBackgroundColor() {
    if (!squeak || !squeak.getContentStr()) {
      return SqueakLockedBackgroundColor();
    }
    return SqueakUnlockedBackgroundColor();
  }

  return (
    <Paper
      elevation={3}
      className={classes.paper}
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
            <Link
              href="#"
              onClick={onAddressClick}
            >
              {getAddressDisplay()}
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
      {showActionBar
            && (
            <SqueakActionBar
              hash={hash}
              squeak={squeak}
              network={network}
              reloadSqueak={reloadSqueak}
            />
            )}
    </Paper>
  );
}
