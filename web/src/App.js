import './App.css';

import { Link, Redirect, Route, BrowserRouter as Router } from 'react-router-dom';

import { FSGamePage } from './pages/NewGame';
import Home from './pages/Home';
import Login from './pages/Login';
import LoginLogoutButton from './components/LoginLogoutButton';
import React from 'react';
import Register from './pages/Register';
import Verify from './pages/Verify';
import Game from './pages/Game';

class App extends React.Component {
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
{/*}                <ul className="nav navbar-nav">
                  <li className="nav-item active">
                    <Link to="/standings">Standings</Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/players">Players</Link>
                  </li>
                </ul> */}
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
            <Route exact path="/register" exact component={Register} />
            <Route exact path="/verify" exact component={Verify} />
            <Route exact path="/" component={Home} />
            <Route exact path="/new-game" component={FSGamePage} />
            <Route path="/game/:slug" component={Game} />
            <Route exact path="/login" component={Login} />
          </div>
        </div>
      </Router>
    );
  }
};

export default App;
