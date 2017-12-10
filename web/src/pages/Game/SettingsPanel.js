/* eslint no-unused-vars: "off" */

import React from 'react';
import PropTypes from 'prop-types';

import { Form, FormGroup, ControlLabel, FormControl, HelpBlock, Button, Checkbox, Col, Jumbotron } from 'react-bootstrap';

class LeagueTitle extends React.Component {
    render() {
        return (
            <h1>League Title</h1>
        );
    }
}

class Contacts extends React.Component {
    getInitialState() {
        return {
            value: ''
        };
    }

    getValidationState() {
        const length = this.state.value.length;
        if (length > 10) return 'success';
        else if (length > 5) return 'warning';
        else if (length > 0) return 'error';
    }

    handleChange(e) {
        this.setState({ value: e.target.value });
    }

    render() {
        return (
            <FormGroup controlId="formLeagueTitle" validationState={this.getValidationState()}>
                <Col componentClass={ControlLabel} sm={2}>League Title</Col>
                <Col sm={10}>
                    <FormControl
                        type="text"
                        value={this.state.value}
                        placeholder="e.g., Cup of the Century"
                        onChange={this.handleChange}
                    />
                    <HelpBlock></HelpBlock>
                </Col>
            </FormGroup>
        );
    }
}

class SlackChannel extends React.Component {
    render() {
        return (
          <FormGroup controlId="formSlackChannel">
            <Col componentClass={ControlLabel} sm={2}>Slack Channel</Col>
            <Col sm={10}>
              <FormControl
                type="text"
                defaultValue={this.props.channel}
                placeholder="#mychannel"
                onChange={this.handleChange}
              />
              <HelpBlock>Know what's happening about the league in this channel and you'll be able to do any configuration about this league in this channel.</HelpBlock>
            </Col>
          </FormGroup>
        );
    }
}

class Managers extends React.Component {
    render() {
      return (
        <FormGroup controlId="formPlayers">
          <Col componentClass={ControlLabel} sm={2}>Managers</Col>
          <div className="col-sm-6">
            {this.props.managers.map((manager) => {
              return (
                <div className="input-group" key={manager.name}>
                  <span className="form-control">{manager.name}</span>
                  <span className="input-group-btn">
                    {
                      manager.role === 'admin' ?
                        <button className="btn btn-danger">Remove Admin</button>
                      : <button className="btn btn-default">Make Admin</button>
                    }
                    <button className="btn btn-danger">Remove</button>
                  </span>
                </div>
              )
            })}

            <div className="input-group">
              <input type="text" className="form-control" placeholder="User name" />
              <span class="input-group-btn">
                <button class="btn btn-success" type="button">Add</button>
              </span>
            </div>

            <HelpBlock>List of Managers in this league</HelpBlock>
          </div>
        </FormGroup>
      );
    }
}

class EndDate extends React.Component {
    render() {
      return (
        <FormGroup controlId="formEndDate">
          <Col componentClass={ControlLabel} sm={2}>End Date</Col>
          <Col sm={10}>
            <FormControl
              type="text"
              placeholder="2018-01-09 05:00:00"
              onChange={this.handleChange}
              defaultValue={this.props.end.local().format()}
            />
            <HelpBlock>Exactly when this league will end</HelpBlock>
          </Col>
        </FormGroup>
      );
    }
}

class StartDate extends React.Component {
    render() {
      return (
        <FormGroup controlId="formStartDate">
          <Col componentClass={ControlLabel} sm={2}>Start Date</Col>
          <Col sm={10}>
            <FormControl
              type="text"
              placeholder="2017-12-09 05:00:00"
              defaultValue={this.props.start.local().format()} />
            <HelpBlock>Exactly when this league will start</HelpBlock>
          </Col>
        </FormGroup>
      );
    }
}
class PlayersPerTeam extends React.Component {
    render() {
      return (
        <FormGroup controlId="formPlayers">
          <Col componentClass={ControlLabel} sm={2}>Players Per Team</Col>
          <Col sm={10}>
            <FormControl
              type="text"
              placeholder="e.g., 2"
              defaultValue={this.props.playersPerTeam} />
            <HelpBlock>It's good to have a number that complements the size of your Slack, say total number of Slackers / number of players / 2</HelpBlock>
          </Col>
        </FormGroup>
      );
    }
}

class ScoringCategories extends React.Component {
  render() {
    return (
      <FormGroup controlId="formScoringCategories">
        <Col componentClass={ControlLabel} sm={2}>Scoring Categories</Col>
        <Col sm={10}>
          <Checkbox>Loud Mouth</Checkbox>
          <Checkbox>Reactions</Checkbox>
          <Checkbox>Chatty Kathy</Checkbox>
          <Checkbox>Emoji Master</Checkbox>
          <Checkbox>Shouter</Checkbox>
          <Checkbox>GIF Ninja</Checkbox>
          <Checkbox>Editor</Checkbox>
        </Col>
      </FormGroup>
    );
  }
}

class SettingsPanel extends React.Component {
  static propTypes = {
    game: PropTypes.object.isRequired,
  };

  render() {
    return (
      <div>
        <Jumbotron>
          <h1>Settings</h1>
          <p>So you want to start a game of Fantasy Slack, huh? Fill out this form so we can get you started.</p>
        </Jumbotron>
        <Form horizontal>
          <LeagueTitle />
          <SlackChannel channel={this.props.game.channel} />
          <Managers managers={this.props.game.managers} />
          <StartDate start={this.props.game.start} />
          <EndDate end={this.props.game.end} />
          <PlayersPerTeam playersPerTeam={this.props.game.playersPerTeam} />
          <ScoringCategories />
          <Col smOffset={2}>
            <Button type="submit" className="btn btn-primary">
              Save
            </Button>
          </Col>
        </Form>
      </div>
    );
  }
}

export default SettingsPanel;
