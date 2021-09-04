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
  initialAddress = '',
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const [profileName, setProfileName] = useState('');
  const [address, setAddress] = useState(initialAddress);

  const resetFields = () => {
    setProfileName('');
    setAddress(initialAddress);
  };

  const handleChangeProfileName = (event) => {
    setProfileName(event.target.value);
  };

  const handleChangeAddress = (event) => {
    setAddress(event.target.value);
  };

  const handleResponse = (response) => {
    goToProfilePage(history, response.getProfileId());
  };

  const handleErr = (err) => {
    alert(`Error creating contact profile: ${err}`);
  };

  const createContactProfile = (profileName, squeakAddress) => {
    createContactProfileRequest(profileName, squeakAddress, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('profileName:', profileName);
    console.log('address:', address);
    if (!profileName) {
      alert('Profile Name cannot be empty.');
      return;
    }
    if (!address) {
      alert('Address Name cannot be empty.');
      return;
    }
    createContactProfile(profileName, address);
    handleClose();
  }

  function CreateContactProfileNameInput() {
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

  function CreateContactAddressInput() {
    return (
      <TextField
        required
        id="standard-textarea"
        label="Address"
        value={address}
        onChange={handleChangeAddress}
        inputProps={{ maxLength: 35 }}
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
          {CreateContactAddressInput()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {CreateContactProfilButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
