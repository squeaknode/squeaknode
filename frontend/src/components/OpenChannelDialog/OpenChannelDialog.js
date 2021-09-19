import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
  CircularProgress,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  lndOpenChannelSyncRequest,
} from '../../squeakclient/requests';

export default function OpenChannelDialog({
  open,
  pubkey,
  handleClose,
  ...props
}) {
  const classes = useStyles();

  const [amount, setAmount] = useState('');
  const [satperbyte, setSatperbyte] = useState('');
  const [loading, setLoading] = useState(false);

  const resetFields = () => {
    setAmount('');
    setSatperbyte('');
  };

  const handleChangeAmount = (event) => {
    setAmount(event.target.value);
  };

  const handleChangeSatPerBytes = (event) => {
    setSatperbyte(event.target.value);
  };

  const handleResponse = (response) => {
    // TODO: go to channel page instead of showing alert.
    setLoading(false);
    alert('Open channel pending.');
  };

  const handleErr = (err) => {
    setLoading(false);
    alert(`Error opening channel: ${err}`);
  };

  const openChannel = (pubkey, amount) => {
    setLoading(true);
    lndOpenChannelSyncRequest(pubkey, amount, satperbyte, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('pubkey:', pubkey);
    console.log('amount:', amount);
    console.log('satperbyte:', satperbyte);
    if (!amount) {
      alert('Amount cannot be empty.');
      return;
    }
    openChannel(pubkey, amount, satperbyte);
    handleClose();
  }

  function PubKeyInput() {
    return (
      <TextField
        id="pubkey-textarea"
        label="Node Pub Key"
        required
        autoFocus
        value={pubkey}
        fullWidth
        inputProps={{
          readOnly: true,
        }}
      />
    );
  }

  function LocalFundingAmountInput() {
    return (
      <TextField
        id="amount-textarea"
        label="Local Funding Amount"
        required
        autoFocus
        value={amount}
        onChange={handleChangeAmount}
        fullWidth
        inputProps={{ maxLength: 64 }}
      />
    );
  }

  function SatPerByteInput() {
    return (
      <TextField
        id="satperbyte-textarea"
        label="Sats Per Byte"
        required
        autoFocus
        value={satperbyte}
        onChange={handleChangeSatPerBytes}
        fullWidth
        inputProps={{ maxLength: 64 }}
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

  function OpenChannelButton() {
    return (
      <div className={classes.wrapper}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
        >
          Open Channel
        </Button>
        {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
      </div>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Open Channel</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {PubKeyInput()}
        </DialogContent>
        <DialogContent>
          {LocalFundingAmountInput()}
        </DialogContent>
        <DialogContent>
          {SatPerByteInput()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {OpenChannelButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
