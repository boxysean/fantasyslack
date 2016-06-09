import React from 'react';
import ReactDOM from 'react-dom';

import { FormGroup, ControlLabel, FormControl, HelpBlock } from 'react-bootstrap';

export var FSGamePage = React.createClass({
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
            <form>
                <FormGroup
                    controlId="formBasicText"
                    validationState={this.getValidationState()}
                >
                    <ControlLabel>Working example with validation</ControlLabel>
                    <FormControl
                        type="text"
                        value={this.state.value}
                        placeholder="Enter text"
                        onChange={this.handleChange}
                    />
                    <HelpBlock>Validation is based on string length.</HelpBlock>
                </FormGroup>
            </form>
        );
    }
});



/*

*/