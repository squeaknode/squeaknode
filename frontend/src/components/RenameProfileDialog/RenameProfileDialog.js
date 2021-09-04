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
  renameSqueakProfileRequest,
} from '../../squeakclient/requests';

export default function RenameProfileDialog({
  open,
  handleClose,
  profile,
  reloadProfile,
  ...props
}) {
  const classes = useStyles();

  const [profileName, setProfileName] = useState('');

  const resetFields = () => {
    setProfileName('');
  };

  const handleChangeProfileName = (event) => {
    setProfileName(event.target.value);
  };

  const handleResponse = (response) => {
    reloadProfile();
  };

  const handleErr = (err) => {
    alert(`Error renaming signing profile: ${err}`);
  };

  const renameSqueakProfile = (profileId, profileName) => {
    renameSqueakProfileRequest(profileId, profileName, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    const profileId = profile.getProfileId();
    console.log('profileId:', profileId);
    console.log('profileName:', profileName);
    if (!profileName) {
      alert('Profile Name cannot be empty.');
      return;
    }
    renameSqueakProfile(profileId, profileName);
    handleClose();
  }

  function RenameProfileNameInput() {
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

  function RenameProfilButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Rename Profile
      </Button>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Rename Profile</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {RenameProfileNameInput()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {RenameProfilButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
