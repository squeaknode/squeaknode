import React from 'react';

import TimelineDot from '@material-ui/lab/TimelineDot';

import HelpIcon from '@material-ui/icons/Help';
import Avatar from '@material-ui/core/Avatar';

import { useHistory } from 'react-router-dom';

import {
  getProfileImageSrcString,
} from '../../squeakimages/images';
import {
  goToSqueakAddressPage,
} from '../../navigation/navigation';

export default function SqueakUserAvatar({
  squeakProfile,
  ...props
}) {
  const history = useHistory();

  const onAvatarClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling avatar click...');
    if (squeakProfile) {
      goToSqueakAddressPage(history, squeakProfile.getAddress());
    }
  };

  function AvatarImage() {
    return (
      <Avatar src={`${getProfileImageSrcString(squeakProfile)}`} />
    );
  }

  return (
    <TimelineDot
      onClick={onAvatarClick}
      style={{ cursor: 'pointer' }}
    >
      {squeakProfile
        ? AvatarImage()
        : <HelpIcon fontSize="large" />}
    </TimelineDot>
  );
}
