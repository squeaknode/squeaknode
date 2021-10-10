import React from 'react';
import {
  Route,
  Switch,
  Redirect,
  withRouter,
} from 'react-router-dom';
import classnames from 'classnames';

// styles
import useStyles from './styles';

// components
import Header from '../Header';
import Sidebar from '../Sidebar';

// pages
import Timeline from '../../pages/timeline';
import Dashboard from '../../pages/dashboard';
import SqueakAddress from '../../pages/squeakaddress';
import Search from '../../pages/search';
import Squeak from '../../pages/squeak';
import Profile from '../../pages/profile';
import Wallet from '../../pages/wallet';
import LightningNode from '../../pages/lightningnode';
import Channel from '../../pages/channel';
import Notifications from '../../pages/notifications';
import Maps from '../../pages/maps';
import Profiles from '../../pages/profiles';
import Payments from '../../pages/payments';
import SentPayments from '../../pages/sentpayments';
import ReceivedPayments from '../../pages/receivedpayments';
import Liked from '../../pages/liked';
import Icons from '../../pages/icons';
import Charts from '../../pages/charts';
import Peers from '../../pages/peers';
import Peer from '../../pages/peer';
import PeerAddress from '../../pages/peeraddress';

// context
import { useLayoutState } from '../../context/LayoutContext';

function Layout(props) {
  const classes = useStyles();

  // global
  const layoutState = useLayoutState();

  return (
    <div className={classes.root}>
      <>
        <Header history={props.history} />
        <Sidebar />
        <div
          className={classnames(classes.content, {
            [classes.contentShift]: layoutState.isSidebarOpened,
          })}
        >
          <div className={classes.fakeToolbar} />
          <Switch>
            <Route path="/app/timeline" component={Timeline} />
            <Route path="/app/dashboard" component={Dashboard} />
            <Route path="/app/squeakaddress/:address" component={SqueakAddress} />
            <Route path="/app/search/:searchText" component={Search} />
            <Route path="/app/search" component={Search} />
            <Route path="/app/squeak/:hash" component={Squeak} />
            <Route path="/app/profile/:id" component={Profile} />
            <Route path="/app/profiles" component={Profiles} />
            <Route path="/app/payments" component={Payments} />
            <Route path="/app/sentpayments" component={SentPayments} />
            <Route path="/app/receivedpayments" component={ReceivedPayments} />
            <Route path="/app/liked" component={Liked} />
            <Route path="/app/wallet" component={Wallet} />
            <Route path="/app/lightningnode/:pubkey/:host/:port" component={LightningNode} />
            <Route path="/app/lightningnode/:pubkey/:host" component={LightningNode} />
            <Route path="/app/lightningnode/:pubkey" component={LightningNode} />
            <Route path="/app/channel/:txId/:outputIndex" component={Channel} />
            <Route path="/app/peers" component={Peers} />
            <Route path="/app/peer/:id" component={Peer} />
            <Route path="/app/peeraddress/:host/:port/:useTorStr" component={PeerAddress} />
            <Route path="/app/notifications" component={Notifications} />
            <Route
              exact
              path="/app/ui"
              render={() => <Redirect to="/app/ui/icons" />}
            />
            <Route path="/app/ui/maps" component={Maps} />
            <Route path="/app/ui/icons" component={Icons} />
            <Route path="/app/ui/charts" component={Charts} />
          </Switch>
        </div>
      </>
    </div>
  );
}

export default withRouter(Layout);
