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
  importSigningProfileRequest,
} from '../../squeakclient/requests';
import {
  goToProfilePage,
} from '../../navigation/navigation';

export default function ImportSigningProfileDialog({
  open,
  handleClose,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const [profileName, setProfileName] = useState('');
  const [privateKey, setPrivateKey] = useState('');

  const resetFields = () => {
    setProfileName('');
  };

  const handleChangeProfileName = (event) => {
    setProfileName(event.target.value);
  };

  const handleChangePrivateKey = (event) => {
    setPrivateKey(event.target.value);
  };

  const handleResponse = (response) => {
    goToProfilePage(history, response.getProfileId());
  };

  const handleErr = (err) => {
    alert(`Error creating contact profile: ${err}`);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('profileName:', profileName);
    console.log('privateKey:', privateKey);
    if (!profileName) {
      alert('Profile Name cannot be empty.');
      return;
    }
    if (!privateKey) {
      alert('Private Key cannot be empty.');
      return;
    }
    importSigningProfileRequest(profileName, privateKey, handleResponse, handleErr);
    handleClose();
  }

  function ImportSigningProfileNameInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Profile Name"
        required
        autoFocus
        value={profileName}
        onChange={handleChangeProfileName}
        fullWidth
        inputProps={{ maxLength: 64 }}
      />
    );
  }

  function ImportSigningProfilePrivateKeyInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Private Key"
        required
        autoFocus
        value={privateKey}
        onChange={handleChangePrivateKey}
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

  function ImportSigningProfilButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Import Signing Profile
      </Button>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Import Signing Profile</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {ImportSigningProfileNameInput()}
        </DialogContent>
        <DialogContent>
          {ImportSigningProfilePrivateKeyInput()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {ImportSigningProfilButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
