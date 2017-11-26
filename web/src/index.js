import './index.css';
import 'bootstrap/dist/css/bootstrap.css';

import { cognito, setupCognito } from 'react-cognito';
import { combineReducers, createStore } from 'redux';

import App from './App';
import { Provider } from 'react-redux';
import React from 'react';
import ReactDOM from 'react-dom';

const reducers = combineReducers({
  cognito,
});

let store = createStore(reducers, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__());

let cognitoConfig = {
  "region": "us-east-1",
  "userPool": "us-east-1_APXGoWFHh",
  "clientId": "6o37c8db0u7l74o1nhukqaqdup",
  "identityPool": "us-east-1:822a71cf-4bdb-43ab-8f9d-cbfec9c30997",
};

setupCognito(store, cognitoConfig);

ReactDOM.render((
  <Provider store={store}>
    <App />
  </Provider>
), document.getElementById('root'))
