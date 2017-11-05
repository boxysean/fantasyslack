import React, { Component } from 'react';
import {
    BrowserRouter as Router,
    Route,
    Link,
} from 'react-router-dom';

import './App.css';


import { FSGamePage } from './pages/game';
import { FSStandingsPage } from './pages/standings';
import { FSPlayersPage } from './pages/players';

class App extends Component {
  render() {
    return (
      <Router basename="/fantasyslack">
        <div>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/game">Game</Link></li>
            <li><Link to="/standings">Standings</Link></li>
            <li><Link to="/players">Players</Link></li>
          </ul>

          <hr/>

          <Route exact path="/" component={Home}/>
          <Route path="/game" component={FSGamePage}/>
          <Route path="/standings" component={FSStandingsPage}/>
          <Route path="/players" component={FSPlayersPage}/>
        </div>
      </Router>
    );
  }
}

const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
)

export default App;
