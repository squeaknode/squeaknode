import React, { useState } from 'react';
import {
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
  FormControl,
  InputLabel,
  Select,
} from '@material-ui/core';

import { useHistory } from 'react-router-dom';

// styles
import useStyles from './styles';

import SqueakThreadItem from '../SqueakThreadItem';

import {
  makeSqueakRequest,
  getSigningProfilesRequest,
  storeDefaultSigningProfileIdRequest,
} from '../../squeakclient/requests';
import {
  goToSqueakPage,
} from '../../navigation/navigation';

export default function MakeSqueakDialog({
  open,
  handleClose,
  replytoSqueak,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const [profileId, setProfileId] = useState(-1);
  const [content, setContent] = useState('');
  const [signingProfiles, setSigningProfiles] = useState([]);

  const resetFields = () => {
    setProfileId(-1);
    setContent('');
  };

  const handleChange = (event) => {
    setProfileId(event.target.value);
    storeDefaultSigningProfile(event.target.value);
  };

  const handleChangeContent = (event) => {
    setContent(event.target.value);
  };

  const handleResponse = (response) => {
    goToSqueakPage(history, response.getSqueakHash());
  };

  const handleErr = (err) => {
    alert(`Error making squeak: ${err}`);
  };

  const createSqueak = (profileId, content, replyto) => {
    makeSqueakRequest(profileId, content, replyto, handleResponse, handleErr);
  };
  const loadSigningProfiles = () => {
    getSigningProfilesRequest(setSigningProfiles);
  };

  const storeDefaultSigningProfile = (profileId) => {
    console.log(`MakeSqueakDialog > storeDefaultSigningProfile > profileId=${profileId}`);
    return storeDefaultSigningProfileIdRequest(profileId);
  };

  // useEffect(() => {
  //   loadSigningProfiles()
  // }, []);

  function handleSubmit(event) {
    event.preventDefault();
    console.log('profileId:', profileId);
    console.log('content:', content);
    const replyto = (replytoSqueak ? replytoSqueak.getSqueakHash() : null);
    console.log('replyto:', replyto);
    if (profileId === -1) {
      alert('Signing profile must be selected.');
      return;
    }
    if (!content) {
      alert('Content cannot be empty.');
      return;
    }
    createSqueak(profileId, content, replyto);
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

  function ReplySqueakContent() {
    return (
      <>
        <SqueakThreadItem
          hash={replytoSqueak.getSqueakHash()}
          squeak={replytoSqueak}
        />
      </>
    );
  }

  function MakeSelectSigningProfile() {
    return (
      <FormControl className={classes.formControl} required style={{ minWidth: 120 }}>
        <InputLabel id="demo-simple-select-label">Signing Profile</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={profileId}
          onChange={handleChange}
        >
          {signingProfiles.map((p) => <MenuItem key={p.getProfileId()} value={p.getProfileId()}>{p.getProfileName()}</MenuItem>)}
        </Select>
      </FormControl>
    );
  }

  function MakeSqueakContentInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Squeak content"
        placeholder="Enter squeak content here..."
        required
        autoFocus
        value={content}
        onChange={handleChangeContent}
        multiline
        rows={8}
        fullWidth
        inputProps={{ maxLength: 280 }}
      />
    );
  }

  function MakeCancelButton() {
    return (
      <Button
        onClick={cancel}
        variant="contained"
        color="secondary"
      >
        Cancel
      </Button>
    );
  }

  function MakeSqueakButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Make Squeak
      </Button>
    );
  }

  return (
    <Dialog open={open} onRendered={load} onEnter={resetFields} onClose={cancel} onClick={ignore} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Make Squeak</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {replytoSqueak
            ? ReplySqueakContent() : <></>}
          {MakeSelectSigningProfile()}
          {MakeSqueakContentInput()}
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
          {MakeSqueakButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
