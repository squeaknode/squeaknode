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
import PeerListItem from "../../components/PeerListItem";


// data
import mock from "../dashboard/mock";

import {
  getPeersRequest,
} from "../../squeakclient/requests"
import {
  goToPeerPage,
} from "../../navigation/navigation"


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
  const [value, setValue] = useState(0);
  const history = useHistory();

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

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

  function TabPanel(props) {
    const { children, value, index, ...other } = props;
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <div>{children}</div>
        )}
      </div>
    );
  }

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

  function PeersGridItem(peers) {
    return (
      <Grid item xs={12}>
        {peers.map(peer =>
           <Box
              p={1}
              key={peer.getPeerName()}
           >
             <PeerListItem
                key={peer.getPeerName()}
                handlePeerClick={() => console.log("clicked peer")}
                peer={peer}>
             </PeerListItem>
           </Box>
        )}
      </Grid>
    )
  }

  function PeersTabs() {
    return (
      <>
      <AppBar position="static" color="default">
        <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
          <Tab label="Saved Peers" {...a11yProps(0)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {SavedPeersContent()}
      </TabPanel>
      </>
    )
  }

  function SavedPeersContent() {
    return (
      <>
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Widget disableWidgetMenu>
            {CreatePeerButton()}
            {PeersGridItem(peers)}
          </Widget>
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
          ></CreatePeerDialog>
      </>
    )
  }

  return (
    <>
     < PageTitle title = "Peers" />
    {PeersTabs()}
    {CreatePeerDialogContent()}
   < />);
}
