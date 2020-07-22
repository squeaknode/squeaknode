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

export default function ProfilePage() {
  var classes = useStyles();
  const { id } = useParams();

  return (
    <>
      <PageTitle title={'Squeak Profile: ' + id} />
      <div>
      Hello!
      </div>
    </>
  );
}
