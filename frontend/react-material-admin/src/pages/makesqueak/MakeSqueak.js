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
  // const [age, setAge] = useState('');
  const [value, setValue] = useState('Controlled');
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
    setProfileId(event.target.value);
  };

  const handleChangeContent = (event) => {
    setContent(event.target.value);
  };

  const makeSqueak = (profileId, content, replyto) => {
    console.log("called makeSqueak");

    var makeSqueakRequest = new MakeSqueakRequest()
    makeSqueakRequest.setProfileId(profileId);
    makeSqueakRequest.setContent(content);
    makeSqueakRequest.setReplyto(replyto);
    console.log(makeSqueakRequest);

    client.makeSqueak(makeSqueakRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error making squeak: ' + err.message);
        return;
      }

      console.log(response);
      console.log(response.getSqueakHash());
      goToSqueakPage(response.getSqueakHash());
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

  function MakeSelectSigningProfile() {
    return (
      <FormControl className={classes.formControl}>
        <InputLabel id="demo-simple-select-label">Signing Profile</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={profileId}
          onChange={handleChange}
        >
          {signingProfiles.map(p =>
            <MenuItem key={p.getProfileId()} value={p.getProfileId()}>{p.getProfileName()}</MenuItem>
          )}
        </Select>
      </FormControl>
    )
  }

  function MakeSqueakForm() {
    return (
      <form className={classes.root} noValidate autoComplete="off">
        <div>
          <TextField
            id="standard-textarea"
            label="Squeak content"
            placeholder="Enter squeak content here..."
            value={content}
            onChange={handleChangeContent}
            multiline
            rows={8}
            fullWidth
            inputProps={{ maxLength: 280 }}
          />
        </div>
      </form>
    )
  }

  function MakeSqueakButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="secondary"
       className={classes.button}
       >
       Make Squeak
       </Button>
    )
  }

  return (
    <>
     < PageTitle title = "Make Squeak" />

     <div className={classes.root}>

     {MakeSelectSigningProfile()}
     {MakeSqueakForm()}
     {MakeSqueakButton()}

     </div>
</>);
}
