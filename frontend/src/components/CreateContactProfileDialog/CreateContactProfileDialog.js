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
  createContactProfileRequest,
} from '../../squeakclient/requests';
import {
  goToProfilePage,
} from '../../navigation/navigation';

export default function CreateContactProfileDialog({
  open,
  handleClose,
  initialPubkey = '',
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const [profileName, setProfileName] = useState('');
  const [pubkey, setPubkey] = useState(initialPubkey);

  const resetFields = () => {
    setProfileName('');
    setPubkey(initialPubkey);
  };

  const handleChangeProfileName = (event) => {
    setProfileName(event.target.value);
  };

  const handleChangePubkey = (event) => {
    setPubkey(event.target.value);
  };

  const handleResponse = (response) => {
    goToProfilePage(history, response.getProfileId());
  };

  const handleErr = (err) => {
    alert(`Error creating contact profile: ${err}`);
  };

  const createContactProfile = (profileName, squeakPubkey) => {
    createContactProfileRequest(profileName, squeakPubkey, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('profileName:', profileName);
    console.log('pubkey:', pubkey);
    if (!profileName) {
      alert('Profile Name cannot be empty.');
      return;
    }
    if (!pubkey) {
      alert('Pubkey Name cannot be empty.');
      return;
    }
    createContactProfile(profileName, pubkey);
    handleClose();
  }

  function CreateContactProfileNameInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Profile Name"
        variant="outlined"
        required
        autoFocus
        value={profileName}
        onChange={handleChangeProfileName}
        fullWidth
        margin="normal"
        inputProps={{ maxLength: 64 }}
      />
    );
  }

  function CreateContactPubkeyInput() {
    return (
      <TextField
        required
        id="standard-textarea"
        label="Pubkey"
        variant="outlined"
        margin="normal"
        value={pubkey}
        onChange={handleChangePubkey}
        inputProps={{ maxLength: 66 }}
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

  function CreateContactProfilButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Create Contact Profile
      </Button>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Create Contact Profile</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {CreateContactProfileNameInput()}
          {CreateContactPubkeyInput()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {CreateContactProfilButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
