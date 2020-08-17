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

import {
  DeleteSqueakProfileRequest,
} from "../../proto/squeak_admin_pb"
import { client } from "../../squeakclient/squeakclient"


export default function DeleteProfileDialog({
  open,
  handleClose,
  profile,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  const deleteProfile = (profileId) => {
    console.log("called deleteSqueak");

    var deleteSqueakProfileRequest = new DeleteSqueakProfileRequest()
    deleteSqueakProfileRequest.setProfileId(profileId);
    console.log(deleteSqueakProfileRequest);

    client.deleteSqueakProfile(deleteSqueakProfileRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error deleting profile: ' + err.message);
        return;
      }

      console.log(response);
      reloadRoute();
    });
  };

  const reloadRoute = () => {
    history.go(0);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'profile:', profile);
    var profileId = profile.getProfileId();
    console.log( 'profileId:', profileId);
    deleteProfile(profileId);
    handleClose();
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

  function DeleteProfileButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
        Delete Profile
       </Button>
    )
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Delete Profile</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    Are you sure you want to delete this profile?
  </DialogContent>
  <DialogActions>
    {MakeCancelButton()}
    {DeleteProfileButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
