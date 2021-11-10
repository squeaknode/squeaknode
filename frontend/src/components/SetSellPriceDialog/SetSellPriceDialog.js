import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControl,
  FormLabel,
  TextField,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  setSellPriceRequest,
} from '../../squeakclient/requests';

export default function SetSellPriceDialog({
  open,
  handleClose,
  reloadSellPriceFn,
  ...props
}) {
  const classes = useStyles();
  const [sellPriceMsat, setSellPriceMsat] = useState(0);


  const setSellPrice = (priceMsat) => {
    setSellPriceRequest(priceMsat, () => {
      reloadSellPriceFn();
    });
  };

  // const setUseCustomPrice = (id, useCustomPrice) => {
  //   setSqueakProfileUseCustomPriceRequest(id, useCustomPrice, () => {
  //     reloadProfile();
  //   });
  // };
  //
  // const setCustomPriceMsat = (id, customPriceMsat) => {
  //   setSqueakProfileCustomPriceRequest(id, customPriceMsat, () => {
  //     reloadProfile();
  //   });
  // };

  // const handleSettingsFollowingChange = (event) => {
  //   console.log(`Following changed for profile id: ${squeakProfile.getProfileId()}`);
  //   console.log(`Following changed to: ${event.target.checked}`);
  //   setFollowing(squeakProfile.getProfileId(), event.target.checked);
  // };
  //
  // const handleSettingsUseCustomPriceChange = (event) => {
  //   console.log(`UseCustomPrice changed for profile id: ${squeakProfile.getProfileId()}`);
  //   console.log(`UseCustomPrice changed to: ${event.target.checked}`);
  //   setUseCustomPrice(squeakProfile.getProfileId(), event.target.checked);
  // };

  const handlePriceMsatChange = (event) => {
    console.log(`Price changed:`);
    const newPriceMsat = event.target.value;
    console.log(`Price changed to: ${newPriceMsat}`);
    setSellPriceMsat(newPriceMsat);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('sell price msat:', sellPriceMsat);
    if (!sellPriceMsat) {
      alert('Sell price cannot be empty.');
      return;
    }
    setSellPrice(sellPriceMsat);
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
    );
  }

  function SubmitButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Set Sell Price
      </Button>
    );
  }

  function SellPriceForm() {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Set Sell Price</FormLabel>
        <TextField
          required
          id="standard-required"
          label="Price (msats)"
          type="number"
          defaultValue={0}
          onChange={handlePriceMsatChange}
        />
      </FormControl>
    );
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Sell Price</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {SellPriceForm()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {SubmitButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
