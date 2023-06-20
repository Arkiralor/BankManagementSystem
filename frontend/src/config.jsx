import React from "react";
import "./css/config.css";
import FuckedLight from "./components/notifications/okayLight";
import OkayLight from "./components/notifications/okayLight";

// I need to set the global variables and constants here.

// This is the URL of the backend server.
const BASE_URL = process.env.REACT_APP_BASE_URL;

// URLs regarding the user-app.
const REGISTER_TELLER_EP = process.env.REACT_APP_REGISTER_TELLER_EP;
const PASSWORD_LOGIN_EP = process.env.REACT_APP_PASSWORD_LOGIN_EP;
const TEST_AUTHENTICATION_EP = process.env.REACT_APP_TEST_AUTHENTICATION_EP;
const GET_OWN_DETAILS_EP = process.env.REACT_APP_GET_OWN_DETAILS_EP;


function registerNotice(msg, check) {
    if (Boolean(check) == true) {
        let comp = (
            <div className="noticeContainer">
                <div className="notice">
                    <OkayLight /> <h3>{msg}</h3>
                </div>
            </div>
        )

        return comp;
    }
    else if (Boolean(check) == false) {
        let comp = (
            <div className="noticeContainer">
                <div className="notice">
                    <FuckedLight /> <h3>{msg}</h3>
                </div>
            </div>
        )

        return comp;
    }
};

export default function CheckEnvVariables() {

    let envVars = {
        baseUrl: BASE_URL,
        registerTellerEp: REGISTER_TELLER_EP,
        passwordLoginEp: PASSWORD_LOGIN_EP,
        testAuthenticationEp: TEST_AUTHENTICATION_EP,
        getOwnDetailsEp: GET_OWN_DETAILS_EP,
    }

    let msg = "All environment variables set.";
    let check = true;

    let keys = Object.keys(envVars);
    for (const item of keys) {
        if (
            (envVars[item] == undefined)
            || (envVars[item] == "")
            || (envVars[item] == null)
        ) {
            console.log(`[${new Date().toLocaleString()}] ${item}: ${envVars[item]}`);
            msg = `The \`${item}\` environment variable is not set.`;
            check = false;
            console.log(`[${new Date().toLocaleString()}] Check: ${check}`);
            break;
        }
    }
    console.log(`[${new Date().toLocaleString()}] Check: ${check}`);
    return registerNotice(msg, check);
}
