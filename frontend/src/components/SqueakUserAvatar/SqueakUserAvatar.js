import React from 'react';

import HelpIcon from '@material-ui/icons/Help';
import Avatar from '@material-ui/core/Avatar';

import { useHistory } from 'react-router-dom';
import useStyles from './styles';

import {
  getProfileImageSrcString,
} from '../../squeakimages/images';
import {
  goToPubkeyPage,
} from '../../navigation/navigation';

export default function SqueakUserAvatar({
  squeakAddress,
  squeakProfile,
  ...props
}) {
  const history = useHistory();
  const classes = useStyles();

  const onAvatarClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling avatar click...');
    if (squeakAddress) {
      goToPubkeyPage(history, squeakAddress);
    }
  };

  function AvatarImage() {
    return (
      <Avatar className={classes.large} src={`${getProfileImageSrcString(squeakProfile)}`} />
    );
  }

  return (
    <div
      onClick={onAvatarClick}
      style={{ cursor: 'pointer' }}
    >
      {squeakProfile
        ? AvatarImage()
        : <HelpIcon className={classes.large} fontSize="large" />}
    </div>
  );
}
