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
  getSqueakProfilePrivateKey,
} from "../../squeakclient/requests"



export default function ExportPrivateKeyDialog({
  open,
  handleClose,
  profile,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [privateKey, setPrivateKey] = useState('');

  const resetFields = () => {
    setPrivateKey('');
  };

  const handleChangePrivateKey = (event) => {
    setPrivateKey(event.target.value);
  };

  const getPrivateKey = () => {
    var profileId = profile.getProfileId();
    getSqueakProfilePrivateKey(profileId, (response) => {
      setPrivateKey(response.getPrivateKey());
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    getPrivateKey();
  }

  function DisplayPrivateKey() {
    return (
      <TextField
        id="standard-textarea"
        label="private-key"
        required
        autoFocus
        value={privateKey}
        fullWidth
        inputProps={{
           readOnly: true,
        }}
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

  function ShowPrivateKeyButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Show private key
       </Button>
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Export Private Key</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {DisplayPrivateKey()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {ShowPrivateKeyButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
