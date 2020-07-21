import React from "react";
import { useParams } from 'react-router-dom';
import { Grid } from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import { Typography } from "../../components/Wrappers";

export default function SqueakAddressPage() {
  var classes = useStyles();
  const { id } = useParams();

  return (
    <>
      <PageTitle title={'Squeak Address: ' + id} />
      <Grid container spacing={4}>
      <div>
      Hello!
      </div>
      </Grid>
    </>
  );
}
