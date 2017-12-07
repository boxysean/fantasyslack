import React from 'react';
import { Table } from 'react-bootstrap';
import _ from 'lodash';
import axios from 'axios';
import { connect } from 'react-redux';

class BasePlayersStandingsTable extends React.Component {
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
        {
          title: 'Current Team',
          key: 'team'
        },
      ];
    }

    tableColumnHeaderClickHandler(index) {
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
                        <td>{player.team}</td>
                    </tr>
                    )
                }
                </tbody>
            </Table>
        );
    }

  componentDidMount() {
    const jwtConfig = {
      headers: {
        "accessToken": this.props.accessToken,
        "idToken": this.props.idToken,
      },
    };

    axios.get("http://localhost:5000/api/v1/games/" + this.props.slug + "/players", jwtConfig)
      .then(res => {
        this.setState({
          players: res.data
        });
      }
    );
  }
}

const mapStateToProps = function(state) {
  let accessToken = '';

  try {
    accessToken = state.cognito.user.signInUserSession.accessToken.jwtToken;
  } catch (e) {

  }

  let idToken = '';

  try {
    idToken = state.cognito.user.signInUserSession.idToken.jwtToken;
  } catch (e) {

  }

  return {
    accessToken: accessToken,
    idToken: idToken,
    cognito: state.cognito,
  }
};
const PlayersStandingsTable = connect(mapStateToProps, null)(BasePlayersStandingsTable);

export default PlayersStandingsTable;
