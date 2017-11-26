import React from 'react';
import PropTypes from 'prop-types';

import { FieldGroup } from '../components/Form';


class ConfirmForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: '',
      verificationCode: '',
    };
  }

  static propTypes = {
    onSubmit: PropTypes.func,
    onCancel: PropTypes.func,
    onResend: PropTypes.func,
    error: PropTypes.string,
  }

  onSubmit = (event) => {
    event.preventDefault();
    console.log("State!", this.state.verificationCode, this.state.email);
    console.log("Context!", this.context);

    this.props.onSubmit(this.state.verificationCode)
     .then((user) => {
       console.log(user);
     })
     .catch((error) => {
       console.log(error);
       this.setState({ error });
     });
  }

  onResend = (event) => {
    event.preventDefault();
    this.props.onResend()
     .then((user) => {
       this.setState({ error: 'Code resent' });
     })
     .catch((error) => {
       this.setState({ error });
     });

  }

  changeVerificationCode = (event) => {
    this.setState({ verificationCode: event.target.value });
  }

  changeEmail = (event) => {
    this.setState({ email: event.target.value });
  }

  render = () => (
    <form onSubmit={this.onSubmit}>
      <div>{this.state.error.toString()}</div>

      <FieldGroup
        type="text"
        id="code"
        placeholder="code"
        label="Verification Code"
        onChange={this.changeVerificationCode} required />

      <button className="btn btn-primary" type="submit">Submit</button>
      <button className="btn btn-default" type="button" onClick={this.onResend}>Resend code</button>
    </form>
  )
}

ConfirmForm.propTypes = {

};

export default ConfirmForm;