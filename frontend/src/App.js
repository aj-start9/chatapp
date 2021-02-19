import React from 'react';
import './App.css';
import { Route, Switch } from 'react-router-dom'
import Auth from './containers/auth/auth'
import Chat from './containers/chat/chat'
import { LinkedInPopUp } from 'react-linkedin-login-oauth2';



class App extends React.Component {
  render() {
    return (
      <div className="App">
        <Switch>
          <Route path="/chat" component={Chat} />
          <Route path="/" component={Auth} />
        </Switch>
      </div>
    );
  }
}


export default App;
