import React from 'react';
import { Table } from 'react-bootstrap';
import _ from 'lodash';
import axios from 'axios';
import { connect } from 'react-redux';

class BaseStandingsTable extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        activeTableColumnIndex: 0,
        reverse: false,
        standings: []
      };
    }

    getColumnHeaders() {
      return [
        {
          title: 'Rank',
          key: 'rank'
        },
        {
          title: 'Team',
          key: 'team',
        },
        {
          title: 'Score',
          key: 'score',
        },
        {
          title: 'Points',
          key: 'points'
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

    sortStandings() {
      let standings = _.sortBy(this.state.standings, this.getColumnHeaders()[this.state.activeTableColumnIndex].key);

      if (this.state.reverse) {
        standings = _.reverse(standings);
      }

      return standings;
    }

    render() {
        return (
            <Table striped bordered>
                <thead>
                    <tr>
                        {this.getColumnHeaders().map((columnHeader, index) => (
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
                  this.sortStandings().map((row) =>
                    <tr key={row.team}>
                      {this.getColumnHeaders().map((column) =>
                        <td key={row.team + "-" + column.key}>{row[column.key]}</td>
                      )}
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

    axios.get("http://localhost:5000/api/v1/games/" + this.props.slug, jwtConfig)
      .then(res => {
        this.setState({
          standings: res.data.standings
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

const StandingsTable = connect(mapStateToProps, null)(BaseStandingsTable);

export default StandingsTable;
