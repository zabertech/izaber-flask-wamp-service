const PREFIX = 'com.izaber.wamp.osso.';

const USERNAME = '';
const API_KEY = '';

var websocketURL = location.protocol == 'https:' ? 'wss' : 'ws';
    websocketURL += '://'+location.host+'/ws';

function onchallenge(session, method, extra) {
// --------------------------------------------------
    console.log("Challenge received:",method);
    if ( method === "ticket" ) {
      return API_KEY;
    }
    else {
      throw "don't know how to authenticate using '" + method + "'";
    }
}

function initWAMP () {
// --------------------------------------------------
    console.log("Location protocol is:", location.protocol);
    console.log("Connecting to ",websocketURL);
    connection = new autobahn.Connection({
                            url: websocketURL, // secure websocket server location
                            realm: 'izaber', // realm is kinda like namespace, zaber
                                             // doesn't have another namespace (we
                                             // tried for sandboxing but ended up with
                                             //  bigger issues)
                            authmethods: ["ticket","cookie"], // there are multiple methods of authentication
                                                     // (ie. SSL certs which we don't use), we're just
                                                     // using username and (passwords or API keys)
                            authid: USERNAME,
                            onchallenge: onchallenge
                        });

    connection.onclose = function (reason, details) {
        console.log("disconnected", reason, details.reason, details);
        let div = document.getElementById('onclose');
        div.innerHTML = details.reason;
    };

    connection.onopen = function (session) {
        session.subscribe(
            'com.izaber.wamp.osso.time',
            handlerTimeEvent
        );
    };
}

function handlerTimeEvent(args, kwargs, details) {
// --------------------------------------------------
    var d = new Date(kwargs['iso_str']);
    var t = document.getElementById('dashboard-time');
    t.innerHTML = d.toLocaleTimeString()
}

function initMainIndex() {
// --------------------------------------------------
    initWAMP();
    connection.open();
}

