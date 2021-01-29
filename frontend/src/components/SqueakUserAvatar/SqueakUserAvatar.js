import React, { useState } from "react";

import TimelineDot from '@material-ui/lab/TimelineDot';

import FaceIcon from '@material-ui/icons/Face';
import HelpIcon from '@material-ui/icons/Help';
import Avatar from '@material-ui/core/Avatar';

import {useHistory} from "react-router-dom";

import {
  getAuthorImageSrcString,
} from "../../squeakimages/images"


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

  function AvatarImage() {
    return (
      <Avatar src={`${getAuthorImageSrcString(squeak)}`} />
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
