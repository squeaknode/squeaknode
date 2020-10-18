import React, {useState, useEffect} from 'react';
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField,
  DialogActions,
  Button,
  FormControl,
  InputLabel,
  Select,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";
import SqueakThreadItem from "../../components/SqueakThreadItem";


import {
  CloseChannelRequest,
  ChannelPoint,
  PayOfferRequest,
} from "../../proto/lnd_pb"
import { client } from "../../squeakclient/squeakclient"


export default function BuyOfferDialog({
  open,
  offer,
  handleClose,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  const payOffer = (offerId) => {
    console.log("called payOffer");

    var payOfferRequest = new PayOfferRequest()
    payOfferRequest.setOfferId(offerId);
    console.log(payOfferRequest);

    client.payOffer(payOfferRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error paying offer: ' + err.message);
        return;
      }
      console.log(response);
      // goToProfilePage(response.getProfileId());
    });
  };

  // const goToProfilePage = (profileId) => {
  //   history.push("/app/profile/" + profileId);
  // };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'Offer ID:', offer.getOfferId());
    payOffer(offer.getOfferId());
    handleClose();
  }

  function OfferIdInput() {
    return (
      <TextField
        id="offerid-textarea"
        label="OfferId"
        required
        autoFocus
        value={offer.getOfferId()}
        fullWidth
        inputProps={{
           readOnly: true,
        }}
      />
    )
  }

  function CancelButton() {
    return (
      <Button
        onClick={handleClose}
        variant="contained"
        color="secondary"
      >
        Cancel
      </Button>
    )
  }

  function CloseChannelButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Close Channel
       </Button>
    )
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Buy Offer</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {OfferIdInput()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {CloseChannelButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
