import React from 'react';
import {
  HashRouter, Route, Switch, Redirect,
} from 'react-router-dom';

// components
import Layout from './Layout';

// pages
import Error from '../pages/error';
import Login from '../pages/login';

// context
// import { useUserState } from '../context/UserContext';

export default function App() {
  // global
  // const { isAuthenticated } = useUserState();

  return (
    <HashRouter>
      <Switch>
        <Route exact path="/" render={() => <Redirect to="/app/timeline" />} />
        <Route
          exact
          path="/app"
          render={() => <Redirect to="/app/timeline" />}
        />
        <PublicRoute path="/app" component={Layout} />
        //
        {' '}
        <PublicRoute path="/login" component={Login} />
        <Route component={Error} />
      </Switch>
    </HashRouter>
  );

  // #######################################################################

  // function PrivateRoute({ component, ...rest }) {
  //   return (
  //     <Route
  //       {...rest}
  //       render={props =>
  //         isAuthenticated ? (
  //           React.createElement(component, props)
  //         ) : (
  //           <Redirect
  //             to={{
  //               pathname: "/login",
  //               state: {
  //                 from: props.location,
  //               },
  //             }}
  //           />
  //         )
  //       }
  //     />
  //   );
  // }

  function PublicRoute({ component, ...rest }) {
    return (
      <Route
        {...rest}
        render={(props) => React.createElement(component, props)}
      />
    );
  }
}
