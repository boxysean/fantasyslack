import React from 'react';
import PropTypes from 'prop-types';
import { Table } from 'react-bootstrap';
import _ from 'lodash';
import axios from 'axios';
import { connect } from 'react-redux';
import moment from 'moment';

class SortableTable extends React.Component {
  static propTypes = {
    table: PropTypes.array.isRequired,
    columnHeaders: PropTypes.array.isRequired,
  };

  constructor(props) {
    super(props);

    this.state = {
      activeTableColumnIndex: 0,
      reverse: false,
      players: [],
    };
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

  sortRows() {
    let rows = _.sortBy(this.props.table, this.props.columnHeaders[this.state.activeTableColumnIndex].key);

    if (this.state.reverse) {
      rows = _.reverse(rows);
    }

    return rows;
  }

  render() {
    return (
      <Table striped bordered>
        <thead>
          <tr>
            {this.props.columnHeaders.map((columnHeader, index) => (
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
          this.sortRows().map((row) =>
            <tr key={row.name}>
              {this.props.columnHeaders.map((column) =>
                <td key={row.name + "-" + column.key}>{row[column.key]}</td>
              )}
            </tr>
          )
        }
        </tbody>
      </Table>
    );
  }
}

export default SortableTable;
