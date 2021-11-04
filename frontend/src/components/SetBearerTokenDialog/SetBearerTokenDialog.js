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
  setTwitterBearerTokenRequest,
} from '../../squeakclient/requests';
import {
  goToProfilePage,
} from '../../navigation/navigation';

export default function SetBearerTokenDialog({
  open,
  handleClose,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const [bearerToken, setBearerToken] = useState('');

  const resetFields = () => {
    setBearerToken('');
  };

  const handleChangeBearerToken = (event) => {
    setBearerToken(event.target.value);
  };

  const handleResponse = (response) => {
    // goToProfilePage(history, response.getProfileId());
    // TODO
  };

  const handleErr = (err) => {
    alert(`Error setting bearer token: ${err}`);
  };

  const setBearerTokenRequest = (bearerToken) => {
    setTwitterBearerTokenRequest(bearerToken, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('bearerToken:', bearerToken);
    if (!bearerToken) {
      alert('Bearer Token cannot be empty.');
      return;
    }
    setBearerTokenRequest(bearerToken);
    handleClose();
  }

  function SetBearerTokenInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Bearer Token"
        required
        autoFocus
        value={bearerToken}
        onChange={handleChangeBearerToken}
        fullWidth
        inputProps={{ maxLength: 256 }}
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

  function SetBearerTokenButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Set Bearer Token
      </Button>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Set Bearer Token</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {SetBearerTokenInput()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {SetBearerTokenButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
