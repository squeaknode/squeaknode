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

import {
  goToProfilePage,
} from '../../navigation/navigation';

export default function ProfileListItem({
  profile,
  ...props
}) {
  const classes = useStyles({
    clickable: true,
  });

  const history = useHistory();

  const onProfileClick = (event) => {
    event.preventDefault();
    console.log('Handling profile click...');
    const profileId = profile.getProfileId();
    // const host = getPeerHost();
    // const port = getPeerPort();
    goToProfilePage(history, profileId);
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

  const name = profile.getProfileName();
  const address = profile.getAddress();

  function ProfileCardContent() {
    return (
      <>
        <Box>
          {profile.getHasPrivateKey() && <VpnKeyIcon />}
        </Box>
        <Box>
          {`Address: ${address}`}
        </Box>
        <SqueakProfileFollowingIndicator
          squeakProfile={profile}
        />
      </>
    );
  }

  return (
    <Card
      className={classes.root}
      onClick={onProfileClick}
    >
      <CardHeader
        avatar={(
          <SqueakUserAvatar
            squeakProfile={profile}
          />
)}
        title={`Name: ${name}`}
        subheader={ProfileCardContent()}
      />
    </Card>
  );
}
