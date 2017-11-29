import React from 'react';
import axios from 'axios';

class Overview extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      game: {},
    };
  }

  render() {
    const { match } = this.props;

    return (
      <div>
        <h2>Overview</h2>
        <p>Here we can put some information about the game!</p>
        <p>Slug: {match.params.slug}</p>
        <p>Info: {JSON.stringify(this.state.game)}</p>
      </div>
    );
  }

  componentDidMount() {
    axios.get("http://localhost:5000/api/v1/games/" + this.props.match.params.slug)
      .then(res => {
        this.setState({
          game: res.data
        });
      }
    );
  }
}

export default Overview;
