import React, {useState, useEffect} from 'react';
import {useHistory} from "react-router-dom";
import {
    Grid,
    Button,
    Paper,
    Tabs,
    Tab,
    AppBar,
    Box,
    Typography,
  } from "@material-ui/core";
import MUIDataTable from "mui-datatables";

// styles
import {makeStyles} from '@material-ui/core/styles';

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import Table from "../dashboard/components/Table/Table";
import CreateSubscriptionDialog from "../../components/CreateSubscriptionDialog";

// data
import mock from "../dashboard/mock";

import {
  GetSubscriptionsRequest,
} from "../../proto/squeak_admin_pb"
import {SqueakAdminClient} from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1)
    }
  }
}));

export default function Subscriptions() {
  const classes = useStyles();
  const [subscriptions, setSubscriptions] = useState([]);
  const [createSubscriptionDialogOpen, setCreateSubscriptionDialogOpen] = useState(false);
  const history = useHistory();

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const getSqueakSubscriptions = () => {
    console.log("called getSigningProfiles");

    var getSubscriptionsRequest = new GetSubscriptionsRequest();

    client.getSubscriptions(getSubscriptionsRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        return;
      }
      console.log(response);
      setSubscriptions(response.getSqueakSubscriptionsList());
    });
  };

  const goToSubscriptionPage = (id) => {
    history.push("/app/Subscription/" + id);
  };

  const handleClickOpenCreateSubscriptionDialog = () => {
    setCreateSubscriptionDialogOpen(true);
  };

  const handleCloseCreateSubscriptionDialog = () => {
    setCreateSubscriptionDialogOpen(false);
  };

  useEffect(() => {
    getSqueakSubscriptions()
  }, []);

  function CreateSubscriptionButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickOpenCreateSubscriptionDialog();
            }}>Create Subscription
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function SubscriptionsInfo() {
    return (
      <>
      <Grid container spacing={4}>
        {CreateSubscriptionButton()}
       <Grid item xs={12}>
         <MUIDataTable
           title="Subscriptions"
           data={subscriptions.map(s =>
              [
                s.getSubscriptionId(),
                s.getSubscriptionName(),
                s.getHost(),
                s.getPort(),
                s.getSubscribed().toString(),
                s.getPublishing().toString(),
              ]
            )}
           columns={[
             {
               name: "Id",
               options: {
                 display: false,
               }
             },
             "Name",
             "Host",
             "Port",
             "Subscribed",
             "Publishing",
           ]}
           options={{
             filter: false,
             print: false,
             viewColumns: false,
             selectableRows: "none",
             onRowClick: rowData => {
               var id = rowData[0];
               console.log("clicked on id" + id);
               goToSubscriptionPage(id);
             },
           }}/>
       </Grid>
     </Grid>
      </>
    )
  }

  function CreateSubscriptionDialogContent() {
    return (
      <>
        <CreateSubscriptionDialog
          open={createSubscriptionDialogOpen}
          handleClose={handleCloseCreateSubscriptionDialog}
          ></CreateSubscriptionDialog>
      </>
    )
  }

  return (
    <>
     < PageTitle title = "Subscriptions" />
    {SubscriptionsInfo()}
    {CreateSubscriptionDialogContent()}
   < />);
}
