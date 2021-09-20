import React from 'react';
import { useHistory } from 'react-router-dom';

import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';

// icons
import ComputerIcon from '@material-ui/icons/Computer';

import useStyles from '../../pages/wallet/styles';

import {
  goToPeerAddressPage,
} from '../../navigation/navigation';

export default function PeerListItem({
  peer,
  ...props
}) {
  const classes = useStyles({
    clickable: true,
  });

  const history = useHistory();

  const onPeerClick = (event) => {
    event.preventDefault();
    console.log('Handling peer address click...');
    const host = peer.getPeerAddress().getHost();
    const port = peer.getPeerAddress().getPort();
    goToPeerAddressPage(history, host, port);
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

  const getConnectedPeerDisplayName = (peer) => {
    if (peer.getSavedPeer()) {
      return `Name: ${peer.getSavedPeer().getPeerName()}`;
    }
    return '';
  };

  return (
    <Card
      className={classes.root}
      onClick={onPeerClick}
    >
      <CardHeader
        avatar={<ComputerIcon />}
        title={getConnectedPeerDisplayName(peer)}
        subheader={`Address: ${peer.getPeerAddress().getHost()}:${peer.getPeerAddress().getPort()}`}
      />
    </Card>
  );
}
