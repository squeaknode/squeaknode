import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  Divider,
  Box,
} from "@material-ui/core";

import Timeline from '@material-ui/lab/Timeline';
import TimelineItem from '@material-ui/lab/TimelineItem';
import TimelineSeparator from '@material-ui/lab/TimelineSeparator';
import TimelineConnector from '@material-ui/lab/TimelineConnector';
import TimelineContent from '@material-ui/lab/TimelineContent';
import TimelineDot from '@material-ui/lab/TimelineDot';

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakDetailItem from "../../components/SqueakDetailItem";
import SqueakThreadItem from "../../components/SqueakThreadItem";

import {
  getSqueakDisplayRequest,
  getAncestorSqueakDisplaysRequest,
  getReplySqueakDisplaysRequest,
  getNetworkRequest,
} from "../../squeakclient/requests"


export default function SqueakPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [squeak, setSqueak] = useState(null);
  const [ancestorSqueaks, setAncestorSqueaks] = useState([]);
  const [replySqueaks, setReplySqueaks] = useState([]);
  const [network, setNetwork] = useState("");

  const getSqueak = (hash) => {
      getSqueakDisplayRequest(hash, setSqueak);
  };
  const getAncestorSqueaks = (hash) => {
      getAncestorSqueakDisplaysRequest(hash, setAncestorSqueaks);
  };
  const getReplySqueaks = (hash) => {
      getReplySqueakDisplaysRequest(hash, setReplySqueaks);
  };
  const getNetwork = () => {
      getNetworkRequest(setNetwork);
  };

  const unknownAncestorHash = () => {
      if (!ancestorSqueaks) {
        return null;
      }
      var oldestKnownAncestor = ancestorSqueaks[0];
      if (!oldestKnownAncestor) {
        return null;
      }
      console.log(oldestKnownAncestor);
      console.log("oldestKnownAncestor");
      return oldestKnownAncestor.getReplyTo();
  };

  useEffect(()=>{
    getSqueak(hash)
  },[hash]);
  useEffect(()=>{
    getAncestorSqueaks(hash)
  },[hash]);
  useEffect(()=>{
    getReplySqueaks(hash)
  },[hash]);
  useEffect(()=>{
    getNetwork()
  },[]);

  function NoSqueakContent() {
    return (
      <div>
        Unable to load squeak.
      </div>
    )
  }

  function UnkownReplyToContent() {
    var squeakHash = unknownAncestorHash();
    if (!squeakHash) {
      return (
        <></>
      )
    }
    return (
      <div>
          <Box
            key={squeakHash}
            >
          <SqueakThreadItem
            hash={squeakHash}
            key={squeakHash}
            squeak={null}>
          </SqueakThreadItem>
          <Divider />
          </Box>
      </div>
    )
  }

  function AncestorsContent() {
    return (
      <Timeline>
        {ancestorSqueaks.slice(0, -1)
          //.reverse()
          .map(ancestorSqueak =>
            <TimelineItem>
  <TimelineSeparator>
    <TimelineDot />
    <TimelineConnector />
  </TimelineSeparator>
  <TimelineContent>

  <Box
    key={ancestorSqueak.getSqueakHash()}
    >
  <SqueakThreadItem
    hash={ancestorSqueak.getSqueakHash()}
    key={ancestorSqueak.getSqueakHash()}
    squeak={ancestorSqueak}
    network={network}>
  </SqueakThreadItem>
  <Divider />
  </Box>

  </TimelineContent>
</TimelineItem>

        )}
      </Timeline>
    )
  }

  function RepliesContent() {
    console.log("replySqueaks: " + replySqueaks);
    return (
      <div>
        {replySqueaks
          .map(replySqueak =>
          <Box
            p={1}
            key={replySqueak.getSqueakHash()}
            >
          <SqueakThreadItem
            hash={replySqueak.getSqueakHash()}
            key={replySqueak.getSqueakHash()}
            squeak={replySqueak}
            network={network}>
          </SqueakThreadItem>
          <Divider />
          </Box>
        )}
      </div>
    )
  }

  function SqueakContent() {
    return (
      <>
        {UnkownReplyToContent()}
        {AncestorsContent()}
        <div>
          <SqueakDetailItem
            hash={hash}
            squeak={squeak}
            network={network}>
          </SqueakDetailItem>
        </div>
        {RepliesContent()}
      </>
    )
  }

  return (
    <>
      <PageTitle title="Squeak" />
      {SqueakContent()}
    </>
  );
}
