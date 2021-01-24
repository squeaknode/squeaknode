import React from "react";
import {
  Typography,
  Grid,
  Box,
  Link,
} from "@material-ui/core";
import {useHistory} from "react-router-dom";
import LockIcon from '@material-ui/icons/Lock';
import DownloadIcon from '@material-ui/icons/CloudDownload';
import moment from 'moment';
import {
  getBlockDetailUrl
} from "../../bitcoin/blockexplorer"
import {navigateTo, PROFILE_VIEW, SQUEAK_ADDRESS_VIEW, SQUEAK_VIEW} from "../../navigation/routes";


export default function SqueakThreadItem({
  hash,
  squeak,
  network,
  ...props
}) {
  const history = useHistory();

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
    navigateTo(history, SQUEAK_ADDRESS_VIEW, [squeak.getAuthorAddress()]);
  }

  const onSqueakClick = (event) => {
    event.preventDefault();
    console.log("Handling squeak click for hash: " + hash);
    navigateTo(history, SQUEAK_VIEW, [hash]);
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

  function SqueakMissingContent() {
    return (
      <>
        <DownloadIcon />
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

  function SqueakLockedBackgroundColor() {
    return {backgroundColor: 'lightgray'};
  }

  function SqueakUnlockedBackgroundColor() {
    return {backgroundColor: 'white'};
  }

  function getAddressDisplay() {
    if (!squeak) {
      return "Author unknown"
    }
    return squeak.getIsAuthorKnown()
      ? squeak.getAuthorName()
      : squeak.getAuthorAddress()
  }

  function SqueakBackgroundColor() {
    if (!squeak) {
      return SqueakLockedBackgroundColor();
    }
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
    </Box>
  )
}
