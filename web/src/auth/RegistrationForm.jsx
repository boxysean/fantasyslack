import React from 'react';
import PropTypes from 'prop-types';
import { registerUser } from 'react-cognito';
import { withRouter } from 'react-router';

import { FieldGroup } from '../components/Form';


class RegistrationForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: '',
      password: '',
      email: '',
    };
  }

  static propTypes = {
    history: PropTypes.object.isRequired,
  }

  onSubmit = (event) => {
    const { store } = this.context;
    const state = store.getState();
    event.preventDefault();
    console.log("State!", this.state.email, this.state.password);
    registerUser(state.cognito.userPool, state.cognito.config, this.state.email, this.state.password, {}).then(
      (action) => {
        console.log("Action! " + action);
        store.dispatch(action);
        this.props.history.push('/register/confirm');
      },
      (error) => {
        this.setState({error: error});
      }
    );
  }

  changePassword = (event) => {
    this.setState({ password: event.target.value });
  }

  changeEmail = (event) => {
    this.setState({ email: event.target.value });
  }

  render = () => (
    <form onSubmit={this.onSubmit}>
      <div>{this.state.error.toString()}</div>

      <FieldGroup
        type="email"
        id="email"
        placeholder="email"
        label="Email"
        onChange={this.changeEmail}
        required />
      
      <FieldGroup
        type="password"
        placeholder="password"
        label="Password"
        onChange={this.changePassword}
        required />
      
      <button type="submit" className="btn btn-primary">Register</button>
    </form>
  )
}
RegistrationForm.contextTypes = {
  store: PropTypes.object,
};

export default withRouter(RegistrationForm);
