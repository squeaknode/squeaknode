import React, { useState } from "react";

import TimelineDot from '@material-ui/lab/TimelineDot';

import FaceIcon from '@material-ui/icons/Face';
import HelpIcon from '@material-ui/icons/Help';
import Avatar from '@material-ui/core/Avatar';

import {useHistory} from "react-router-dom";

import {
  getProfileImageSrcString,
} from "../../squeakimages/images"


export default function SqueakUserAvatar({
  squeakProfile,
  ...props
}) {
  const history = useHistory();

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
  };

  const handleAvatarClick = () => {
    if (squeakProfile) {
      goToSqueakAddressPage(squeakProfile.getAddress());
    }
  };

  function AvatarImage() {
    return (
      <Avatar src={`${getProfileImageSrcString(squeakProfile)}`} />
    )
  }

  return (
    <TimelineDot
    onClick={handleAvatarClick}
    style={{cursor: 'pointer'}}
    >
      {squeakProfile ?
        AvatarImage() :
        <HelpIcon fontSize="large" />
      }
    </TimelineDot>
  )
}
