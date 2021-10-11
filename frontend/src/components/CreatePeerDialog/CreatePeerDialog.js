import React, { useState, useMemo } from 'react';
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
import { useHistory } from 'react-router-dom';

// styles
import { makeStyles } from '@material-ui/core/styles';

import {
  getDefaultPeerPortRequest,
  createPeerRequest,
} from '../../squeakclient/requests';
import {
  goToPeerPage,
} from '../../navigation/navigation';

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


export default function CreatePeerDialog({
  open,
  handleClose,
  initialNetwork = '',
  initialHost = '',
  initialPort = '',
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const [defaultPeerPort, setDefaultPeerPort] = useState(null);
  const [peerName, setPeerName] = useState('');
  const [host, setHost] = useState('');
  const [port, setPort] = useState('');
  const [customPortChecked, setCustomPortChecked] = useState(false);
  const [useTorChecked, setUseTorChecked] = useState(false);
  const portToUse = useMemo(() => customPortChecked ? port : defaultPeerPort,  [customPortChecked, port, defaultPeerPort]);

  const getDefaultPeerPort = () => {
    getDefaultPeerPortRequest(setDefaultPeerPort);
  };

  const resetFields = () => {
    setPeerName('');
    setHost('');
    if (initialNetwork === 'TORV3') {
      setUseTorChecked(true);
    }
    if (initialHost) {
      setHost(initialHost);
    }
    setPort('');
    setCustomPortChecked(false);
    if (initialPort) {
      setPort(initialPort);
      setCustomPortChecked(true);
    }
  };

  function load(event) {
    getDefaultPeerPort();
    resetFields();
  }

  const handleChangePeerName = (event) => {
    setPeerName(event.target.value);
  };

  const handleChangeHost = (event) => {
    setHost(event.target.value);
  };

  const handleChangeCustomPortChecked = (event) => {
    // setPort(
    //   event.target.checked ? '' : portDefaultValue,
    // );
    setPort('');
    setCustomPortChecked(event.target.checked);
  };

  const handleChangePort = (event) => {
    setPort(event.target.value);
  };

  const handleChangeUseTorChecked = (event) => {
    setUseTorChecked(event.target.checked);
  };

  const getNetwork = (useTor) => {
    if (useTor) {
      return "TORV3";
    } else {
      return "IPV4";
    }
  };

  const createPeer = (peerName, host, port) => {
    const network = getNetwork(useTorChecked);
    createPeerRequest(peerName, network, host, port, (response) => {
      goToPeerPage(history, response.getPeerId());
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('peerName:', peerName);
    console.log('host:', host);
    console.log('port:', port);
    if (!host) {
      alert('Host cannot be empty.');
      return;
    }
    if (!portToUse) {
      alert('portToUse cannot be empty.');
      return;
    }
    createPeer(peerName, host, portToUse);
    handleClose();
  }

  function CreatePeerNameInput() {
    return (
      <TextField
        required
        variant="outlined"
        label="Peer Name"
        autoFocus
        value={peerName}
        onChange={handleChangePeerName}
        fullWidth
        inputProps={{ maxLength: 64 }}
        margin="normal"
      />
    );
  }

  function CreateHostInput() {
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

  function CreatePortInput() {
    return (
      <TextField
        required={customPortChecked}
        variant="outlined"
        label="Port"
        value={portToUse}
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

  function UseTorSwitch() {
    return (
      <FormControlLabel
        className={classes.formControlLabel}
        control={(
          <Switch
            checked={useTorChecked}
            onChange={handleChangeUseTorChecked}
            name="use-tor"
            size="small"
          />
        )}
        label="Use Tor"
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
    );
  }

  return (
    <Dialog
      open={open}
      onEnter={load}
      onClose={handleClose}
      aria-labelledby="form-dialog-title"
      maxWidth="sm"
    >
      <DialogTitle id="form-dialog-title">
        Create Peer
      </DialogTitle>
      <form
        className={classes.form}
        onSubmit={handleSubmit}
        noValidate
        autoComplete="off"
      >
        <DialogContent>
          {CreatePeerNameInput()}
          {CreateHostInput()}
          {CreatePortInput()}
        </DialogContent>
        <DialogActions>
          {CustomPortSwitch()}
        </DialogActions>
        <DialogActions>
          {UseTorSwitch()}
        </DialogActions>
        <DialogActions>
          {CancelButton()}
          {CreatePeerButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
