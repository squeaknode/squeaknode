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

import {MakeSqueakRequest, GetSigningProfilesRequest} from "../../proto/squeak_admin_pb"
import {SqueakAdminClient} from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function MakeSqueakDialog({
  open,
  handleClose,
  replyto,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [profileId, setProfileId] = useState(-1);
  var [content, setContent] = useState('');
  var [signingProfiles, setSigningProfiles] = useState([]);

  // local
  // var [moreButtonRef, setMoreButtonRef] = useState(null);
  // var [isMoreMenuOpen, setMoreMenuOpen] = useState(false);

  const handleChange = (event) => {
    setProfileId(event.target.value);
  };

  const handleChangeContent = (event) => {
    setContent(event.target.value);
  };

  const makeSqueak = (profileId, content, replyto) => {
    console.log("called makeSqueak");

    var makeSqueakRequest = new MakeSqueakRequest()
    makeSqueakRequest.setProfileId(profileId);
    makeSqueakRequest.setContent(content);
    makeSqueakRequest.setReplyto(replyto);
    console.log(makeSqueakRequest);

    client.makeSqueak(makeSqueakRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error making squeak: ' + err.message);
        return;
      }

      console.log(response);
      console.log(response.getSqueakHash());
      goToSqueakPage(response.getSqueakHash());
    });
  };
  const getSigningProfiles = () => {
    console.log("called getSigningProfiles");
    var getSigningProfilesRequest = new GetSigningProfilesRequest()
    client.getSigningProfiles(getSigningProfilesRequest, {}, (err, response) => {
      console.log(response);
      console.log(response.getSqueakProfilesList());
      setSigningProfiles(response.getSqueakProfilesList());
    });
  };

  useEffect(() => {
    getSigningProfiles()
  }, []);

  const goToSqueakPage = (squeakHash) => {
    history.push("/app/squeak/" + squeakHash);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'profileId:', profileId);
    console.log( 'content:', content);
    console.log( 'replyto:', replyto);
    if (profileId == -1) {
      alert('Signing profile must be selected.');
      return;
    }
    if (!content) {
      alert('Content cannot be empty.');
      return;
    }
    makeSqueak(profileId, content, replyto);
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
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Make Squeak</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
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
