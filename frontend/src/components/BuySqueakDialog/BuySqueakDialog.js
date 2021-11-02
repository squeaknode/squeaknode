import React, { useState, useEffect, useCallback } from 'react';
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
  CircularProgress,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import BuyOfferDetailItem from '../BuyOfferDetailItem';
import DownloadInProgressDialog from '../../components/DownloadInProgressDialog';


import {
  downloadOffersRequest,
  getBuyOffersRequest,
  // subscribeBuyOffersRequest,
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

  const [selectedOfferId, setSelectedOfferId] = useState('');
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [waitingForDownloadOffers, setWaitingForDownloadOffers] = useState(false);

  const resetFields = () => {
    setSelectedOfferId('');
  };

  const handleChange = (event) => {
    setSelectedOfferId(event.target.value);
  };

  const loadOffers = useCallback(() => {
    getBuyOffersRequest(hash, setOffers);
  },
  [hash, setOffers]);
  // const subscribeOffers = useCallback(() => subscribeBuyOffersRequest(hash, (offer) => {
  //   setOffers((prevOffers) => prevOffers.concat([offer]));
  // }),
  // [hash, setOffers]);

  const handleDownloadOffers = () => {
    console.log(`downloadOffersRequest with hash: ${hash}`);
    setWaitingForDownloadOffers(true);
    console.log(`downloadOffersRequest with hash: ${hash}`);
    downloadOffersRequest(hash, (response) => {
      setWaitingForDownloadOffers(false);
      const downloadResult = response.getDownloadResult();
      const numPeers = downloadResult.getNumberPeers();
      const numDownloaded = downloadResult.getNumberDownloaded();
      if (numPeers === 0) {
        alert("Unable to download because zero connected peers.");
      } else {
        alert(`Downloaded ${numDownloaded} offers from ${numPeers} connected peers.`);
      }
      getBuyOffersRequest(hash, setOffers);
    });
  };

  const handleCloseOffersDownloadInProgressDialog = () => {
    setWaitingForDownloadOffers(false);
  };

  const handlePayResponse = (response) => {
    handlePaymentComplete();
    setLoading(false);
    handleClose();
  };

  const handlePayErr = (err) => {
    alert(`Payment failure: ${err}`);
    setLoading(false);
    handleClose();
  };

  const pay = (offerId) => {
    setLoading(true);
    payOfferRequest(offerId, handlePayResponse, handlePayErr);
  };

  const onDownloadClick = (event) => {
    event.preventDefault();
    console.log('Handling download click...');
    console.log(`downloadOffersRequest with hash: ${hash}`);
    // downloadOffers();
    handleDownloadOffers();
  };

  const getSelectedOffer = () => {
    let offer;
    for (offer of offers) {
      if (offer.getOfferId() === selectedOfferId) {
        return offer;
      }
    }
    return null;
  };

  const getPeerAddressText = (offer) => {
    const peerAddress = offer.getPeerAddress();
    return `${peerAddress.getHost()}:${peerAddress.getPort()}`;
  };

  useEffect(() => {
    loadOffers();
  }, [loadOffers]);
  // useEffect(() => {
  //   const stream = subscribeOffers();
  //   return () => stream.cancel();
  // }, [subscribeOffers, hash]);

  function handleSubmit(event) {
    event.preventDefault();
    console.log('selectedOfferId:', selectedOfferId);
    if (selectedOfferId === '') {
      alert('Offer must be selected.');
      return;
    }
    pay(selectedOfferId);
    // handleClose();
  }

  function cancel(event) {
    event.stopPropagation();
    handleClose();
  }

  function ignore(event) {
    event.stopPropagation();
  }

  function SelectOfferContent() {
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

  function SelectedOfferContentInput() {
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

  function CancelBuyButton() {
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

  function BuySqueakButton() {
    return (
      <div className={classes.wrapper}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
        >
          Buy Squeak
        </Button>
        {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
      </div>
    );
  }

  function OffersDownloadInProgressDialogContent() {
    return (
      <>
        <DownloadInProgressDialog
          open={waitingForDownloadOffers}
          handleClose={handleCloseOffersDownloadInProgressDialog}
        />
      </>
    );
  }

  return (
    <>
    <Dialog open={open} onEnter={resetFields} onClose={cancel} onClick={ignore} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">
        Buy Squeak
      </DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          <Box>
            {LoadOffersButton()}
          </Box>
          <Box>
            <Typography variant="body1" color="textSecondary" component="p">
              {offers.length}
              {' '}
              offers
            </Typography>
          </Box>
          <Box>
            {SelectOfferContent()}
          </Box>
          {SelectedOfferContentInput()}
        </DialogContent>
        <DialogActions>
          {CancelBuyButton()}
          {BuySqueakButton()}
        </DialogActions>
      </form>
    </Dialog>
    {OffersDownloadInProgressDialogContent()}
    </>
  );
}
