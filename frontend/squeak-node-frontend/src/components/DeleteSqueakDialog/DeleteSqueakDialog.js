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
  DeleteSqueakRequest,
} from "../../proto/squeak_admin_pb"
import {SqueakAdminClient} from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function DeleteSqueakDialog({
  open,
  handleClose,
  squeakToDelete,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  const deleteSqueak = (squeakHash) => {
    console.log("called deleteSqueak");

    var deleteSqueakRequest = new DeleteSqueakRequest()
    deleteSqueakRequest.setSqueakHash(squeakHash);
    console.log(deleteSqueakRequest);

    client.deleteSqueak(deleteSqueakRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error deleting squeak: ' + err.message);
        return;
      }

      console.log(response);
      reloadRoute();
    });
  };

  const goToSqueakPage = (squeakHash) => {
    history.push("/app/squeak/" + squeakHash);
  };

  const reloadRoute = () => {
    history.go(0);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'squeakToDelete:', squeakToDelete);
    var squeakHash = squeakToDelete.getSqueakHash();
    console.log( 'squeakHash:', squeakHash);
    deleteSqueak(squeakHash);
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

  function DeleteSqueakButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
        Delete Squeak
       </Button>
    )
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Make Squeak</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    Are you sure you want to delete this squeak?
  </DialogContent>
  <DialogActions>
    {MakeCancelButton()}
    {DeleteSqueakButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
