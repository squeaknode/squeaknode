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
  GetSubscriptionRequest,
} from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function SubscriptionPage() {
  var classes = useStyles();
  const { id } = useParams();
  const [subscription, setSubscription] = useState(null);

  const getSubscription = (id) => {
        console.log("called getSubscription with subscriptionId: " + id);
        var getSubscriptionRequest = new GetSubscriptionRequest()
        getSubscriptionRequest.setSubscriptionId(id);
        console.log(getSubscriptionRequest);
        client.getSubscription(getSubscriptionRequest, {}, (err, response) => {
          console.log(response);
          setSubscription(response.getSqueakSubscription())
        });
  };


  useEffect(()=>{
    getSubscription(id)
  },[id]);


  function NoSubscriptionContent() {
    return (
      <p>
        No subscription loaded
      </p>
    )
  }

  function SubscriptionContent() {
    return (
      <>
        <p>
          Subscription name: {subscription.getSubscriptionName()}
        </p>
      </>
    )
  }

  return (
    <>
      <PageTitle title={'Subscription: ' + (subscription ? subscription.getSubscriptionName() : null)} />
      <div>
      {subscription
        ? SubscriptionContent()
        : NoSubscriptionContent()
      }
      </div>
    </>
  );
}
