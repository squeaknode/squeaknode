import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Grid } from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
// import { Typography } from "../../components/Wrappers";

import { GetAddressSqueakDisplaysRequest } from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function SqueakAddressPage() {
  var classes = useStyles();
  const { id } = useParams();
  const [squeaks, setSqueaks] = useState([]);

  const getSqueaks = () => {
        console.log("called getSqueaks");

        var getSqueaksRequest = new GetAddressSqueakDisplaysRequest()
        getSqueaksRequest.setAddress(id);
        console.log(getSqueaksRequest);

        client.getAddressSqueakDisplays(getSqueaksRequest, {}, (err, response) => {
          console.log(response);
          console.log(response.getSqueakDisplayEntriesList());
          // console.log(response.getSqueakDisplayEntriesList(),length);
          setSqueaks(response.getSqueakDisplayEntriesList())
        });
  };
  useEffect(()=>{
    getSqueaks()
  },[]);

  return (
    <>
      <PageTitle title={'Squeak Address: ' + id} />
      <div>
      Hello!
      Number of squeaks for address: {squeaks.length}
      </div>
    </>
  );
}
