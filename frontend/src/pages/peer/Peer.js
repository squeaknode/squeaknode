import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import {
  Grid,
  FormLabel,
  FormControl,
  FormGroup,
  FormControlLabel,
  Switch,
  Button,
  CircularProgress,
} from '@material-ui/core';

// styles
import useStyles from './styles';

// components
import PageTitle from '../../components/PageTitle';
import DeletePeerDialog from '../../components/DeletePeerDialog';

import {
  getPeerRequest,
  setPeerAutoconnectRequest,
  setPeerShareForFreeRequest,
} from '../../squeakclient/requests';
import {
  goToPeerAddressPage,
} from '../../navigation/navigation';

export default function PeerPage() {
  const classes = useStyles();
  const history = useHistory();
  const { id } = useParams();
  const [peer, setPeer] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [waitingForPeer, setWaitingForPeer] = useState(false);

  const getSqueakPeer = (id) => {
    setWaitingForPeer(true);
    getPeerRequest(id, (peer => {
      setWaitingForPeer(false);
      setPeer(peer);
    }));
  };
  const setAutoconnect = (id, autoconnect) => {
    setPeerAutoconnectRequest(id, autoconnect, () => {
      getSqueakPeer(id);
    });
  };
  const setShareForFree = (id, shareForFree) => {
    setPeerShareForFreeRequest(id, shareForFree, () => {
      getSqueakPeer(id);
    });
  };

  useEffect(() => {
    getSqueakPeer(id);
  }, [id]);

  const handleClickOpenDeleteDialog = () => {
    setDeleteDialogOpen(true);
    console.log(`deleteDialogOpen: ${deleteDialogOpen}`);
  };

  const handleCloseDeleteDialog = () => {
    setDeleteDialogOpen(false);
  };

  const handleSettingsAutoconnectChange = (event) => {
    console.log(`Autoconnect changed for peer id: ${id}`);
    console.log(`Autoconnect changed to: ${event.target.checked}`);
    setAutoconnect(id, event.target.checked);
  };

  const handleSettingsShareForFreeChange = (event) => {
    console.log(`share_for_free changed for peer id: ${id}`);
    console.log(`share_for_free changed to: ${event.target.checked}`);
    setShareForFree(id, event.target.checked);
  };

  const peerAddressToStr = (peerAddress) => `${peerAddress.getHost()}:${peerAddress.getPort()}`;

  function PeerContent() {
    return (
      <>
      {peer
        ? PeerDisplay()
        : NoPeerDisplay()}
      </>
    );
  }

  function NoPeerDisplay() {
    return (
      <p>
        No peer loaded
      </p>
    );
  }

  function PeerDisplay() {
    return (
      <>
        <p>
          Peer name:
          {' '}
          {peer.getPeerName()}
        </p>
        <p>
          {PeerAddressContent()}
        </p>
        {PeerSettingsForm()}
        {DeletePeerButton()}
      </>
    );
  }

  function PeerSettingsForm() {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Peer settings</FormLabel>
        <FormGroup>
          <FormControlLabel
            control={<Switch checked={peer.getAutoconnect()} onChange={handleSettingsAutoconnectChange} />}
            label="Autoconnect"
          />
          <FormControlLabel
            control={<Switch checked={peer.getShareForFree()} onChange={handleSettingsShareForFreeChange} />}
            label="Share For Free"
          />
        </FormGroup>
      </FormControl>
    );
  }

  function DeletePeerButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickOpenDeleteDialog();
              }}
            >
              Delete Peer
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function DeletePeerDialogContent() {
    return (
      <>
        <DeletePeerDialog
          open={deleteDialogOpen}
          handleClose={handleCloseDeleteDialog}
          peer={peer}
        />
      </>
    );
  }

  function PeerAddressContent() {
    console.log(peer.getPeerAddress());
    console.log(peer.getPeerAddress().getNetwork());
    const peerAddressStr = peerAddressToStr(peer.getPeerAddress());
    const network = peer.getPeerAddress().getNetwork();
    return (
      <>
        <div className={classes.root}>
          Peer Address:
          <Button
            variant="contained"
            onClick={() => {
              goToPeerAddressPage(
                history,
                peer.getPeerAddress().getNetwork(),
                peer.getPeerAddress().getHost(),
                peer.getPeerAddress().getPort(),
              );
            }}
          >
            {peerAddressStr}
          </Button>
        </div>
        <div className={classes.root}>
          Network:
          {' '}
          {network}
        </div>
      </>
    );
  }

  function WaitingIndicator() {
    return (
      <CircularProgress size={48} className={classes.buttonProgress} />
    );
  }

  return (
    <>
      {!waitingForPeer
        ? (
          <>
            <PageTitle title={`Peer: ${peer ? peer.getPeerName() : null}`} />
            {PeerContent()}
          </>
        )
        : WaitingIndicator()}
      {DeletePeerDialogContent()}
    </>
  );
}
