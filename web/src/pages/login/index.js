import { CognitoState, EmailVerification, Login, NewPasswordRequired } from 'react-cognito';
import { Link, Redirect } from 'react-router-dom';

import EmailVerificationForm from './EmailVerificationForm';
import LoginForm from './LoginForm';
import NewPasswordRequiredForm from './NewPasswordRequiredForm';
import { Panel } from 'react-bootstrap';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

// eslint-disable-next-line
const loggedInPageDebug = (user, attributes) => (
  <div>
    <p>Attributes</p>
    <table>
      <thead>
        <tr>
          <td>Name</td>
          <td>Value</td>
        </tr>
      </thead>
      <tbody>
        {Object.keys(attributes).map(name =>
          <tr key={name}>
            <td>{name}</td>
            <td>{attributes[name]}</td>
          </tr>,
        )}
      </tbody>
    </table>
  </div>
);

const loggedInPage = (user, attributes) => (
  <Redirect to="/" />
);

const loggedOutPage = () => (
  <Panel className="login-form">
    <p>Not logged in</p>
    <Login>
      <LoginForm />
    </Login>
  </Panel>
);

const newPasswordPage = () => (
  <div>
    <p>New password required, since this is your first login</p>
    <NewPasswordRequired>
      <NewPasswordRequiredForm />
    </NewPasswordRequired>
  </div>
);

const emailVerificationPage = () => (
  <div>
    <p>You must verify your email address.  Please check your email for a code</p>
    <EmailVerification>
      <EmailVerificationForm />
    </EmailVerification>
  </div>
);

const confirmFormDebug = () => (
  <div>
    <p>A confirmation code has been sent to your email address</p>
    <Link to="/">Home</Link>
  </div>
);

const mfaPage = () => (
  <div>
    <p>You need to enter an MFA, but this library does not yet support them.</p>
  </div>
);

const BaseDashboard = ({ state, user, attributes }) => {
  console.log("Base Dashboard State: " + state);
  switch (state) {
    case CognitoState.LOGGED_IN:
      return loggedInPage(user, attributes);
    case CognitoState.AUTHENTICATED:
    case CognitoState.LOGGING_IN:
      return (
        <div>
          <img src="ajax-loader.gif" alt="" />
        </div>
        )
    case CognitoState.LOGGED_OUT:
    case CognitoState.LOGIN_FAILURE:
      return loggedOutPage();
    case CognitoState.MFA_REQUIRED:
      return mfaPage();
    case CognitoState.NEW_PASSWORD_REQUIRED:
      return newPasswordPage();
    case CognitoState.EMAIL_VERIFICATION_REQUIRED:
      return emailVerificationPage();
    case CognitoState.CONFIRMATION_REQUIRED:
      return confirmFormDebug();
    default:
      return (
        <div>
          <p>Unrecognised cognito state</p>
        </div>
      );
  }
};
BaseDashboard.propTypes = {
  user: PropTypes.object,
  attributes: PropTypes.object,
  state: PropTypes.string,
};

const mapStateToProps = state => ({
  state: state.cognito.state,
  user: state.cognito.user,
  attributes: state.cognito.attributes,
});

const Dashboard = connect(mapStateToProps, null)(BaseDashboard);

export default Dashboard;
