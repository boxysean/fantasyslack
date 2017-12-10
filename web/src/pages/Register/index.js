import { Panel } from 'react-bootstrap';
import React from 'react';
import RegistrationForm from './RegistrationForm';
import { withRouter } from 'react-router';

const Register = () => (
  <Panel>
    <h2>Register</h2>
    <div className="row">
      <div className="col-md-4">
        <RegistrationForm />
      </div>
    </div>
  </Panel>
);

export default withRouter(Register);
