import { FieldGroup } from '../../components/BootstrapExt';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import React from 'react';

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

  onPasswordResetSubmt = (event) => {
    event.preventDefault();
    this.props.setPassword(this.state.email, this.state.code, this.state.password)
      .then(() => this.setState({
        message: 'Password reset',
        error: '',
      }))
      .catch((err) => this.setState({
        message: '',
        error: err.message,
      }));
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
      </form>
    );
  }
}

LoginForm.propTypes = {
  onSubmit: PropTypes.func,
  clearCache: PropTypes.func,
  error: PropTypes.string,
  email: PropTypes.string,
};

export default LoginForm;
