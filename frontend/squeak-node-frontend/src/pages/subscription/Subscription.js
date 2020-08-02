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
  SetSubscriptionSubscribedRequest,
  SetSubscriptionPublishingRequest,
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
  const setSubscribed = (id, subscribed) => {
        console.log("called setSubscribed with subscriptionId: " + id + ", subscribed: " + subscribed);
        var setSubscriptionSubscribedRequest = new SetSubscriptionSubscribedRequest()
        setSubscriptionSubscribedRequest.setSubscriptionId(id);
        setSubscriptionSubscribedRequest.setSubscribed(subscribed);
        console.log(setSubscriptionSubscribedRequest);
        client.setSubscriptionSubscribed(setSubscriptionSubscribedRequest, {}, (err, response) => {
          console.log(response);
          getSubscription(id);
        });
  };
  const setPublishing = (id, publishing) => {
        console.log("called setPublishing with subscriptionId: " + id + ", publishing: " + publishing);
        var setSubscriptionPublishingRequest = new SetSubscriptionPublishingRequest()
        setSubscriptionPublishingRequest.setSubscriptionId(id);
        setSubscriptionPublishingRequest.setPublishing(publishing);
        console.log(setSubscriptionPublishingRequest);
        client.setSubscriptionPublishing(setSubscriptionPublishingRequest, {}, (err, response) => {
          console.log(response);
          getSubscription(id);
        });
  };

  useEffect(()=>{
    getSubscription(id)
  },[id]);

  const handleSettingsSubscribedChange = (event) => {
    console.log("Subscribed changed for subscription id: " + id);
    console.log("Subscribed changed to: " + event.target.checked);
    setSubscribed(id, event.target.checked);
  };

  const handleSettingsPublishingChange = (event) => {
    console.log("Publishing changed for subscription id: " + id);
    console.log("Publishing changed to: " + event.target.checked);
    setPublishing(id, event.target.checked);
  };

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
        {SubscriptionSettingsForm()}
      </>
    )
  }

  function SubscriptionSettingsForm() {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Subscription settings</FormLabel>
        <FormGroup>
          <FormControlLabel
            control={<Switch checked={subscription.getSubscribed()} onChange={handleSettingsSubscribedChange} />}
            label="Subscribed"
          />
          <FormControlLabel
            control={<Switch checked={subscription.getPublishing()} onChange={handleSettingsPublishingChange} />}
            label="Publishing"
          />
        </FormGroup>
      </FormControl>
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
