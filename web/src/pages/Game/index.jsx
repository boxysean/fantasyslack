import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import Players from './Players';
import Standings from './Standings';
import Overview from './Overview';
import { Route } from 'react-router-dom';
import { withRouter } from 'react-router';

class Game extends React.Component {
  static propTypes = {
    name: PropTypes.string,
    match: PropTypes.object.isRequired,
  };

  static defaultProps = {
    // slug: 'sluggg',
  };

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
              <Link className="nav-link" to={match.url + "/standings"}>Standings</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to={match.url + "/players"}>Players</Link>
            </li>
          </ul>
        </nav>

        <div className="container">
          <Route exact path="/game/:slug" component={Overview} />
          <Route exact path="/game/:slug/standings" component={Standings} />
          <Route exact path="/game/:slug/players" component={Players} />
        </div>
      </div>
    );
  }
}

export default withRouter(Game);
