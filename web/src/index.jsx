require("../node_modules/bootstrap/dist/css/bootstrap.min.css");

import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route } from 'react-router';

import { FSNav } from './components/navigation.js';
import { FSOverviewPage } from './pages/overview/';
import { FSStandingsPage } from './pages/standings';

var pages = [
    { name: 'Overview', slug: 'overview', app: FSOverviewPage },
    { name: 'Standings', slug: 'standings', app: FSStandingsPage },
    { name: 'Your Team', slug: 'your-team', app: undefined },
    { name: 'All Emailers', slug: 'all-emailers', app: undefined },
    { name: 'All Emails', slug: 'all-emails', app: undefined },
    { name: 'All Transactions', slug: 'all-transactions', app: undefined },
    { name: 'Rules/Help', slug: 'help', app: undefined }
];

export var App = React.createClass({
	render: function() {
        return (
            <div>
                <FSNav pages={pages} />
                {this.props.children}
            </div>
        );
	}
});

var router = (
    <Router>
        <Route path="/" component={App}>
            {pages.filter((page) => page.app !== undefined).map((page) =>
                <Route path={page.slug} component={page.app} />
            )}
        </Route>
    </Router>
);


ReactDOM.render(router, document.querySelector("#myApp"));
