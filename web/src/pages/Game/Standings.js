import React from 'react';

import StandingsTable from './StandingsTable';

class Standings extends React.Component {
  getGameSlug() {
    const { match } = this.props;
    return match.params.slug;
  }

  render() {
    return (
      <div>
        <h1>Standings Page</h1>
        <StandingsTable  slug={this.getGameSlug()} />
      </div>
    );
  }
}

export default Standings;
