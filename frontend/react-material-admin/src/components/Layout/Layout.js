import React from "react";
import {
  Route,
  Switch,
  Redirect,
  withRouter,
} from "react-router-dom";
import classnames from "classnames";

// styles
import useStyles from "./styles";

// components
import Header from "../Header";
import Sidebar from "../Sidebar";

// pages
import Dashboard from "../../pages/dashboard";
import SqueakAddress from "../../pages/squeakaddress";
import Profile from "../../pages/profile";
import CreateSigningProfile from "../../pages/createsigningprofile";
import MakeSqueak from "../../pages/makesqueak";
import Lightning from "../../pages/lightning";
import Notifications from "../../pages/notifications";
import Maps from "../../pages/maps";
import Profiles from "../../pages/profiles";
import Icons from "../../pages/icons";
import Charts from "../../pages/charts";

// context
import { useLayoutState } from "../../context/LayoutContext";

function Layout(props) {
  var classes = useStyles();

  // global
  var layoutState = useLayoutState();

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
              <Route path="/app/dashboard" component={Dashboard} />
              <Route path="/app/squeakaddress/:address" component={SqueakAddress} />
              <Route path="/app/profile/:id" component={Profile} />
              <Route path="/app/createsigningprofile" component={CreateSigningProfile} />
              <Route path="/app/profiles" component={Profiles} />
              <Route path="/app/makesqueak" component={MakeSqueak} />
              <Route path="/app/lightning" component={Lightning} />
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
