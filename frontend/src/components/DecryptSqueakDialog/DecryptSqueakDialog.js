import React, { useState, useEffect, useCallback } from 'react';
import {
  MenuItem,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControl,
  InputLabel,
  Select,
  CircularProgress,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  getSigningProfilesRequest,
  // decryptSqueakRequest,
  decryptRequest,
} from '../../squeakclient/requests';

export default function DecryptSqueakDialog({
  open,
  handleClose,
  handleDecryptComplete,
  hash,
  squeak,
  ...props
}) {
  const classes = useStyles();

  const [profileId, setProfileId] = useState(-1);
  const [signingProfiles, setSigningProfiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const resetFields = () => {
    setProfileId('');
  };

  const handleChangeProfileId = (event) => {
    setProfileId(event.target.value);
  };

  const loadSigningProfiles = useCallback(() => {
    getSigningProfilesRequest(setSigningProfiles);
  },
  [setSigningProfiles]);

  const handleDecryptResponse = (response) => {
    handleDecryptComplete();
    setLoading(false);
    handleClose();
  };

  const handleDecryptErr = (err) => {
    alert(`Decryption failure: ${err}`);
    setLoading(false);
    handleClose();
  };

  const decrypt = (profileId) => {
    const hasRecipient = profileId !== -1;
    setLoading(true);
    decryptRequest(hash, null, -1, hasRecipient, profileId, handleDecryptResponse, handleDecryptErr);
  };

  useEffect(() => {
    loadSigningProfiles();
  }, [loadSigningProfiles]);

  function handleSubmit(event) {
    event.preventDefault();
    console.log('profileId:', profileId);
    if (profileId === '') {
      alert('Profile must be selected.');
      return;
    }
    decrypt(profileId);
    // handleClose();
  }

  function cancel(event) {
    event.stopPropagation();
    handleClose();
  }

  function ignore(event) {
    event.stopPropagation();
  }

  function SelectProfileContent() {
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

  function CancelDecryptButton() {
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

  function DecryptSqueakButton() {
    return (
      <div className={classes.wrapper}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
        >
          Decrypt Squeak
        </Button>
        {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
      </div>
    );
  }

  return (
    <>
    <Dialog open={open} onEnter={resetFields} onClose={cancel} onClick={ignore} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">
        Decrypt Squeak
      </DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          <Box>
            {SelectProfileContent()}
          </Box>
        </DialogContent>
        <DialogActions>
          {CancelDecryptButton()}
          {DecryptSqueakButton()}
        </DialogActions>
      </form>
    </Dialog>
    </>
  );
}
