import React from 'react';
import ReactDOM from 'react-dom';

import { OverviewTable } from './table';
import { TeamStore } from '../../stores/team';

export var FSOverviewPage = React.createClass({
    render: function() {
        return (
            <div>
                <h1>Overview Page</h1>
                <OverviewTable teams={TeamStore.DATA.teams} />
            </div>
        );
    }
});
