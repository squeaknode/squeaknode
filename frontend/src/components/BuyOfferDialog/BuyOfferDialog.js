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
  payOfferRequest,
} from "../../squeakclient/requests"
import {navigateTo, SQUEAK_VIEW} from "../../navigation/routes";


export default function BuyOfferDialog({
  open,
  offer,
  handleClose,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  const handleResponse = (response) => {
    navigateTo(history, SQUEAK_VIEW, [offer.getSqueakHash()]);
  };

  const handleErr = (err) => {
    alert('Payment failure: ' + err);
  };

  const pay = (offerId) => {
    payOfferRequest(offerId, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'Offer ID:', offer.getOfferId());
    pay(offer.getOfferId());
    handleClose();
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

  function PayOfferButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Pay
       </Button>
    )
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Buy Offer</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    Are you sure you want to pay {offer.getPriceMsat() / 1000} satoshis for this offer?
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {PayOfferButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
