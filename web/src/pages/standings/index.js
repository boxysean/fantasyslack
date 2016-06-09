import React from 'react';
import ReactDOM from 'react-dom';

import { StandingsTable } from './table';
import { TeamStore } from '../../stores/team';

export var FSStandingsPage = React.createClass({
    render: function() {
        return (
            <div>
                <h1>Standings Page</h1>
                <StandingsTable teams={TeamStore.DATA.teams} />
            </div>
        );
    }
});
