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
  const [email, setEmail] = useState('');

  var classes = useStyles();
  const history = useHistory();

  const goToProfilePage = (profileId) => {
    history.push("/app/squeakaddress/" + profileId);
  };

  function handleSubmit(event) {
      event.preventDefault();
      console.log( 'Email:', email);
     // You should see email and password in console.
     // ..code to submit form to backend here...
  }

  const createSigningProfile = () => {
    console.log("called createSigningProfile");

    var createSigningProfileRequest = new CreateSigningProfileRequest()
    createSigningProfileRequest.setProfileName("foooo");
    console.log(createSigningProfileRequest);

    client.getAddressSqueakDisplays(createSigningProfileRequest, {}, (err, response) => {
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
                 value={email}
                 label="Profile name"
                 onInput={ e=>setEmail(e.target.value)}
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
