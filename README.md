# iZaber Flask WAMP Services

This provides an example Flask based web service that uses standard HTTP or WAMP locally to exchanges information.

## Architecture

Flask is the background framework. Within Flask, WAMP support via websockets is provided.

On the front end, autobahn.js is through a webpack bundled javascript package.

## Building:

### Prerequisites:

> This still needs to be sorted out.

* needs nodejs and npm
* apt-get install python3
* pip3 install flask izaber-flask-wamp

### Prepping environment

After cloning the repository, execute the script:

`./scripts/env-setup.sh`

What this will do is:
* ensure repo is up to date
* install the required npm modules
* generate required bundle files
* copy the bundle files into the appropriate place for the flask app

### Starting up the server

After running `env-setup.sh`, execute the script:

`./run-server.sh`

This should create a basic site on 0.0.0.0:5000 that can reached at http://SYSTEMIP:5000







