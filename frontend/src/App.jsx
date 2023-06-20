import logo from './logo.svg';
import './css/App.css';

import { BrowserRouter, Route, Switch } from 'react-router-dom';
import AffirmativeButton from './components/buttons/affirmativeButton';
import DenyButton from './components/buttons/denyButton';

import CheckEnvVariables from './config';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                    Standalone Bank Management web-application written in <code className="codeBlock">Python</code>/<code className="codeBlock">Django</code><br/>
                    with the web-frontend written in <code className="codeBlock">ReactJS</code> and the mobile frontend written in <code className="codeBlock">ReactNative</code>.
                </p>
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn React
                </a>
                <div className="buttons-container">
                    <AffirmativeButton text="Click me!" onClick={() => console.log("Agree!")} />
                    <DenyButton text="Don't click me!" onClick={() => console.log("Disagree!")} />
                </div>
            </header>
            <CheckEnvVariables />
        </div>
    );
}

export default App;
