import React, { useState } from "react";

import TimelineDot from '@material-ui/lab/TimelineDot';

import FaceIcon from '@material-ui/icons/Face';

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
    console.log("Avatar clicked with squeak: " + squeak);
    if (squeak) {
      goToSqueakAddressPage(squeak.getAuthorAddress());
    }
  };
  return (
    <TimelineDot
    onClick={handleAvatarClick}
    style={{cursor: 'pointer'}}
    >
      <FaceIcon />
    </TimelineDot>
  )
}
