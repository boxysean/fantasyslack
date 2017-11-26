import React from 'react';

import PlayersStandingsTable from './PlayersStandingsTable';

class Players extends React.Component {
  getGameSlug() {
    const { match } = this.props;
    return match.params.slug;
  }

  render() {
    return (
      <div>
        <h1>Players</h1>
        <PlayersStandingsTable slug={this.getGameSlug()} />
      </div>
    );
  }
}

export default Players;
