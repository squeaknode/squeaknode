import React, { Suspense, lazy } from 'react'
import { Route, Switch, BrowserRouter, Redirect, withRouter } from 'react-router-dom'
import { StoreProvider } from './store/store'
import 'dotenv/config'
import './App.scss'
import Loader from './components/Loader'
import Nav from './components/Nav'
import Login from './components/Login'
import Signup from './components/Signup'
import Tweet from './components/Tweet'
import Profiles from './components/Profiles'
import Payments from './components/Payments'
import Peers from './components/Peers'
import Feed from './components/Feed'
import Notifications from './components/Notifications'
import Alerts from './components/Alerts'

const Home = lazy(() => import('./components/Home'))
const Profile = lazy(() => import('./components/Profile'))
const Peer = lazy(() => import('./components/Peer'))

const DefaultContainer = withRouter(({ history }) => {
  return (<div className="body-wrap">
    <main className="main">
      <div className={history.location.pathname.slice(0,9) !== '/messages' ? "middle-section ms-width" : "middle-section"}>
        <Route path="/" exact>
          <Redirect to="/app/home" />
        </Route>
        <Route path="/app/home" exact>
          <Home />
        </Route>
        <Route path="/app/profile/:username" exact>
          <Profile />
        </Route>
        <Route path="/app/peer/:network/:host/:port" exact>
          <Peer />
        </Route>
        <Route path="/app/tweet/:id" exact>
          <Tweet />
        </Route>
        <Route path="/app/profiles" exact>
          <Profiles/>
        </Route>
        <Route path="/app/payments" exact>
          <Payments/>
        </Route>
        <Route path="/app/peers" exact>
          <Peers/>
        </Route>
        <Route path="/app/notifications" exact>
          <Notifications/>
        </Route>
      </div>
        {history.location.pathname.slice(0,9) !== '/messages' &&
        <div className="right-section">
          <Feed/>
        </div>
         }
    </main>
    <nav className="header">
      <Nav />
    </nav>
  </div>)
});

function App() {
  return (
    <div className="dark-mode">
      <StoreProvider>
        <BrowserRouter>
          <Suspense fallback={<Loader />}>
            <Alerts />
            <Switch>
              <Route path="/login" exact>
                <Login />
              </Route>
              <Route path="/signup" exact>
                <Signup />
              </Route>
              <Route component={DefaultContainer} />
            </Switch>
          </Suspense>
        </BrowserRouter>
      </StoreProvider>
    </div>
  )
}

export default App
