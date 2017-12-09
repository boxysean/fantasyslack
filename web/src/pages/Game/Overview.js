import React from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import _ from 'lodash';
import moment from 'moment';

class Overview extends React.Component {
  static propTypes = {
    game: PropTypes.object,
  };

  render() {
    if (this.props.game) {
      return (
        <div>
          <h2>Overview</h2>
          <p>{
            (this.props.game.hasEnded) ? "The game has ended!" :
              (this.props.game.hasStarted) ? "The game is underway!" :
              "The game has yet to begin!"
          }</p>
          <p>Start: {this.props.game.start.local().format("dddd, MMMM Do YYYY, h:mm a")}</p>
          <p>End: {this.props.game.end.local().format("dddd, MMMM Do YYYY, h:mm a")}</p>
          <p>Draft Start: {this.props.game.draft.start.local().format("dddd, MMMM Do YYYY, h:mm a")}</p>
          <p>Admins:</p>
          <ul>
            {this.props.game.admins.map((admin) =>
              <li key={admin}>{admin}</li>
            )}
          </ul>
          <p>Teams:</p>
          <ul>
            {this.props.game.teams.map((team) =>
              <li key={team}>{team}</li>
            )}
          </ul>
          <p>Categories:</p>
          <ul>
            {_.keys(this.props.game.categories).map((category) =>
              <li key={category}>{category}</li>
            )}
          </ul>
        </div>
      );
    } else {
      return null;
    }
  }
}

export default Overview;
