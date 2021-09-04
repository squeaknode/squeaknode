import React, { useState } from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogTitle,
  DialogContent,
  FormControlLabel,
  Switch,
  TextField,
} from '@material-ui/core';

// styles
import { makeStyles } from '@material-ui/core/styles';

import {
  connectSqueakPeerRequest,
} from '../../squeakclient/requests';

const useStyles = makeStyles((theme) => ({
  form: {
    margin: 'auto',
    width: 'fit-content',
    '& .MuiDialogContent-root': {
      overflow: 'hidden',
    },
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
    },
    '& .MuiDialogActions-root': {
      padding: '1rem',
    },
  },
  formControlLabel: {
    position: 'absolute',
    left: '2rem',
  },
}));

const portDefaultValue = '0';

export default function ConnectPeerDialog({
  open,
  handleClose,
  ...props
}) {
  const classes = useStyles();

  const [peerName, setPeerName] = useState('');
  const [host, setHost] = useState('');
  const [port, setPort] = useState('');
  const [customPortChecked, setCustomPortChecked] = React.useState(false);

  const resetFields = () => {
    setPeerName('');
    setHost('');
    setPort(portDefaultValue);
    setCustomPortChecked(false);
  };

  const handleChangeHost = (event) => {
    setHost(event.target.value);
  };

  const handleChangeCustomPortChecked = (event) => {
    setPort(
      event.target.checked ? '' : portDefaultValue,
    );
    setCustomPortChecked(event.target.checked);
  };

  const handleChangePort = (event) => {
    setPort(event.target.value);
  };

  const connectPeer = (peerName, host, port) => {
    connectSqueakPeerRequest(host, port, (response) => {
      // goToPeerPage(history, response.getPeerId());
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('host:', host);
    console.log('port:', port);
    if (!host) {
      alert('Host cannot be empty.');
      return;
    }
    if (!port) {
      alert('Port cannot be empty.');
      return;
    }
    connectPeer(peerName, host, port);
    handleClose();
  }

  function ConnectHostInput() {
    return (
      <TextField
        required
        variant="outlined"
        label="Host"
        value={host}
        onChange={handleChangeHost}
        inputProps={{ maxLength: 128 }}
        margin="normal"
      />
    );
  }

  function ConnectPortInput() {
    return (
      <TextField
        required={customPortChecked}
        variant="outlined"
        label="Port"
        value={customPortChecked ? port : ''}
        onChange={handleChangePort}
        inputProps={{ maxLength: 8 }}
        disabled={!customPortChecked}
        margin="normal"
      />
    );
  }

  function CustomPortSwitch() {
    return (
      <FormControlLabel
        className={classes.formControlLabel}
        control={(
          <Switch
            checked={customPortChecked}
            onChange={handleChangeCustomPortChecked}
            name="use-custom-port"
            size="small"
          />
        )}
        label="Use custom port"
      />
    );
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
    );
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
    );
  }

  return (
    <Dialog
      open={open}
      onEnter={resetFields}
      onClose={handleClose}
      aria-labelledby="form-dialog-title"
      maxWidth="sm"
    >
      <DialogTitle id="form-dialog-title">
        Connect Peer
      </DialogTitle>
      <form
        className={classes.form}
        onSubmit={handleSubmit}
        noValidate
        autoComplete="off"
      >
        <DialogContent>
          {ConnectHostInput()}
          {ConnectPortInput()}
        </DialogContent>
        <DialogActions>
          {CustomPortSwitch()}
          {CancelButton()}
          {ConnectPeerButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
