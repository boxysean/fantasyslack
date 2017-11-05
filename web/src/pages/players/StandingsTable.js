import PropTypes from 'prop-types';
import React from 'react';
import axios from 'axios';
import _ from 'lodash';

import { Table } from 'react-bootstrap';

var sortBy = require('sort-by');

export class StandingsTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeTableColumnIndex: 1,
            reverse: false,
            players: []
        };

        this.columnHeaders = [
            {
                title: 'Rank',
                key: 'rank'
            },
            {
                title: 'Name',
                key: 'name',
            },
            {
                title: 'Points',
                key: 'points'
            },
        ];
    }

    tableColumnHeaderClickHandler(index) {
        var newIndex = this.state.activeTableColumnIndex;
        var reverse = this.state.reverse;

        if (index+1 === this.state.activeTableColumnIndex) {
            reverse = !reverse;
        } else {
            newIndex = index;
            reverse = false;
        }

        this.setState({
            activeTableColumnIndex: newIndex,
            reverse: reverse
        });
    }

    sortPlayers() {
        let players = _.sortBy(this.state.players, this.columnHeaders[this.state.activeTableColumnIndex].key);
        
        if (this.state.reverse) {
            players = _.reverse(players);
        }

        return players;
    }

    render() {
        var sortModifier = this.state.activeTableColumnIndex < 0 ? '-' : '';
        var activeIndex = Math.abs(this.state.activeTableColumnIndex)-1;

        return (
            <Table striped bordered>
                <thead>
                    <tr>
                        {this.columnHeaders.map((columnHeader, index) => (
                            <th onClick={this.tableColumnHeaderClickHandler.bind(this, index)}
                                className={activeIndex === index && "TableColumnHeader-active"}>
                                    {columnHeader.title}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                {
                    this.sortPlayers().map((player) =>
                    <tr>
                        <td>{player.rank}</td>
                        <td>{player.name}</td>
                        <td>{player.points}</td>
                    </tr>
                    )
                }
                </tbody>
            </Table>
        );
    }

    componentDidMount() {
        axios.get("http://localhost:5000/api/v1/players")
            .then(res => {
                this.setState({
                    players: res.data
                });
            });
    }
}
