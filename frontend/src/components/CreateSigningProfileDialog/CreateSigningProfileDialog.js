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
  createSigningProfileRequest,
} from '../../squeakclient/requests';
import {
  goToProfilePage,
} from '../../navigation/navigation';

export default function CreateSigningProfileDialog({
  open,
  handleClose,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const [profileName, setProfileName] = useState('');

  const resetFields = () => {
    setProfileName('');
  };

  const handleChangeProfileName = (event) => {
    setProfileName(event.target.value);
  };

  const handleResponse = (response) => {
    goToProfilePage(history, response.getProfileId());
  };

  const handleErr = (err) => {
    alert(`Error creating signing profile: ${err}`);
  };

  const createSigningProfile = (profileName) => {
    createSigningProfileRequest(profileName, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('profileName:', profileName);
    if (!profileName) {
      alert('Profile Name cannot be empty.');
      return;
    }
    createSigningProfile(profileName);
    handleClose();
  }

  function CreateSigningProfileNameInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Profile Name"
        variant="outlined"
        margin="normal"
        required
        autoFocus
        value={profileName}
        onChange={handleChangeProfileName}
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

  function CreateSigningProfilButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Create Signing Profile
      </Button>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Create Signing Profile</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {CreateSigningProfileNameInput()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {CreateSigningProfilButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
