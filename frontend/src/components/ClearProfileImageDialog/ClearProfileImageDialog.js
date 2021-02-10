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
  clearSqueakProfileImageRequest,
} from "../../squeakclient/requests"
import {
  reloadRoute,
} from "../../navigation/navigation"


export default function ClearProfileImageDialog({
  open,
  handleClose,
  squeakProfile,
  reloadProfile,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  const handleResponse = (response) => {
    reloadProfile();
  };

  const handleErr = (err) => {
    alert('Error clearing profile image: ' + err);
  };

  const clearProfileImage = () => {
    clearSqueakProfileImageRequest(
      squeakProfile.getProfileId(),
      handleResponse,
      handleErr,
    );
  };

  function handleSubmit(event) {
    event.preventDefault();
    clearProfileImage();
    handleClose();
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
    )
  }

  function ClearProfileImageButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Clear Profile Image
       </Button>
    )
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Clear Profile Image</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    Are you sure you want to clear the image for this profile?
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {ClearProfileImageButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
