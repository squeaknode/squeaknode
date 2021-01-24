import React, {useState, useEffect} from 'react';
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField,
  DialogActions,
  Button,
  FormControl,
  InputLabel,
  Select,
} from "@material-ui/core";

import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";
import SqueakThreadItem from "../../components/SqueakThreadItem";

import {
  makeSqueakRequest,
  getSigningProfilesRequest,
} from "../../squeakclient/requests"
import {navigateTo, PROFILE_VIEW, SQUEAK_VIEW} from "../../navigation/routes";


export default function MakeSqueakDialog({
  open,
  handleClose,
  replytoSqueak,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [profileId, setProfileId] = useState(-1);
  var [content, setContent] = useState('');
  var [signingProfiles, setSigningProfiles] = useState([]);

  const resetFields = () => {
    setProfileId(-1);
    setContent('');
  };

  const handleChange = (event) => {
    setProfileId(event.target.value);
  };

  const handleChangeContent = (event) => {
    setContent(event.target.value);
  };

  const handleResponse = (response) => {
    navigateTo(history, SQUEAK_VIEW, [response.getSqueakHash()]);
  };

  const handleErr = (err) => {
    alert('Error making squeak: ' + err);
  };

  const createSqueak = (profileId, content, replyto) => {
    makeSqueakRequest(profileId, content, replyto, handleResponse, handleErr);
  };
  const loadSigningProfiles = () => {
    getSigningProfilesRequest(setSigningProfiles);
  };

  useEffect(() => {
    loadSigningProfiles()
  }, []);

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'profileId:', profileId);
    console.log( 'content:', content);
    if (replytoSqueak) {
      var replyto = replytoSqueak.getSqueakHash();
    } else {
      var replyto = null;
    }
    console.log( 'replyto:', replyto);
    if (profileId == -1) {
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

  function ReplySqueakContent() {
    return (
      <>
        <SqueakThreadItem
          hash={replytoSqueak.getSqueakHash()}
          squeak={replytoSqueak}>
        </SqueakThreadItem>
      </>
    )
  }

  function MakeSelectSigningProfile() {
    return (
      <FormControl className={classes.formControl} required style={{minWidth: 120}}>
        <InputLabel id="demo-simple-select-label">Signing Profile</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={profileId}
          onChange={handleChange}
        >
          {signingProfiles.map(p =>
            <MenuItem key={p.getProfileId()} value={p.getProfileId()}>{p.getProfileName()}</MenuItem>
          )}
        </Select>
      </FormControl>
    )
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
    )
  }

  function MakeCancelButton() {
    return (
      <Button
        onClick={handleClose}
        variant="contained"
        color="secondary"
      >
        Cancel
      </Button>
    )
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
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Make Squeak</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {replytoSqueak ?
      ReplySqueakContent() : <></>}
    {MakeSelectSigningProfile()}
    {MakeSqueakContentInput()}
  </DialogContent>
  <DialogActions>
    {MakeCancelButton()}
    {MakeSqueakButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
