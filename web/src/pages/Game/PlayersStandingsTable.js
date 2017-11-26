import React from 'react';
import axios from 'axios';
import _ from 'lodash';

import { Table } from 'react-bootstrap';

export default class PlayersStandingsTable extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        activeTableColumnIndex: 0,
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
        console.log("Clicked! " + index);

        if (index === this.state.activeTableColumnIndex) {
            this.setState({
                'reverse': !this.state.reverse,
            });
        } else {
            this.setState({
                'reverse': false,
                'activeTableColumnIndex': index,
            });
        }
    }

    sortPlayers() {
        let players = _.sortBy(this.state.players, this.columnHeaders[this.state.activeTableColumnIndex].key);

        if (this.state.reverse) {
            players = _.reverse(players);
        }

        return players;
    }

    render() {
        return (
            <Table striped bordered>
                <thead>
                    <tr>
                        {this.columnHeaders.map((columnHeader, index) => (
                            <th onClick={this.tableColumnHeaderClickHandler.bind(this, index)}
                                className={this.state.activeTableColumnIndex === index ? "TableColumnHeader-active" : "TableColumnHeader-active"}
                                key={columnHeader.title}>
                                    {columnHeader.title}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                {
                    this.sortPlayers().map((player) =>
                    <tr key={player.name}>
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
    axios.get("http://localhost:5000/api/v1/game/" + this.props.slug + "/players")
      .then(res => {
        this.setState({
          players: res.data
        });
      }
    );
  }
}
