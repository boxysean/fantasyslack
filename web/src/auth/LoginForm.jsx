import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

import { FieldGroup } from '../components/Form';

class LoginForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      email: props.email || '',
      password: '',
    };
  }

  onSubmit = (event) => {
    event.preventDefault();
    this.props.onSubmit(this.state.email, this.state.password);
  }

  changeEmail = (event) => {
    this.setState({ email: event.target.value });
  }

  changePassword = (event) => {
    this.setState({ password: event.target.value });
  }

  componentWillUnmount = () => {
    this.props.clearCache();
  }

  render() {
    return (
      <form onSubmit={this.onSubmit}>
        <div>{this.props.error}</div>

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

        <button type="submit" className="btn btn-primary">Sign in</button>
        <Link to="/reset"><button className="btn btn-default">Password reset</button></Link>
      </form>
    );
  }
}

LoginForm.propTypes = {
  onSubmit: PropTypes.func,
  clearCache: PropTypes.func,
  username: PropTypes.string,
  error: PropTypes.string,
  email: PropTypes.string,
};

export default LoginForm;