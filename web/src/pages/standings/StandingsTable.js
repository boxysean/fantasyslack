import PropTypes from 'prop-types';
import React from 'react';

import { Table } from 'react-bootstrap';

var sortBy = require('sort-by');

export class StandingsTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeTableColumnIndex: 1
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
        var newIndex;

        if (index+1 === this.state.activeTableColumnIndex) {
            newIndex = -index - 1;
        } else {
            newIndex = 1 + index;
        }

        this.setState({
            activeTableColumnIndex: newIndex
        });
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
                {this.props.teams.sort(sortBy(sortModifier + this.columnHeaders[activeIndex].key)).map((team) =>
                    <tr>
                        <td>{team.rank}</td>
                        <td>{team.name}</td>
                        <td>{team.points}</td>
                    </tr>
                )}
                </tbody>
            </Table>
        );
    }
}

StandingsTable.propTypes = {
    teams: PropTypes.arrayOf(PropTypes.object)
};

StandingsTable.columnHeaders = [
    
];
