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
import DownloadIcon from '@material-ui/icons/CloudDownload';

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';

export default function SentPayment({
  sentPayment,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const goToSqueakPage = (hash) => {
    history.push("/app/squeak/" + hash);
  };

  const goToLightningNodePage = (pubkey, host, port) => {
      console.log("Go to lightning node for pubkey: " + pubkey);
      if (pubkey && host && port) {
        history.push("/app/lightningnode/" + pubkey + "/" + host + "/" + port);
      } else if (pubkey && host) {
        history.push("/app/lightningnode/" + pubkey + "/" + host);
      } else {
        history.push("/app/lightningnode/" + pubkey);
      }
  };

  const onSqueakClick = (event) => {
    event.preventDefault();
    var hash = sentPayment.getSqueakHash();
    console.log("Handling squeak click for hash: " + hash);
    if (goToSqueakPage) {
      goToSqueakPage(hash);
    }
  }

  const onLightningNodeClick = (event) => {
    event.preventDefault();
    var nodePubkey = sentPayment.getSqueakHash();
    console.log("Handling lightning node click for nodePubkey: " + nodePubkey);
    if (goToLightningNodePage) {
      goToLightningNodePage(nodePubkey);
    }
  }

  return (
    <Box
      p={1}
      m={0}
      style={{ backgroundColor: "lightgray" }}
      >
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
                <Box fontWeight="fontWeightBold">
                  {sentPayment.getPriceMsat()} mSats
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
              Squeak hash:
                <Link href="#"
                  onClick={onSqueakClick}
                  >
                  <span> </span>{sentPayment.getSqueakHash()}
                  </Link>
            </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              Lightning node:
                <Link href="#"
                  onClick={onLightningNodeClick}
                  >
                  <span> </span>{sentPayment.getNodePubkey()}
                </Link>
            </Grid>
          </Grid>
    </Box>
  )
}
