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

import {GetInfoRequest} from "../../proto/lnd_pb"
import {
  GetSqueakServersRequest,
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

export default function Servers() {
  const classes = useStyles();
  const [servers, setServers] = useState([]);
  const [createSubscriptionDialogOpen, setCreateSubscriptionDialogOpen] = useState(false);
  const history = useHistory();

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const getSqueakServers = () => {
    console.log("called getSigningProfiles");

    var getSqueakServersRequest = new GetSqueakServersRequest()

    client.getSqueakServers(getSqueakServersRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        return;
      }
      console.log(response);
      setServers(response.getSqueakServersList());
    });
  };

  const handleClickOpenCreateSubscriptionDialog = () => {
    setCreateSubscriptionDialogOpen(true);
  };

  const handleCloseCreateSubscriptionDialog = () => {
    setCreateSubscriptionDialogOpen(false);
  };

  useEffect(() => {
    getSqueakServers()
  }, []);

  function CreateServerButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickOpenCreateSubscriptionDialog();
            }}>Create Server Subscription
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function ServersInfo() {
    return (
      <>
      <Grid container spacing={4}>
        {CreateServerButton()}
       <Grid item xs={12}>
         <MUIDataTable
           title="Servers"
           data={servers.map(p =>
              [
                p.getServerName(),
                p.getHost(),
              ]
            )}
           columns={["Name", "Host"]}
           options={{
             filter: false,
             print: false,
             viewColumns: false,
             selectableRows: "none",
             onRowClick: rowData => {
               var host = rowData[1];
               console.log("clicked on host" + host);
             }
           }}/>
       </Grid>
     </Grid>
      </>
    )
  }

  function CreateServerDialogContent() {
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
     < PageTitle title = "Servers" />
    {ServersInfo()}
    {CreateServerDialogContent()}
   < />);
}
