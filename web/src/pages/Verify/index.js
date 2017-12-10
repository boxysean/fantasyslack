import { Confirm } from 'react-cognito';
import { Panel } from 'react-bootstrap';
import React from 'react';
import VerificationForm from './VerificationForm';
import { withRouter } from 'react-router';

const Verify = () => (
  <Panel>
    <p>A confirmation code has been sent to your email address</p>
    <div className="row">
      <div className="col-md-4">
        <Confirm>
          <VerificationForm />
        </Confirm>
      </div>
    </div>
  </Panel>
);

export default withRouter(Verify);
