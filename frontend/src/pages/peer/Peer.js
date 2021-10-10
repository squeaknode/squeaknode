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
} from '@material-ui/core';

// styles
import useStyles from './styles';

// components
import PageTitle from '../../components/PageTitle';
import DeletePeerDialog from '../../components/DeletePeerDialog';

import {
  getPeerRequest,
  setPeerAutoconnectRequest,
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

  const getSqueakPeer = (id) => {
    getPeerRequest(id, setPeer);
  };
  const setAutoconnect = (id, autoconnect) => {
    setPeerAutoconnectRequest(id, autoconnect, () => {
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

  const peerAddressToStr = (peerAddress) => `${peerAddress.getHost()}:${peerAddress.getPort()}`;
  const peerUseTorToStr = (peerAddress) => `${peerAddress.getUseTor()}`;

  function NoPeerContent() {
    return (
      <p>
        No peer loaded
      </p>
    );
  }

  function PeerContent() {
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
    console.log(peer.getPeerAddress().getUseTor());
    const peerAddressStr = peerAddressToStr(peer.getPeerAddress());
    const useTor = peerUseTorToStr(peer.getPeerAddress());
    return (
      <>
      <div className={classes.root}>
        Peer Address:
        <Button
          variant="contained"
          onClick={() => {
            goToPeerAddressPage(
              history,
              peer.getPeerAddress().getHost(),
              peer.getPeerAddress().getPort(),
              peer.getPeerAddress().getUseTor(),
            );
          }}
        >
          {peerAddressStr}
        </Button>
      </div>
      <div className={classes.root}>
        Use Tor: {useTor}
      </div>
      </>
    );
  }

  return (
    <>
      <PageTitle title={`Peer: ${peer ? peer.getPeerName() : null}`} />
      <div>
        {peer
          ? PeerContent()
          : NoPeerContent()}
      </div>
      {DeletePeerDialogContent()}
    </>
  );
}
