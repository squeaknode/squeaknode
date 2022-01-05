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
  CircularProgress,
  FormControlLabel,
  Switch,
  Typography,
} from '@material-ui/core';

import { useHistory } from 'react-router-dom';

// styles
import useStyles from './styles';

import SqueakThreadItem from '../SqueakThreadItem';

import {
  makeSqueakRequest,
  getSigningProfilesRequest,
  getProfilesRequest,
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
  const [profiles, setProfiles] = useState([]);
  const [isPrivate, setIsPrivate] = useState(false);
  const [recipientProfileId, setrecipientProfileId] = useState(-1);
  const [loading, setLoading] = useState(false);

  const resetFields = () => {
    setProfileId(-1);
    setContent('');
    setIsPrivate(false);
  };

  const handleChange = (event) => {
    setProfileId(event.target.value);
  };

  const handleChangeContent = (event) => {
    setContent(event.target.value);
  };

  const handleChangeIsPrivate = (event) => {
    if (!event.target.checked) {
      setrecipientProfileId(-1);
    }
    setIsPrivate(event.target.checked);
  };

  const handleChangeRecipient = (event) => {
    setrecipientProfileId(event.target.value);
  };

  const handleResponse = (response) => {
    setLoading(false);
    handleClose();
    goToSqueakPage(history, response.getSqueakHash());
  };

  const handleErr = (err) => {
    setLoading(false);
    handleClose();
    alert(`Error making squeak: ${err}`);
  };

  const createSqueak = (profileId, content, replyto, recipientProfileId) => {
    const hasRecipient = recipientProfileId !== -1;
    setLoading(true);
    makeSqueakRequest(profileId, content, replyto, hasRecipient, recipientProfileId, handleResponse, handleErr);
  };
  const loadSigningProfiles = () => {
    getSigningProfilesRequest(setSigningProfiles);
  };
  const loadProfiles = () => {
    getProfilesRequest(setProfiles);
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
    if (isPrivate && recipientProfileId === -1) {
      alert('Recipient profile must be selected for a private squeak.');
      return;
    }
    createSqueak(profileId, content, replyto, recipientProfileId);
  }

  function load(event) {
    loadSigningProfiles();
    loadProfiles();
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
          variant="outlined"
          margin="normal"
          value={profileId}
          onChange={handleChange}
        >
          {signingProfiles.map((p) => <MenuItem key={p.getProfileId()} value={p.getProfileId()}>{p.getProfileName()}</MenuItem>)}
        </Select>
      </FormControl>
    );
  }

  function MakeSelectIsPrivate() {
    return (
      <FormControlLabel
        className={classes.formControlLabel}
        control={(
          <Switch
            checked={isPrivate}
            onChange={handleChangeIsPrivate}
            name="is-private-squeak"
            size="small"
          />
        )}
        label="Private Squeak"
      />
    );
  }

  function MakeSelectRecipientProfile() {
    return (
      <FormControl className={classes.formControl} required style={{ minWidth: 120 }}>
        <InputLabel id="demo-simple-select-label">Recipient Profile</InputLabel>
        <Select
          labelId="recipient-profile-select-label"
          id="recipient-profile-select"
          variant="outlined"
          margin="normal"
          value={recipientProfileId}
          onChange={handleChangeRecipient}
        >
          {profiles.map((p) => <MenuItem key={p.getProfileId()} value={p.getProfileId()}>{p.getProfileName()}</MenuItem>)}
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
        variant="outlined"
        margin="normal"
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

  function ContentLimitDisplay() {
    return (
      <Typography variant="caption">
       {content.length} / 280
      </Typography>
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
      <div className={classes.wrapper}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
        >
          Make Squeak
        </Button>
        {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
      </div>
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
          {ContentLimitDisplay()}
        </DialogContent>
        <DialogContent>
          {MakeSelectIsPrivate()}
          {isPrivate && MakeSelectRecipientProfile()}
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
          {MakeSqueakButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
