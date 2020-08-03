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
  SetPeerSubscribedRequest,
  SetPeerPublishingRequest,
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
  const setSubscribed = (id, subscribed) => {
        console.log("called setSubscribed with peerId: " + id + ", subscribed: " + subscribed);
        var setPeerSubscribedRequest = new SetPeerSubscribedRequest()
        setPeerSubscribedRequest.setPeerId(id);
        setPeerSubscribedRequest.setSubscribed(subscribed);
        console.log(setPeerSubscribedRequest);
        client.setPeerSubscribed(setPeerSubscribedRequest, {}, (err, response) => {
          console.log(response);
          getPeer(id);
        });
  };
  const setPublishing = (id, publishing) => {
        console.log("called setPublishing with peerId: " + id + ", publishing: " + publishing);
        var setPeerPublishingRequest = new SetPeerPublishingRequest()
        setPeerPublishingRequest.setPeerId(id);
        setPeerPublishingRequest.setPublishing(publishing);
        console.log(setPeerPublishingRequest);
        client.setPeerPublishing(setPeerPublishingRequest, {}, (err, response) => {
          console.log(response);
          getPeer(id);
        });
  };

  useEffect(()=>{
    getPeer(id)
  },[id]);

  const handleSettingsSubscribedChange = (event) => {
    console.log("Subscribed changed for peer id: " + id);
    console.log("Subscribed changed to: " + event.target.checked);
    setSubscribed(id, event.target.checked);
  };

  const handleSettingsPublishingChange = (event) => {
    console.log("Publishing changed for peer id: " + id);
    console.log("Publishing changed to: " + event.target.checked);
    setPublishing(id, event.target.checked);
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
            control={<Switch checked={peer.getSubscribed()} onChange={handleSettingsSubscribedChange} />}
            label="Subscribed"
          />
          <FormControlLabel
            control={<Switch checked={peer.getPublishing()} onChange={handleSettingsPublishingChange} />}
            label="Publishing"
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
