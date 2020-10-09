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
  LightningAddress,
} from "../../proto/lnd_pb"
import {
  DeleteSqueakProfileRequest,
} from "../../proto/squeak_admin_pb"
import { client } from "../../squeakclient/squeakclient"


export default function ConnectPeerDialog({
  open,
  handleClose,
  peer,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  const connectPeer = (pubkey, host) => {
    console.log("called connectPeer");

    var connectPeerRequest = new ConnectPeerRequest()
    var address = new LightningAddress();
    address.setPubkey(pubkey);
    address.setHost(host);
    connectPeerRequest.setAddr(address);
    console.log(connectPeerRequest);

    client.connectPeer(connectPeerRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error connecting peer: ' + err.message);
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
    console.log( 'peer:', peer);
    var pubkey = profile.getPubKey();
    var address = profile.getAddress();
    console.log( 'pubkey:', pubkey);
    console.log( 'address:', address);
    deleteProfile(pubkey, address);
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

  function ConnectPeerButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
        Connect Peer
       </Button>
    )
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Connect Peer</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    Are you sure you want to delete this profile?
  </DialogContent>
  <DialogActions>
    {MakeCancelButton()}
    {ConnectPeerButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
