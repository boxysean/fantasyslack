import React from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import _ from 'lodash';

class Overview extends React.Component {
  static propTypes = {
    slug: PropTypes.string.isRequired,
  };

  constructor(props) {
    super(props);

    this.state = {
      game: {
        teams: [],  // <-- need this pre-mount
        categories: [],
        draft: {},
      },
    };
  }

  render() {
    return (
      <div>
        <h2>Overview</h2>
        <p>Start: {this.state.game.start}</p>
        <p>End: {this.state.game.end}</p>
        <p>Draft Start: {this.state.game.draft.start}</p>
        <p>Teams:</p>
        <ul>
          {this.state.game.teams.map((team) =>
            <li>{team}</li>
          )}
        </ul>
        <p>Categories:</p>
        <ul>
          {_.keys(this.state.game.categories).map((category) =>
            <li>{category}</li>
          )}
        </ul>
      </div>
    );
  }

  componentDidMount() {
    axios.get("http://localhost:5000/api/v1/games/" + this.props.slug)
      .then(res => {
        this.setState({
          game: res.data
        });
      }
    );
  }
}

export default Overview;
