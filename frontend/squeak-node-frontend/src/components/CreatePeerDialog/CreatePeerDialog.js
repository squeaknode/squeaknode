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
  CreatePeerRequest,
} from "../../proto/squeak_admin_pb"
import {SqueakAdminClient} from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function CreatePeerDialog({
  open,
  handleClose,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [peerName, setpeerName] = useState('');
  var [host, setHost] = useState('');
  var [port, setPort] = useState('');

  const handleChangePeerName = (event) => {
    setpeerName(event.target.value);
  };

  const handleChangeHost = (event) => {
    setHost(event.target.value);
  };

  const handleChangePort = (event) => {
    setPort(event.target.value);
  };

  const createPeer = (peerName, host, port) => {
    console.log("called createPeer");

    var createPeerRequest = new CreatePeerRequest()
    createPeerRequest.setPeerName(peerName);
    createPeerRequest.setHost(host);
    createPeerRequest.setPort(port);
    console.log(createPeerRequest);

    client.createPeer(createPeerRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error creating peer: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getPeerId());
      // goToProfilePage(response.getProfileId());
    });
  };

  const goToProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'peerName:', peerName);
    console.log( 'host:', host);
    console.log( 'port:', port);
    if (!host) {
      alert('Host cannot be empty.');
      return;
    }
    if (!port) {
      alert('Port cannot be empty.');
      return;
    }
    createPeer(peerName, host, port);
    handleClose();
  }

  function CreatePeerNameInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Peer Name"
        autoFocus
        value={peerName}
        onChange={handleChangePeerName}
        fullWidth
        inputProps={{ maxLength: 64 }}
      />
    )
  }

  function CreateHostInput() {
    return (
      <TextField required
          id="standard-textarea"
          label="Host"
          required
          value={host}
          onChange={handleChangeHost}
          inputProps={{ maxLength: 128 }}
      />
    )
  }

  function CreatePortInput() {
    return (
      <TextField required
          id="standard-textarea"
          label="Port"
          required
          value={port}
          onChange={handleChangePort}
          inputProps={{ maxLength: 8 }}
      />
    )
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

  function CreatePeerButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Create Peer
       </Button>
    )
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Create Peer</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    <div>
      {CreatePeerNameInput()}
    </div>
    <div>
      {CreateHostInput()}
    </div>
    <div>
      {CreatePortInput()}
    </div>
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {CreatePeerButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
