import React from 'react';
import PropTypes from 'prop-types';

import StandingsTable from './StandingsTable';

class Teams extends React.Component {
  static propTypes = {
    game: PropTypes.object,
  };

  render() {
    if (this.props.game) {
      return (
        <div>
          <h1>Teams</h1>
          <StandingsTable slug={this.props.game.slug} />
        </div>
      );
    } else {
      return null;
    }
  }
}

export default Teams;
