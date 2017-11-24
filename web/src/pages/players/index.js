import React from 'react';

import { StandingsTable } from './StandingsTable';
// import { TeamStore } from './team';

export class FSPlayersPage extends React.Component {
    render() {
        return (
            <div>
                <h1>Players Page</h1>
                <StandingsTable />
            </div>
        );
    }
}
