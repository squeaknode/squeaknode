import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import {
  CircularProgress,
  CardHeader,
  Card,
} from '@material-ui/core';

// styles
import useStyles from './styles';

// components
import SavedPeerDetailItem from '../../components/SavedPeerDetailItem';

import {
  getPeerRequest,
} from '../../squeakclient/requests';

export default function PeerPage() {
  const classes = useStyles();
  const { id } = useParams();
  const [peerResp, setPeerResp] = useState(null);

  const handleGetSqueakPeerErr = (err) => {
    setPeerResp(null);
  };

  const getSqueakPeer = useCallback(() => {
    getPeerRequest(id, (resp => {
      setPeerResp(resp);
    }), handleGetSqueakPeerErr);
  },
  [id]);

  useEffect(() => {
    getSqueakPeer(id);
  }, [getSqueakPeer, id]);

  const handleReloadPeer = () => {
    getSqueakPeer(id);
  };

  function PeerContent() {
    return (
      <>
      {peerResp.getSqueakPeer()
        ? SqueakPeerDisplay()
        : NoSqueakPeerDisplay()}
      </>
    );
  }

  function SqueakPeerDisplay() {
    return (
      <SavedPeerDetailItem
        savedPeer={peerResp.getSqueakPeer()}
        handleReloadPeer={handleReloadPeer}
      />
    );
  }

  function NoSqueakPeerDisplay() {
    return (
      <Card
        className={classes.root}
      >
        <CardHeader
          subheader="Peer not found."
        />
      </Card>
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
        ? PeerContent()
        : WaitingIndicator()}
    </>
  );
}
