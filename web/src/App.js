import React, { Component } from 'react';
import {
    BrowserRouter as Router,
    Route,
    Link,
    Redirect,
} from 'react-router-dom';
import { Confirm } from 'react-cognito';
import { Panel } from 'react-bootstrap';

import './App.css';

import { FSGamePage } from './pages/game';
import { FSStandingsPage } from './pages/standings';
import { FSPlayersPage } from './pages/players';
import RegistrationForm from './auth/RegistrationForm';
import ConfirmForm from './auth/ConfirmForm';
import Login from './pages/login';
import LoginLogoutButton from './components/LoginLogoutButton';


const PublicRoute = ({ component: Component, authStatus, ...rest}) => (
    <Route {...rest} render={props => authStatus === false
        ? ( <Component {...props} /> ) : (<Redirect to="/main" />)
    } />
)


const PrivateRoute = ({ component: Component, authStatus, ...rest}) => (
    <Route {...rest} render={props => authStatus === false
        ? ( <Redirect to="/login" /> ) : ( <Component {...props} /> )
    } />
)


class App extends Component {
  constructor() {
    super();
    this.state = {
      authStatus: false,
    };
  }

  static defaultProps = {
    authStatus: false,
  };

  validateUserSession() {
    if(sessionStorage.getItem('isLoggedIn') === 'true'){
      this.setState(() => {
        return {
          authStatus: true
        }
      })
    } else {
      this.setState(() => {
        return {
          authStatus: false
        }
      })
    }
  }

  render() {
    return (
      <Router>
        <div>
          <nav className="navbar navbar-default navbar-static-top">
            <div className="container-fluid">
              <div className="navbar-header">
                <button className="navbar-toggle collapsed" type="button" data-toggle="collapse" data-target="#navbar" aria-controls="navbarNav">
                  <span className="navbar-toggler-icon"></span>
                </button>
                <Link to="/" className="navbar-brand">Fantasy Slack</Link>
              </div>

              <div className="collapse navbar-collapse">
                <ul className="nav navbar-nav">
                  <li className="nav-item active">
                    <Link to="/game">Game</Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/standings">Standings</Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/players">Players</Link>
                  </li>
                </ul>
                <ul className="nav navbar-nav navbar-right">
                  <li className="nav-item">
                    <Link to="/register">Register</Link>
                  </li>
                  <LoginLogoutButton />
                </ul>
              </div>
            </div>
          </nav>

          <div className="container">
            <PublicRoute authStatus={this.state.authStatus} path='/register' exact component={registrationForm} />
            <PublicRoute authStatus={this.state.authStatus} path='/register/confirm' exact component={confirmForm} />
            <PublicRoute authStatus={this.state.authStatus} exact path="/" component={Home} />
            <PublicRoute authStatus={this.state.authStatus} path="/game" component={FSGamePage} />
            <PublicRoute authStatus={this.state.authStatus} path="/standings" component={FSStandingsPage} />
            <PublicRoute authStatus={this.state.authStatus} path="/players" component={FSPlayersPage} />
            <Route path="/login" component={Login} />
          </div>
        </div>
      </Router>
    );
  }
};


          // <Route render={() => (<Redirect to="/login" />)} />
          // <PublicRoute authStatus={this.state.authStatus} path='/login' exact component={LoginForm} />


const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
);

const registrationForm = () => (
  <Panel className="registration-form">
    <h2>Register an account on Fantasy Slack</h2>
    <div className="row">
      <div className="col-md-4">
        <RegistrationForm />
      </div>
    </div>
  </Panel>
);

const confirmForm = () => (
  <Panel className="confirm-form">
    <p>A confirmation code has been sent to your email address</p>
    <div className="row">
      <div className="col-md-4">
        <Confirm>
          <ConfirmForm />
        </Confirm>
      </div>
    </div>
  </Panel>
);

export default App;
