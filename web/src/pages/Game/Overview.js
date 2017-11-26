import React from 'react';

class Overview extends React.Component {
  render() {
    const { match } = this.props;

    return (
      <div>
        <h2>Overview</h2>
        <p>Here we can put some information about the game!</p>
        <p>Slug: {match.params.slug}</p>
      </div>
    );
  }
}

export default Overview;
