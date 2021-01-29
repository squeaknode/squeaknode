import React, { useState } from "react";

import TimelineDot from '@material-ui/lab/TimelineDot';

import FaceIcon from '@material-ui/icons/Face';
import HelpIcon from '@material-ui/icons/Help';
import Avatar from '@material-ui/core/Avatar';

import {useHistory} from "react-router-dom";

export default function SqueakUserAvatar({
  squeak,
  ...props
}) {
  const history = useHistory();

  const goToSqueakAddressPage = () => {
    history.push("/app/squeakaddress/" + squeak.getAuthorAddress());
  };

  const handleAvatarClick = () => {
    if (squeak) {
      goToSqueakAddressPage(squeak.getAuthorAddress());
    }
  };

  const getAuthorImage = () => {
    return squeak.getAuthorImage();
  }

  function ImageSrcString() {
    return "data:image/jpeg;base64," + getAuthorImage();
  }

  function AvatarImage() {
    return (
      <Avatar src={`${ImageSrcString()}`} />
    )
  }

  return (
    <TimelineDot
    onClick={handleAvatarClick}
    style={{cursor: 'pointer'}}
    >
      {squeak ?
        AvatarImage() :
        <HelpIcon fontSize="large" />
      }
    </TimelineDot>
  )
}
