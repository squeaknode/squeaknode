import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  getSqueakProfilePrivateKey,
} from '../../squeakclient/requests';

export default function ExportPrivateKeyDialog({
  open,
  handleClose,
  profile,
  ...props
}) {
  const classes = useStyles();

  const [privateKey, setPrivateKey] = useState('');

  const resetFields = () => {
    setPrivateKey('');
  };

  const handleChangePrivateKey = (event) => {
    setPrivateKey(event.target.value);
  };

  const getPrivateKey = () => {
    const profileId = profile.getProfileId();
    getSqueakProfilePrivateKey(profileId, (response) => {
      setPrivateKey(response.getPrivateKey());
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    getPrivateKey();
  }

  function DisplayPrivateKey() {
    return (
      <TextField
        id="standard-textarea"
        label="private-key"
        required
        autoFocus
        value={privateKey}
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

  function ShowPrivateKeyButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Show private key
      </Button>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Export Private Key</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {DisplayPrivateKey()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {ShowPrivateKeyButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
