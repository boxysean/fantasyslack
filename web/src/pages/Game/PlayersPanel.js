import React from 'react';
import PropTypes from 'prop-types';
import { ButtonToolbar, ToggleButtonGroup, ToggleButton } from 'react-bootstrap';
import axios from 'axios';
import { connect } from 'react-redux';
import moment from 'moment';
import _ from 'lodash';

import SortableTable from './SortableTable';

class BasePlayersPanel extends React.Component {
  static propTypes = {
    game: PropTypes.object,
  };

  constructor(props) {
    super(props);

    this.state = {
      timePeriodDays: 30,
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
      }
    ];

    if (!this.props.game.draft.hasStarted) {
      const updateDraftOrder = _.debounce((player, order) => {
        const config = {
          headers: {
            accessToken: this.props.accessToken,
            idToken: this.props.idToken,
          },
        };

        const data = {
          'draftOrder': [
            {
              'player': player,
              'order': order,
            }
          ]
        };

        axios.put("http://localhost:5000/api/v1/games/" + this.props.game.slug + "/teams/team-unicorn", data, config)
          .then(res => {
            // TODO: fading checkmark ya
            // TODO: or fading x :(
          }
        );
      }, 500);

      const putIt = (event, rowName, columnKey) => {
        updateDraftOrder(rowName, _.parseInt(event.target.value));
      };

      this.columnHeaders.push({
        title: 'Your Draft Order',
        key: 'draftOrder',
        cellGenerator: (value, rowName, columnKey) => {
          return (
            <input
              type="text"
              defaultValue={value || undefined}
              onChange={_.partial(putIt, _, rowName, columnKey)} />
          );
        },
      });
    }
  }

  updateTimePeriodDays(days) {
    this.setState({
      timePeriodDays: days,
    }, () => {
      this.rerequest();
    });
  }

  render() {
    if (this.state.data) {
      return (
        <div>
          <h1>Players</h1>
          <h3>Time period</h3>
          <ButtonToolbar>
            <ToggleButtonGroup type="radio" name="timePeriodDays" defaultValue={this.state.timePeriodDays}>
              <ToggleButton onClick={this.updateTimePeriodDays.bind(this, 30)} value={30}>Last 30 Days</ToggleButton>
              <ToggleButton onClick={this.updateTimePeriodDays.bind(this, 7)} value={7}>Last 7 Days</ToggleButton>
              <ToggleButton onClick={this.updateTimePeriodDays.bind(this, 1)} value={1}>Last 24 Hours</ToggleButton>
            </ToggleButtonGroup>
          </ButtonToolbar>
          <i>Data collection began: xyz date</i>
          <br />
          <br />
          <SortableTable
            table={this.state.data.players}
            columnHeaders={this.columnHeaders}
          />
        </div>
      );
    } else {
      return null;
    }
  }

  componentDidMount() {
    this.rerequest();
  }

  rerequest() {
    console.log('Rerequest!');

    const requestParams = {
      headers: {
        accessToken: this.props.accessToken,
        idToken: this.props.idToken,
      },
      params: {
        start: moment.utc().subtract(this.state.timePeriodDays, 'days').format(),
        end: moment.utc().format(),
      }
    };

    axios.get("http://localhost:5000/api/v1/games/" + this.props.game.slug + "/players", requestParams)
      .then(res => {
        this.setState({
          data: res.data
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
const PlayersPanel = connect(mapStateToProps, null)(BasePlayersPanel);

export default PlayersPanel;
