import React from "react";
import "./css/config.css";
import FuckedLight from "./components/notifications/fuckedLight";
import OkayLight from "./components/notifications/okayLight";
import CurrentDateTime from "./utils/dateString";
import NoticeBody from "./components/notifications/notice";


// This is the URL of the backend server.
const BASE_URL = process.env.REACT_APP_BASE_URL;

// URLs regarding the user-app.
const REGISTER_TELLER_EP = process.env.REACT_APP_REGISTER_TELLER_EP;
const PASSWORD_LOGIN_EP = process.env.REACT_APP_PASSWORD_LOGIN_EP;
const TEST_AUTHENTICATION_EP = process.env.REACT_APP_TEST_AUTHENTICATION_EP;
const GET_OWN_DETAILS_EP = process.env.REACT_APP_GET_OWN_DETAILS_EP;


function registerNotice(msg, check) {
    if (Boolean(check) === true) {

        return  <div className="notice">
                    <OkayLight /> <NoticeBody msg={msg} />
                </div>;
    }
    else if (Boolean(check) === false) {

        return  <div className="notice">
                    <FuckedLight /> <NoticeBody msg={msg} />
                </div>;
    }
};

export default function CheckEnvVariables() {

    const envVars = {
        baseUrl: BASE_URL,
        registerTellerEp: REGISTER_TELLER_EP,
        passwordLoginEp: PASSWORD_LOGIN_EP,
        testAuthenticationEp: TEST_AUTHENTICATION_EP,
        getOwnDetailsEp: GET_OWN_DETAILS_EP
    }

    let msg = "All environment variables set.";
    let check = true;

    let keys = Object.keys(envVars);
    for (const item of keys) {
        if (
            (envVars[item] === undefined)
            || (envVars[item] === "")
            || (envVars[item] === null)
        ) {
            msg = `The \`${item}\` environment variable is not set.`;
            check = false;
            break;
        }
        else {
            continue;
        }
    }
    console.log(`[${CurrentDateTime()}]\t${msg}`);
    return registerNotice(msg, check);
}
