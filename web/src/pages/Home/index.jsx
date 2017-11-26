import React from 'react';
import { Link } from 'react-router-dom';

class Home extends React.Component {
  render() {
    return (
      <div>
        <h2>Welcome to Fantasy Slack!</h2>

        <p>If you are not logged-in or registered, render a button to log in register</p>
        <ul>
          <li><Link to="/register">Register</Link></li>
          <li><Link to="/login">Login</Link></li>
        </ul>

        <p>Otherwise, here's what you can do:</p>
        <ul>
          <li><Link to='/new-game'>Create a New Game</Link></li>
          <li>Your active games:</li>
          <ul>
            <li><Link to="/game/sluggg">sluggg</Link></li>
            <li><Link to="/game/Game2">Game2</Link></li>
          </ul>
        </ul>

        <p>If you are an administrator, you can do even more! All active games:</p>
        <ul>
          <li><Link to="/game/sluggg">sluggg</Link></li>
          <li><Link to="/game/Game2">Game2</Link></li>
          <li><Link to="/game/secretone">secretone</Link></li>
        </ul>
      </div>
    );
  }
}

export default Home;
