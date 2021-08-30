import React, { useState, useEffect } from 'react';
import {
  MenuItem,
  Typography,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControl,
  InputLabel,
  Select,
} from '@material-ui/core';

import { useHistory } from 'react-router-dom';

// styles
import useStyles from './styles';

import BuyOfferDetailItem from '../BuyOfferDetailItem';

import {
  downloadOffersRequest,
  getBuyOffersRequest,
  subscribeBuyOffersRequest,
  payOfferRequest,
} from '../../squeakclient/requests';

export default function BuySqueakDialog({
  open,
  handleClose,
  handlePaymentComplete,
  hash,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const [selectedOfferId, setSelectedOfferId] = useState('');
  const [offers, setOffers] = useState([]);

  const resetFields = () => {
    setSelectedOfferId('');
  };

  const handleChange = (event) => {
    setSelectedOfferId(event.target.value);
  };

  const handleResponse = (response) => {
    // Open pay confirmation dialog
  };

  const handleErr = (err) => {
    alert(`Error paying offer: ${err}`);
  };

  // const payOffer = (offerID) => {
  //   alert('Pay offer ID here: ' + offerID);
  //   pay(offer.getOfferId());
  // };

  const loadOffers = () => {
    getBuyOffersRequest(hash, setOffers);
  };
  const subscribeOffers = () => {
    return subscribeBuyOffersRequest(hash, (offer) => {
      setOffers((prevOffers) => {
        return prevOffers.concat([offer]);
      });
    });
  };
  const downloadOffers = () => {
    console.log(`downloadOffersRequest with hash: ${hash}`);
    downloadOffersRequest(hash, (response) => {
      // Do nothing.
    });
  };

  const handlePayResponse = (response) => {
    handlePaymentComplete();
  };

  const handlePayErr = (err) => {
    alert(`Payment failure: ${err.message}`);
  };

  const pay = (offerId) => {
    payOfferRequest(offerId, handlePayResponse, handlePayErr);
  };

  const onDownloadClick = (event) => {
    event.preventDefault();
    console.log('Handling download click...');
    console.log(`downloadOffersRequest with hash: ${hash}`);
    downloadOffers();
  };

  const getSelectedOffer = () => {
    let offer;
    for (offer of offers) {
      if (offer.getOfferId() == selectedOfferId) {
        return offer;
      }
    }
    return null;
  };

  const getPeerAddressText = (offer) => {
    const peerAddress = offer.getPeerAddress();
    const host = peerAddress.getHost();
    return `${peerAddress.getHost()}:${peerAddress.getPort()}`;
  };

  useEffect(() => {
    loadOffers();
  }, []);
  useEffect(() => {
    const stream = subscribeOffers();
    return () => stream.cancel();
  }, [hash]);

  function handleSubmit(event) {
    event.preventDefault();
    console.log('selectedOfferId:', selectedOfferId);
    if (selectedOfferId == '') {
      alert('Offer must be selected.');
      return;
    }
    pay(selectedOfferId);
    handleClose();
  }

  function load(event) {
    //loadOffers();
    //subscribeOffers();
    downloadOffers();
  }

  function cancel(event) {
    event.stopPropagation();
    handleClose();
  }

  function ignore(event) {
    event.stopPropagation();
  }

  function MakeSelectSigningProfile() {
    return (
      <FormControl className={classes.formControl} required style={{ minWidth: 120 }}>
        <InputLabel id="offer-select-label">Offer</InputLabel>
        <Select
          labelId="offer-select-label"
          id="offer-select"
          value={selectedOfferId}
          onChange={handleChange}
        >
          {offers.map((offer) => (
            <MenuItem key={offer.getOfferId()} value={offer.getOfferId()}>
              {getPeerAddressText(offer)}
              {' '}
              (
              {offer.getPriceMsat() / 1000}
              {' '}
              sats)
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    );
  }

  function LoadOffersButton() {
    return (
      <Button
        variant="contained"
        onClick={onDownloadClick}
      >
        Re-download offers
      </Button>
    );
  }

  function MakeSqueakContentInput() {
    const selectedOffer = getSelectedOffer();
    if (selectedOffer == null) {
      return <></>;
    }
    return (
      <Box
        p={1}
      >
        <BuyOfferDetailItem
          offer={selectedOffer}
        />
      </Box>
    );
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
    );
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
    );
  }

  return (
    <Dialog open={open} onRendered={load} onEnter={resetFields} onClose={cancel} onClick={ignore} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Buy Squeak for hash {hash}</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          <Box>
            <Typography variant="body1" color="textSecondary" component="p">
              {offers.length}
              {' '}
              offers
            </Typography>
          </Box>
          <Box>
            {MakeSelectSigningProfile()}
          </Box>
          {MakeSqueakContentInput()}
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
          {MakeSqueakButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
