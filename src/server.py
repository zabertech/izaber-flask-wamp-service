#!/usr/bin/python

import sys
sys.path.append('libs')

from osso import *


###########################################################################
# Webserver API
###########################################################################

##################################################
# Authenication
##################################################

tokens = {}
authenticator = None
cookie_authenticator = None

wamp_connections = {}
# Seems like wamp_connections is a hash of
#
# wamp_connections = {
#     username: zerp_wamp connection instance
# }
#

class IDEAuthenticator(SimpleTicketAuthenticator):
    def __init__(self):
        # We're going to try and authenticate off of Zerp
        super(IDEAuthenticator,self).__init__({})

    def request_ticket_authenticate(self,realm,username,password,cookie_value):
        # Check by connecting to Nexus
        try:
            user_wamp = izaber.wamp.WAMP(
                        url = config.wamp.connection.url,
                        username = username,
                        password = password,
                        uri_base = 'com.izaber.wamp',
                        realm = 'izaber',
                    ).run()
            # if we have a wamp connection, we can then
            # build it into a Zerp connection
            user_zerp = izaber.wamp.zerp.ZERP(
                            wamp=user_wamp,
                            database=config.wamp.zerp.database,
                        )

            wamp_connections[username] = user_zerp
        except Exception as ex:
            # Nope, not logged in
            return None

        # If we got here, we have a confirmation that there's been
        # a successsful connection. This means we can start setting
        # some stuff up!
        auth = DictObject(
                    authid=username,
                    authprovider='dynamic',
                    authmethod='ticket',
                    role='frontend',
                    realm=realm,
                )

        # If we get a result, let's let the cookie handler know
        if auth:
            cookie_authenticator.session_save(cookie_value,auth)

        return auth


###########################################################################
# Webserver API
###########################################################################

blueprint = IZaberFlask(__name__)

@blueprint.route('/')
def route_index():
    tags = {}
    return render_template('index.html',**tags)

@wamp.register('echo')
def echo(data):
    return data+" RESPONSE!"

@wamp.subscribe('hellos')
def hellos(data):
    print("Received subscribed message:", data.dump())

def app_initialize():
    global authenticator
    global cookie_authenticator

    # We don't want the system to automatically connect
    # to ZERP as we use the connected user's credentials
    izaber.wamp.AUTORUN = False

    #initialize('izaber-wamp',environment='live')
    #initialize('izaber-wamp',environment='debug')
    initialize('izaber-wamp')

    authenticator = IDEAuthenticator()
    cookie_authenticator = CookieAuthenticator()
    app.authenticators.append(authenticator)
    app.authenticators.append(cookie_authenticator)

    authorizer = WAMPAuthorizeUsersEverything('*')
    app.authorizers.append(authorizer)


if __name__ == '__main__':
    initialize('example',environment='debug')
    print("Running")
    app.run()