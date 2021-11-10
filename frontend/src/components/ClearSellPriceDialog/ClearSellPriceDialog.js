import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControl,
  FormLabel,
  FormGroup,
  FormControlLabel,
  Switch,
  TextField,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  clearSellPriceRequest,
} from '../../squeakclient/requests';

export default function ClearSellPriceDialog({
  open,
  handleClose,
  reloadSellPriceFn,
  ...props
}) {
  const classes = useStyles();

  const clearSellPrice = () => {
    clearSellPriceRequest(() => {
      reloadSellPriceFn();
    });
  };


  function handleSubmit(event) {
    event.preventDefault();
    console.log('clear price msat');
    clearSellPrice();
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
        Clear Sell Price
      </Button>
    );
  }

  function SellPriceForm() {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Clear Sell Price</FormLabel>
      </FormControl>
    );
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Clear Sell Price</DialogTitle>
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
