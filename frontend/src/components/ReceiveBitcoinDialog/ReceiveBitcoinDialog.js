import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

// styles
import useStyles from './styles';

import {
  lndNewAddressRequest,
} from '../../squeakclient/requests';

export default function ReceiveBitcoinDialog({
  open,
  handleClose,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const [address, setAddress] = useState('');

  const resetFields = () => {
    setAddress('');
  };

  const handleChangeAddress = (event) => {
    setAddress(event.target.value);
  };

  const getNewAddress = () => {
    lndNewAddressRequest((response) => {
      setAddress(response.getAddress());
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    getNewAddress(address);
    // handleClose();
  }

  function ReceiveBitcoinAddess() {
    return (
      <TextField
        id="standard-textarea"
        label="Address"
        required
        autoFocus
        value={address}
        onChange={handleChangeAddress}
        fullWidth
        inputProps={{
          readOnly: true,
        }}
      />
    );
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

  function RenewAddressButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Get New Address
      </Button>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Receive Bitcoin</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {ReceiveBitcoinAddess()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {RenewAddressButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
