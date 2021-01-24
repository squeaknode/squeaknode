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

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';
import {navigateTo, PROFILE_VIEW, SQUEAK_VIEW} from "../../navigation/routes";

export default function SentOffer({
  receivedPayment,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const paymentTimeMs = receivedPayment.setPaymentTimeMs();

  const onSqueakClick = (event) => {
    event.preventDefault();
    var hash = receivedPayment.getSqueakHash();
    console.log("Handling squeak click for hash: " + hash);
    navigateTo(history, SQUEAK_VIEW, [hash]);
  }

  console.log("receivedPayment:");
  console.log(receivedPayment);
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
                  {receivedPayment.getPriceMsat()} msats
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
              {paymentTimeMs ?
                moment(receivedPayment.setPaymentTimeMs()).format("DD MMM YYYY hh:mm a") : "Not paid"}
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
                  <span> </span>{receivedPayment.getSqueakHash()}
                  </Link>
            </Grid>
          </Grid>
    </Box>
  )
}
