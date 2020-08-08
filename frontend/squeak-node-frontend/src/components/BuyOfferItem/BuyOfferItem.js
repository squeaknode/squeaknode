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

export default function BuyOfferItem({
  offer,
  handleOfferClick,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const onOfferClick = (event) => {
    event.preventDefault();
    console.log("Handling offer click...");
    if (handleOfferClick) {
      handleOfferClick();
    }
  }

  function OfferContent() {
    return (
      <Typography
        size="md"
        >{offer.getAmount()} msats ({offer.getAmount() / 1000} sats)
      </Typography>
    )
  }

  function ProfileInfoContent(peer) {
    return (
      <Box>
        <Typography
          size="md"
          >{peer.getPeerName()}
          </Typography>
      </Box>
    )
  }

  return (
    <Box
      p={1}
      m={0}
      style={{backgroundColor: 'white'}}
      onClick={onOfferClick}
      >
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            {OfferContent()}
          </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            {ProfileInfoContent(offer.getPeer())}
          </Grid>
          </Grid>
    </Box>
  )
}
