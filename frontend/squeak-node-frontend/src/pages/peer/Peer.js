import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Grid,
  FormLabel,
  FormControl,
  FormGroup,
  FormControlLabel,
  FormHelperText,
  Switch,
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";

import {
  GetPeerRequest,
  SetPeerDownloadingRequest,
  SetPeerUploadingRequest,
} from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function PeerPage() {
  var classes = useStyles();
  const { id } = useParams();
  const [peer, setPeer] = useState(null);

  const getPeer = (id) => {
        console.log("called getPeer with peerId: " + id);
        var getPeerRequest = new GetPeerRequest()
        getPeerRequest.setPeerId(id);
        console.log(getPeerRequest);
        client.getPeer(getPeerRequest, {}, (err, response) => {
          console.log(response);
          setPeer(response.getSqueakPeer())
        });
  };
  const setDownloading = (id, downloading) => {
        console.log("called setDownloading with peerId: " + id + ", downloading: " + downloading);
        var setPeerDownloadingRequest = new SetPeerDownloadingRequest()
        setPeerDownloadingRequest.setPeerId(id);
        setPeerDownloadingRequest.setDownloading(downloading);
        console.log(setPeerDownloadingRequest);
        client.setPeerDownloading(setPeerDownloadingRequest, {}, (err, response) => {
          console.log(response);
          getPeer(id);
        });
  };
  const setUploading = (id, uploading) => {
        console.log("called setUploading with peerId: " + id + ", uploading: " + uploading);
        var setPeerUploadingRequest = new SetPeerUploadingRequest()
        setPeerUploadingRequest.setPeerId(id);
        setPeerUploadingRequest.setUploading(uploading);
        console.log(setPeerUploadingRequest);
        client.setPeerUploading(setPeerUploadingRequest, {}, (err, response) => {
          console.log(response);
          getPeer(id);
        });
  };

  useEffect(()=>{
    getPeer(id)
  },[id]);

  const handleSettingsDownloadingChange = (event) => {
    console.log("Downloading changed for peer id: " + id);
    console.log("Downloading changed to: " + event.target.checked);
    setDownloading(id, event.target.checked);
  };

  const handleSettingsUploadingChange = (event) => {
    console.log("Uploading changed for peer id: " + id);
    console.log("Uploading changed to: " + event.target.checked);
    setUploading(id, event.target.checked);
  };

  function NoPeerContent() {
    return (
      <p>
        No peer loaded
      </p>
    )
  }

  function PeerContent() {
    return (
      <>
        <p>
          Peer name: {peer.getPeerName()}
        </p>
        {PeerSettingsForm()}
      </>
    )
  }

  function PeerSettingsForm() {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Peer settings</FormLabel>
        <FormGroup>
          <FormControlLabel
            control={<Switch checked={peer.getDownloading()} onChange={handleSettingsDownloadingChange} />}
            label="Downloading"
          />
          <FormControlLabel
            control={<Switch checked={peer.getUploading()} onChange={handleSettingsUploadingChange} />}
            label="Uploading"
          />
        </FormGroup>
      </FormControl>
    )
  }

  return (
    <>
      <PageTitle title={'Peer: ' + (peer ? peer.getPeerName() : null)} />
      <div>
      {peer
        ? PeerContent()
        : NoPeerContent()
      }
      </div>
    </>
  );
}
