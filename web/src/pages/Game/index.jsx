import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import Players from './Players';
import Teams from './Teams';
import Overview from './Overview';
import { Route } from 'react-router-dom';
import { withRouter } from 'react-router';
import moment from 'moment';
import axios from 'axios';

class Game extends React.Component {
  static propTypes = {
    name: PropTypes.string,
    match: PropTypes.object.isRequired,
  };

  constructor(props) {
    super(props);

    this.state = {
      game: null,
    };
  }

  render() {
    const { match } = this.props;

    return (
      <div>
        <nav className="navbar navbar-light bg-faded">
          <ul className="nav navbar-nav">
            <li className="nav-item active">
              <Link className="navbar-brand nav-link" to={match.url}>{match.params.slug}</Link>
            </li>
            <li className="nav-item active">
              <Link className="nav-link" to={match.url + "/teams"}>Teams</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to={match.url + "/players"}>Players</Link>
            </li>
          </ul>
        </nav>

        <div className="container">
          <Route exact path="/game/:slug" render={() =>
            <Overview game={this.state.game} />
          } />
          <Route exact path="/game/:slug/teams" render={() =>
            <Teams game={this.state.game} />
          } />
          <Route exact path="/game/:slug/players" component={() =>
            <Players game={this.state.game} />
          } />
        </div>
      </div>
    );
  }

  componentDidMount() {
    const { match } = this.props;

    axios.get("http://localhost:5000/api/v1/games/" + match.params.slug)
      .then(res => {
        res.data.start = moment(res.data.start);
        res.data.end = moment(res.data.end);
        res.data.draft.start = moment(res.data.draft.start);

        res.data.hasStarted = moment() > res.data.start;
        res.data.hasEnded = moment() > res.data.end;
        res.data.draft.hasStarted = moment() > res.data.draft.start;

        this.setState({
          game: res.data,
        });
      }
    );
  }
}

export default withRouter(Game);
