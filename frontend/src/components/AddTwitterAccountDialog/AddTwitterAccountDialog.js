import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  addTwitterAccountRequest,
  getSigningProfilesRequest,
} from '../../squeakclient/requests';

export default function AddTwitterAccountDialog({
  open,
  handleClose,
  reloadAccountsFn,
  ...props
}) {
  const classes = useStyles();

  const [twitterHandle, setTwitterHandle] = useState('');
  const [bearerToken, setBearerToken] = useState('');
  const [profileId, setProfileId] = useState(-1);
  const [signingProfiles, setSigningProfiles] = useState([]);

  const resetFields = () => {
    setTwitterHandle('');
    setProfileId(-1);
  };

  const handleChangeTwitterHandle = (event) => {
    setTwitterHandle(event.target.value);
  };

  const handleChangeBearerToken = (event) => {
    setBearerToken(event.target.value);
  };

  const handleChangeProfileId = (event) => {
    setProfileId(event.target.value);
  };

  const handleResponse = (response) => {
    reloadAccountsFn();
  };

  const handleErr = (err) => {
    alert(`Error adding twitter account: ${err}`);
  };

  const addTwitterAccount = (twitterHandle, profileId, bearerToken) => {
    addTwitterAccountRequest(twitterHandle, profileId, bearerToken, handleResponse, handleErr);
  };

  const loadSigningProfiles = () => {
    getSigningProfilesRequest(setSigningProfiles);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('twitterHandle:', twitterHandle);
    console.log('profileId:', profileId);
    if (profileId === -1) {
      alert('Signing profile must be selected.');
      return;
    }
    if (!twitterHandle) {
      alert('twitterHandle cannot be empty.');
      return;
    }
    if (!bearerToken) {
      alert('bearerToken cannot be empty.');
      return;
    }
    addTwitterAccount(twitterHandle, profileId, bearerToken);
    handleClose();
  }

  function load(event) {
    loadSigningProfiles();
  }

  function cancel(event) {
    event.stopPropagation();
    handleClose();
  }

  function ignore(event) {
    event.stopPropagation();
  }

  function AccountHandleInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Twitter Handle"
        variant="outlined"
        margin="normal"
        required
        autoFocus
        value={twitterHandle}
        onChange={handleChangeTwitterHandle}
        fullWidth
        inputProps={{ maxLength: 128 }}
      />
    );
  }

  function BearerTokenInput() {
    return (
      <TextField
        id="standard-textarea-bearer-token"
        label="Bearer Token"
        variant="outlined"
        margin="normal"
        required
        value={bearerToken}
        onChange={handleChangeBearerToken}
        fullWidth
        inputProps={{ maxLength: 128 }}
      />
    );
  }

  function SelectSigningProfile() {
    return (
      <FormControl className={classes.formControl} required style={{ minWidth: 120 }}>
        <InputLabel id="demo-simple-select-label">Signing Profile</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          variant="outlined"
          margin="normal"
          value={profileId}
          onChange={handleChangeProfileId}
        >
          {signingProfiles.map((p) => <MenuItem key={p.getProfileId()} value={p.getProfileId()}>{p.getProfileName()}</MenuItem>)}
        </Select>
      </FormControl>
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

  function AddTwitterAccountButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Add Twitter Account
      </Button>
    );
  }

  return (
    <Dialog open={open} onRendered={load} onEnter={resetFields} onClose={cancel} onClick={ignore}  aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Add Twitter Account</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {AccountHandleInput()}
          {BearerTokenInput()}
          {SelectSigningProfile()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {AddTwitterAccountButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
