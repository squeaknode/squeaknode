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
  Link,
} from '@material-ui/core';

// styles
import useStyles from './styles';

// components
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
  const [peerResp, setPeerResp] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  const getSqueakPeer = (id) => {
    getPeerRequest(id, (resp => {
      setPeerResp(resp);
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
      {peerResp.getSqueakPeer()
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
          {peerResp.getSqueakPeer().getPeerName()}
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
            control={<Switch checked={peerResp.getSqueakPeer().getAutoconnect()} onChange={handleSettingsAutoconnectChange} />}
            label="Autoconnect"
          />
          <FormControlLabel
            control={<Switch checked={peerResp.getSqueakPeer().getShareForFree()} onChange={handleSettingsShareForFreeChange} />}
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
          peer={peerResp.getSqueakPeer()}
        />
      </>
    );
  }

  function PeerAddressContent() {
    const peer = peerResp.getSqueakPeer();
    console.log(peer.getPeerAddress());
    console.log(peer.getPeerAddress().getNetwork());
    const peerAddressStr = peerAddressToStr(peer.getPeerAddress());
    return (
      <>
        <div className={classes.root}>
        <Link
          href="#"
          onClick={(event) => {
            event.preventDefault();
            goToPeerAddressPage(
              history,
              peer.getPeerAddress().getNetwork(),
              peer.getPeerAddress().getHost(),
              peer.getPeerAddress().getPort(),
            );
          }}        >
          {peerAddressStr}
        </Link>
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
      {peerResp
        ? (
          <>
            {PeerContent()}
            {DeletePeerDialogContent()}
          </>
        )
        : WaitingIndicator()}
    </>
  );
}
