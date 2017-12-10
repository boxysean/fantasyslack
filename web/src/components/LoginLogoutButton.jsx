import React from 'react';
import PropTypes from 'prop-types';
import { CognitoState, Logout } from 'react-cognito';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

// eslint-disable-next-line
const LogoutButton = ({ onClick }) => <a href="#" onClick={onClick}>Log out</a>;
LogoutButton.propTypes = {
  onClick: PropTypes.func,
};


const BaseLoginLogoutButton = ({ isLoggedIn }) => {
  if (isLoggedIn) {
    return (
      <li className="nav-item">
        <Logout>
          <LogoutButton />
        </Logout>
      </li>
    );
  } else {
    return (
      <li className="nav-item">
        <Link to="/login">Login</Link>
      </li>
    );
  }
};
const mapStateToProps = state => ({
  isLoggedIn: state.cognito.state === CognitoState.LOGGED_IN
});
const LoginLogoutButton = connect(mapStateToProps, null)(BaseLoginLogoutButton);

export default LoginLogoutButton;
