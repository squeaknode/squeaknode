import React, {useState, useEffect} from 'react';
import {useHistory} from "react-router-dom";
import {Grid, TextField, Button, Typography, Paper} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
// import { Typography } from "../../components/Wrappers";

import {CreateSigningProfileRequest} from "../../proto/squeak_admin_pb"
import {SqueakAdminClient} from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function CreateSigningProfilePage() {
  const [profileName, setProfileName] = useState('');

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
     createSigningProfile(profileName)
  }

  const createSigningProfile = (profileName) => {
    console.log("called createSigningProfile");

    var createSigningProfileRequest = new CreateSigningProfileRequest()
    createSigningProfileRequest.setProfileName(profileName);
    console.log(createSigningProfileRequest);

    client.createSigningProfile(createSigningProfileRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error creating signing profile: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getProfileId());
      goToProfilePage(response.getProfileId());
    });
  };

  return (
    <>
     < PageTitle title = "Create Signing Profile" />
     <Paper>
         <form className={classes.root} onSubmit={handleSubmit} >
             <TextField required
                 value={profileName}
                 label="Profile name"
                 onInput={ e=>setProfileName(e.target.value)}
             />
             <Typography className={classes.divider} />
             <Button
                 type="submit"
                 variant="contained"
                 className={classes.button}
             >
                 Create
             </Button>
         </form>
     </Paper>
</>);
}
