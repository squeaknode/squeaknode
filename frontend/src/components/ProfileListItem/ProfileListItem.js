import React from "react";
import {useHistory} from "react-router-dom";

import Card from '@material-ui/core/Card';
import Button from '@material-ui/core/Button';
import CardHeader from "@material-ui/core/CardHeader";

// icons
import RecordVoiceOverIcon from '@material-ui/icons/RecordVoiceOver';

import useStyles from "../../pages/wallet/styles";

import {
  goToProfilePage,
} from "../../navigation/navigation"


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
    console.log("Handling profile click...");
    const profileId = profile.getProfileId();
    //const host = getPeerHost();
    //const port = getPeerPort();
    goToProfilePage(history, profileId);
  }

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

  return (
     <Card
        className={classes.root}
        onClick={onProfileClick}
     >
       <CardHeader
          avatar={<RecordVoiceOverIcon/>}
          title={`Name: ${profile.getProfileName()}`}
          subheader={`Address: ${profile.getAddress()}`}
          // action={<Button size="small">View Peer</Button>}
       />
     </Card>
  )
}
