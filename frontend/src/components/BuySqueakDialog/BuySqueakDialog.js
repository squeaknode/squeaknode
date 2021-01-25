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
import BuyOfferItem from "../../components/BuyOfferItem";
import BuyOfferDetailItem from "../../components/BuyOfferDetailItem";

import {
  makeSqueakRequest,
  getSigningProfilesRequest,
} from "../../squeakclient/requests"
import {
  getBuyOffersRequest,
  syncSqueakRequest,
} from "../../squeakclient/requests"
import {
  payOfferRequest,
} from "../../squeakclient/requests"


export default function BuySqueakDialog({
  open,
  handleClose,
  hash,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [selectedOfferId, setSelectedOfferId] = useState(-1);
  const [offers, setOffers] = useState([]);

  const resetFields = () => {
    setSelectedOfferId(-1);
  };

  const handleChange = (event) => {
    setSelectedOfferId(event.target.value);
  };

  const handleResponse = (response) => {
    // Open pay confirmation dialog
  };

  const handleErr = (err) => {
    alert('Error paying offer: ' + err);
  };

  // const payOffer = (offerID) => {
  //   alert('Pay offer ID here: ' + offerID);
  //   pay(offer.getOfferId());
  // };

  const loadOffers = () => {
    getBuyOffersRequest(hash, setOffers);
  };

  const handlePayResponse = (response) => {
    // goToSqueakPage(offer.getSqueakHash());
    reloadRoute();
  };

  const handlePayErr = (err) => {
    alert('Payment failure: ' + err);
  };

  const pay = (offerId) => {
    payOfferRequest(offerId, handlePayResponse, handlePayErr);
  };

  const reloadRoute = () => {
    history.go(0);
  };

  const getSelectedOffer = () => {
    var offer;
    for (offer of offers) {
      if (offer.getOfferId() == selectedOfferId) {
        return offer;
      }
    }
    return null;
  };

  useEffect(() => {
    loadOffers()
  }, []);

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'selectedOfferId:', selectedOfferId);
    if (selectedOfferId == -1) {
      alert('Selected Offer Id must be selected.');
      return;
    }
    pay(selectedOfferId);
    handleClose();
  }

  function MakeSelectSigningProfile() {
    return (
      <FormControl className={classes.formControl} required style={{minWidth: 120}}>
        <InputLabel id="offer-select-label">Offer</InputLabel>
        <Select
          labelId="offer-select-label"
          id="offer-select"
          value={selectedOfferId}
          onChange={handleChange}
        >
          {offers.map(offer =>
            <MenuItem key={offer.getOfferId()} value={offer.getOfferId()}>
              {offer.getPeer().getPeerName()} ({offer.getPriceMsat()} msats)
            </MenuItem>
          )}
        </Select>
      </FormControl>
    )
  }

  function MakeSqueakContentInput() {
    var selectedOffer = getSelectedOffer();
    if (selectedOffer == null) {
      return <></>
    }
    return (
      <Box
        p={1}
        key={selectedOffer.getOfferId()}
        >
      <BuyOfferDetailItem
        key={selectedOffer.getOfferId()}
        offer={selectedOffer}>
      </BuyOfferDetailItem>
      </Box>
    )
  }

  function MakeCancelButton() {
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

  function MakeSqueakButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Buy Squeak
       </Button>
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Buy Squeak</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {MakeSelectSigningProfile()}
    {MakeSqueakContentInput()}
  </DialogContent>
  <DialogActions>
    {MakeCancelButton()}
    {MakeSqueakButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
