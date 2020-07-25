import React, {useState, useEffect} from 'react';
import {useHistory} from "react-router-dom";
import {Grid, TextField, Button, Typography, Paper} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
// import { Typography } from "../../components/Wrappers";

import {CreateContactProfileRequest} from "../../proto/squeak_admin_pb"
import {SqueakAdminClient} from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function CreateContactProfilePage() {
  const [profileName, setProfileName] = useState('');
  const [address, setAddress] = useState('');

  var classes = useStyles();
  const history = useHistory();

  const goToProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  function handleSubmit(event) {
      event.preventDefault();
      console.log( 'profileName:', profileName);
     // You should see email and password in console.
     // ..code to submit form to backend here...
     createContactProfile(profileName)
  }

  const createContactProfile = (profileName, squeakAddress) => {
    console.log("called createContactProfile");

    var createContactProfileRequest = new CreateContactProfileRequest()
    createContactProfileRequest.setProfileName(profileName);
    createContactProfileRequest.setAddress(squeakAddress);
    console.log(createContactProfileRequest);

    client.createContactProfile(createContactProfileRequest, {}, (err, response) => {
      console.log(response);
      console.log(response.getProfileId());
      goToProfilePage(response.getProfileId());
    });
  };

  return (
    <>
     < PageTitle title = "Create Contact Profile" />
     <Paper>
         <form className={classes.root} onSubmit={handleSubmit} >
             <TextField required
                 value={profileName}
                 label="Profile name"
                 onInput={ e=>setProfileName(e.target.value)}
             />
             <TextField required
                 value={address}
                 label="Address"
                 onInput={ e=>setProfileName(e.target.value)}
             />
             <Typography className={classes.divider} />
             <Button
                 type="submit"
                 className={classes.button}
             >
                 Create
             </Button>
         </form>
     </Paper>
</>);
}
