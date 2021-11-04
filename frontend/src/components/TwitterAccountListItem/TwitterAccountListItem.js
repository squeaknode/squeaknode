import React from 'react';
import { useHistory } from 'react-router-dom';

import Card from '@material-ui/core/Card';
import Box from '@material-ui/core/Box';
import CardHeader from '@material-ui/core/CardHeader';

// icons
import VpnKeyIcon from '@material-ui/icons/VpnKey';

import useStyles from '../../pages/wallet/styles';
import SqueakUserAvatar from '../SqueakUserAvatar';
import SqueakProfileFollowingIndicator from '../SqueakProfileFollowingIndicator';


export default function TwitterAccountListItem({
  accountEntry,
  ...props
}) {
  const classes = useStyles({
    clickable: true,
  });

  // const onProfileClick = (event) => {
  //   event.preventDefault();
  //   console.log('Handling profile click...');
  //   const profileId = profile.getProfileId();
  //   // const host = getPeerHost();
  //   // const port = getPeerPort();
  //   goToProfilePage(history, profileId);
  // };

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

  const twitterHandle = accountEntry.getHandle();
  const profile = accountEntry.getProfile();

  function AccountCardContent() {
    const name = profile.getProfileName();
    const address = profile.getAddress();
    return (
      <>
        <Box>
          {`Profile Name: ${name}`}
        </Box>
        <Box>
          {`Address: ${address}`}
        </Box>
      </>
    );
  }

  return (
    <Card
      className={classes.root}
      // onClick={alert('do something')}
    >
      <CardHeader
        avatar={(
          <SqueakUserAvatar
            squeakAddress={(profile && profile.getAddress())}
            squeakProfile={profile}
          />
)}
        title={`Twitter handle: ${twitterHandle}`}
        subheader={AccountCardContent()}
      />
    </Card>
  );
}
