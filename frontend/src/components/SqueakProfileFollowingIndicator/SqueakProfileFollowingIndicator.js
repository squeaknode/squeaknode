import React from 'react';
import {
  Typography,
} from '@material-ui/core';

import NotificationsActiveIcon from '@material-ui/icons/NotificationsActive';
import NotificationsNoneIcon from '@material-ui/icons/NotificationsNone';

export default function SqueakProfileFollowingIndicator({
  squeakProfile,
  ...props
}) {

  function FollowingIndicator() {
    return (
      <>
        <Typography variant="body2" color="textSecondary" component="p">
          <NotificationsActiveIcon />
          {' '}
          Following
        </Typography>
      </>
    );
  }

  function NotFollowingIndicator() {
    return (
      <>
        <Typography variant="body2" color="textSecondary" component="p">
          <NotificationsNoneIcon />
          {' '}
          Not Following
        </Typography>
      </>
    );
  }

  return (
    <>
      {(squeakProfile.getFollowing())
        ? FollowingIndicator()
        : NotFollowingIndicator()}
    </>
  );
}
