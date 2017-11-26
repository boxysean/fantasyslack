import React from 'react';

import { StandingsTable } from './StandingsTable';
import { TeamStore } from './team';

class Standings extends React.Component {
  render() {
    return (
      <div>
        <h1>Standings Page</h1>
        <StandingsTable teams={TeamStore.DATA.teams} />
      </div>
    );
  }
}

export default Standings;
