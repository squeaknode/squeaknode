import React from 'react';
import { useHistory } from 'react-router-dom';

import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';

// icons
import ComputerIcon from '@material-ui/icons/Computer';
import CloudOff from '@material-ui/icons/CloudOff';

import useStyles from '../../pages/wallet/styles';

import {
  goToPeerPage,
} from '../../navigation/navigation';

export default function SavedPeerListItem({
  peer,
  isConnected,
  ...props
}) {
  const classes = useStyles({
    clickable: true,
  });

  const history = useHistory();

  const onPeerClick = (event) => {
    event.preventDefault();
    console.log('Handling peer click...');
    const peerId = peer.getPeerId();
    // const host = getPeerHost();
    // const port = getPeerPort();
    goToPeerPage(history, peerId);
  };

  // const getPeerHost = () => {
  //   const address = peer.getAddress();
  //   if (address == null) {
  //     return null;
  //   }
  //   const pieces = address.split(":");
  //   return pieces[0];
  // }
  //
  // const getPeerPort = () => {
  //   const address = peer.getAddress();
  //   if (address == null) {
  //     return null;
  //   }
  //   const pieces = address.split(":");
  //   if (pieces.length < 2) {
  //     return null;
  //   }
  //   return pieces[1];
  // }

  function SavedPeerIcon() {
    if (isConnected) {
      return (
        <ComputerIcon fontSize="large" style={{ fill: 'green' }} />
      );
    }
    return (
      <CloudOff fontSize="large" style={{ fill: 'red' }} />
    );
  }

  return (
    <Card
      className={classes.root}
      onClick={onPeerClick}
    >
      <CardHeader
        avatar={<SavedPeerIcon />}
        title={`Name: ${peer.getPeerName()}`}
        subheader={`Address: ${peer.getPeerAddress().getHost()}:${peer.getPeerAddress().getPort()}`}
      />
    </Card>
  );
}
