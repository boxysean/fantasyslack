import React from 'react';
import ReactDOM from 'react-dom';

import { Form, FormGroup, ControlLabel, FormControl, HelpBlock, InputGroup, Button, Checkbox, Col, Jumbotron } from 'react-bootstrap';
import DateTimeField from 'react-bootstrap-datetimepicker';

var LeagueTitle = React.createClass({
    getInitialState: function() {
        return {
            value: ''
        };
    },

    getValidationState: function() {
        const length = this.state.value.length;
        if (length > 10) return 'success';
        else if (length > 5) return 'warning';
        else if (length > 0) return 'error';
    },

    handleChange: function(e) {
        this.setState({ value: e.target.value });
    },

    render: function() {
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
});

var SlackChannel = React.createClass({
    getInitialState: function() {
        return {
            value: ''
        };
    },

    getValidationState: function() {
        const length = this.state.value.length;
        if (length > 10) return 'success';
        else if (length > 5) return 'warning';
        else if (length > 0) return 'error';
    },

    handleChange: function(e) {
        this.setState({ value: e.target.value });
    },

    render: function() {
        return (
            <FormGroup controlId="formSlackChannel" validationState={this.getValidationState()}>
                <Col componentClass={ControlLabel} sm={2}>Slack Channel</Col>
                <Col sm={10}>
                    <FormControl
                        type="text"
                        value={this.state.value}
                        placeholder="#mychannel"
                        onChange={this.handleChange}
                    />
                    <HelpBlock>Know what's happening about the league in this channel and you'll be able to do any configuration about this league in this channel.</HelpBlock>
                </Col>
            </FormGroup>
        );
    }
});

var Players = React.createClass({
    getInitialState: function() {
        return {
            value: ''
        };
    },

    getValidationState: function() {
        const length = this.state.value.length;
        if (length > 10) return 'success';
        else if (length > 5) return 'warning';
        else if (length > 0) return 'error';
    },

    handleChange: function(e) {
        this.setState({ value: e.target.value });
    },

    render: function() {
        return (
            <FormGroup controlId="formPlayers" validationState={this.getValidationState()}>
                <Col componentClass={ControlLabel} sm={2}>Players</Col>
                <Col sm={10}>
                    <FormControl
                        type="text"
                        value={this.state.value}
                        placeholder="e.g., @jerry @elaine @kramer and @newman"
                        onChange={this.handleChange}
                    />
                    <HelpBlock>Comma-separated list of players in this league</HelpBlock>
                </Col>
            </FormGroup>
        );
    }
});

var EndDate = React.createClass({
    getInitialState: function() {
        return {
            value: ''
        };
    },

    getValidationState: function() {
        const length = this.state.value.length;
        if (length > 10) return 'success';
        else if (length > 5) return 'warning';
        else if (length > 0) return 'error';
    },

    handleChange: function(e) {
        this.setState({ value: e.target.value });
    },

    render: function() {
        return (
            <FormGroup controlId="formEndDate" validationState={this.getValidationState()}>
                <Col componentClass={ControlLabel} sm={2}>End Date</Col>
                <Col sm={10}>
                    <DateTimeField />
                    <HelpBlock>Exactly when this league will end</HelpBlock>
                </Col>
            </FormGroup>
        );
    }
});

var NumberOfTeamMembers = React.createClass({
    getInitialState: function() {
        return {
            value: ''
        };
    },

    getValidationState: function() {
        const length = this.state.value.length;
        if (length > 10) return 'success';
        else if (length > 5) return 'warning';
        else if (length > 0) return 'error';
    },

    handleChange: function(e) {
        this.setState({ value: e.target.value });
    },

    render: function() {
        return (
            <FormGroup controlId="formPlayers" validationState={this.getValidationState()}>
                <Col componentClass={ControlLabel} sm={2}>Number of Team Members</Col>
                <Col sm={10}>
                    <FormControl
                        type="text"
                        value={this.state.value}
                        placeholder="e.g., 2"
                        onChange={this.handleChange}
                    />
                    <HelpBlock>It's good to have a number that complements the size of your Slack, say total number of Slackers / number of players / 2</HelpBlock>
                </Col>
            </FormGroup>
        );
    }
});

var ScoringCategories = React.createClass({
    getInitialState: function() {
        return {
            value: ''
        };
    },

    getValidationState: function() {
        const length = this.state.value.length;
        if (length > 10) return 'success';
        else if (length > 5) return 'warning';
        else if (length > 0) return 'error';
    },

    handleChange: function(e) {
        this.setState({ value: e.target.value });
    },

    render: function() {
        return (
            <FormGroup controlId="formScoringCategories" validationState={this.getValidationState()}>
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
});

export var FSGamePage = React.createClass({
    render: function() {
        return (
            <div>
                <Jumbotron>
                    <h1>Game Configuration</h1>
                    <p>So you want to start a game of Fantasy Slack, huh? Fill out this form so we can get you started.</p>
                </Jumbotron>
                <Form horizontal>
                    <LeagueTitle />
                    <SlackChannel />
                    <Players />
                    <EndDate />
                    <NumberOfTeamMembers />
                    <ScoringCategories />
                    <Col smOffset={2}>
                        <Button type="submit">
                            Let's Play!
                        </Button>
                    </Col>
                </Form>
            </div>
        );
    }
});

