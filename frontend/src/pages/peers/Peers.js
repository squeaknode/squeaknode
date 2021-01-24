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
import CreatePeerDialog from "../../components/CreatePeerDialog";

// data
import mock from "../dashboard/mock";

import {
  getPeersRequest,
} from "../../squeakclient/requests"
import {navigateTo, PEER_VIEW} from "../../navigation/routes";


const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1)
    }
  }
}));

export default function Peers() {
  const classes = useStyles();
  const [peers, setPeers] = useState([]);
  const [createPeerDialogOpen, setCreatePeerDialogOpen] = useState(false);
  const history = useHistory();

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const getSqueakPeers = () => {
    getPeersRequest(setPeers);
  };

  const handleClickOpenCreatePeerDialog = () => {
    setCreatePeerDialogOpen(true);
  };

  const handleCloseCreatePeerDialog = () => {
    setCreatePeerDialogOpen(false);
  };

  useEffect(() => {
    getSqueakPeers()
  }, []);

  function CreatePeerButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickOpenCreatePeerDialog();
            }}>Create Peer
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function PeersInfo() {
    return (
      <>
      <Grid container spacing={4}>
        {CreatePeerButton()}
       <Grid item xs={12}>
         <MUIDataTable
           title="Peers"
           data={peers.map(s =>
              [
                s.getPeerId(),
                s.getPeerName(),
                s.getHost(),
                s.getPort(),
                s.getDownloading().toString(),
                s.getUploading().toString(),
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
             "Downloading",
             "Uploading",
           ]}
           options={{
             filter: false,
             print: false,
             viewColumns: false,
             selectableRows: "none",
             onRowClick: rowData => {
               var id = rowData[0];
               console.log("clicked on id" + id);
               navigateTo(history, PEER_VIEW, [id]);
             },
           }}/>
       </Grid>
     </Grid>
      </>
    )
  }

  function CreatePeerDialogContent() {
    return (
      <>
        <CreatePeerDialog
          open={createPeerDialogOpen}
          handleClose={handleCloseCreatePeerDialog}
        />
      </>
    )
  }

  return (
    <>
      < PageTitle title = "Peers" />
      {PeersInfo()}
      {CreatePeerDialogContent()}
    </>
  )
}
