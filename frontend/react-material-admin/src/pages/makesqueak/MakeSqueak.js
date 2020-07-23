import React, {useState, useEffect} from 'react';
import {useHistory, useParams } from 'react-router-dom';
import {Grid, TextField, Button, Typography, Paper, Select, InputLabel, MenuItem} from "@material-ui/core";

import FormControl from '@material-ui/core/FormControl';

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
// import { Typography } from "../../components/Wrappers";

import {MakeSqueakRequest, GetSigningProfilesRequest} from "../../proto/squeak_admin_pb"
import {SqueakAdminClient} from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function MakeSqueakPage() {
  const [profileId, setProfileId] = useState(-1);
  const [content, setContent] = useState('');
  const [signingProfiles, setSigningProfiles] = useState([]);
  const [age, setAge] = useState('');
  const { replyto } = useParams();

  var classes = useStyles();
  const history = useHistory();

  const goToSqueakPage = (squeakHash) => {
    history.push("/app/squeak/" + squeakHash);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'profileId:', profileId);
    console.log( 'content:', content);
    console.log( 'replyto:', replyto);
   makeSqueak(profileId, content, replyto);
  }

  const handleChange = (event) => {
    setAge(event.target.value);
  };

  const makeSqueak = (profileId, content, replyto) => {
    console.log("called makeSqueak");

    var makeSqueakRequest = new MakeSqueakRequest()
    makeSqueakRequest.setProfileId(profileId);
    makeSqueakRequest.setContent(content);
    makeSqueakRequest.setReplyto(replyto);
    console.log(makeSqueakRequest);

    client.makeSqueak(makeSqueakRequest, {}, (err, response) => {
      console.log(response);
      console.log(response.getHash());
      goToSqueakPage(response.getHash());
    });
  };
  const getSigningProfiles = () => {
    console.log("called getSigningProfiles");
    var getSigningProfilesRequest = new GetSigningProfilesRequest()
    client.getSigningProfiles(getSigningProfilesRequest, {}, (err, response) => {
      console.log(response);
      console.log(response.getSqueakProfilesList());
      setSigningProfiles(response.getSqueakProfilesList());
    });
  };

  useEffect(() => {
    getSigningProfiles()
  }, []);

  return (
    <>
     < PageTitle title = "Make Squeak" />

     <div>
      Number of signing profiles: {signingProfiles.length}
     </div>

     <Paper>
         <form className={classes.root} onSubmit={handleSubmit} >

         <div>
         <FormControl className={classes.formControl}>
           <InputLabel id="demo-simple-select-label">Age</InputLabel>
           <Select
             labelId="demo-simple-select-label"
             id="demo-simple-select"
             value={age}
             onChange={handleChange}
           >
             <MenuItem value={10}>Ten</MenuItem>
             <MenuItem value={20}>Twenty</MenuItem>
             <MenuItem value={30}>Thirty</MenuItem>
           </Select>
         </FormControl>
         </div>

        <div>
             <TextField required
                 value={content}
                 label="Content"
                 inputProps={{
                   multiline: true,
                   maxLength: 280,
                 }}
                 onInput={ e=>setContent(e.target.value)}
             />
        </div>

             <Typography className={classes.divider} />

        <div>
             <Button
                 type="submit"
                 className={classes.button}
             >
                 Make Squeak
             </Button>
        </div>

         </form>
     </Paper>
</>);
}
