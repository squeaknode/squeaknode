import React, { useState } from "react";

import TimelineDot from '@material-ui/lab/TimelineDot';

import FaceIcon from '@material-ui/icons/Face';
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
    console.log("Avatar clicked with squeak: " + squeak);
    if (squeak) {
      goToSqueakAddressPage(squeak.getAuthorAddress());
    }
  };

  const getAuthorImage = () => {
    console.log(squeak);
    console.log("squeak image: " + squeak.getAuthorImage());
    return squeak.getAuthorImage();
  }

  function ImageSrcString() {
    console.log("getAuthorImage" + getAuthorImage());
    return "data:image/jpeg;base64," + getAuthorImage();
  }

  function AvatarImage() {
    console.log("ImageSrcString: " + ImageSrcString());
    return (
      <Avatar alt="Remy Sharp" src={`${ImageSrcString()}`} />
    )
  }

  console.log("show avatar");
  return (
    <TimelineDot
    onClick={handleAvatarClick}
    style={{cursor: 'pointer'}}
    >
      {squeak && AvatarImage()}
    </TimelineDot>
  )
}
