import React from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

class GameList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      games: []
    };
  }

  render() {
    return (
      <ul>
        {this.state.games.map(function(game) {
          return <Link key={game.id} to={"/game/" + game.slug}>{game.name}</Link>
        })}
      </ul>
    );
  }

  componentDidMount() {
    axios.get("http://localhost:5000/api/v1/games")
      .then(res => {
        this.setState({
          games: res.data
        });
      }
    );
  }
}


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
            <li><Link to="/game/fake-game">Fake Game</Link></li>
            <li><Link to="/game/Game2">Game2</Link></li>
          </ul>
        </ul>

        <p>If you are an administrator, you can do even more! All active games:</p>
        <GameList />
      </div>
    );
  }
}

export default Home;
