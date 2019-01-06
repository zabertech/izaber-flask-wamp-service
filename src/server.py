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
# wamp_connections is a hash of
#
# wamp_connections = {
#     username: connection instance
# }
#

class OSSOAuthenticator(SimpleTicketAuthenticator):
    def __init__(self):
        # We're going to try and authenticate off of Zerp
        super(OSSOAuthenticator,self).__init__({})

    def request_ticket_authenticate(self,realm,username,password,cookie_value):
        """ This is called when a user attempts to authenticate themselves
            via the ticket mechanism (AKA. username/password).
        """

        try:
            wamp_connections[username] = True
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


def get_auth_data():
    """ Returns the information related to the current session's
        logins status. 
    """
    # If we can find a session, then let's use it
    cookie_value = request.cookies.get(app.cookie_name)
    if not cookie_value:
        return

    # Get a list of all the payroll runs
    authid = session.get('role',{}).get('authid',None)
    if not authid:
        return

    return session

def is_logged_in():
    """ Returns a truthy value
    """
    return get_auth_data()

def authenticated_only(f):
    def f_authenticated_only(*args,**kwargs):
        if not is_logged_in():
            return redirect(
                        url_for('server.login',
                        _scheme=config.flask.scheme,
                        _external=True
                      ))
        return f(*args,**kwargs)
    return f_authenticated_only

###########################################################################
# Webserver API
###########################################################################

blueprint = IZaberFlask(__name__)

@blueprint.route('/',endpoint='index',methods=['POST','GET'])
@authenticated_only
def route_index():
    tags = {}
    return render_template('index.html',**tags)

@blueprint.route('/login',endpoint='login',methods=['POST','GET'])
def login_page():
    tags = {}

    # Ensure we have a cookie set if one hasn't been created yet
    cookie_value = request.cookies.get(app.cookie_name)
    set_cookie_value = None
    if not cookie_value:
        cookie_value = secure_rand()
        set_cookie_value = cookie_value

    # Check if the user is trying to login
    login = request.form.get('login')
    response = None
    if login:
        password = request.form.get('password')
        auth = authenticator.request_ticket_authenticate('izaber',login,password,cookie_value)
        if auth:
            session['role'] = auth
            response = redirect(url_for('server.index',_scheme=config.flask.scheme,_external=True))
            tokens[cookie_value] = auth

    # If we didn't login successfully, response is None
    if response is None:
        response = render_template('login.html',**tags)

    # And create the response that will be sent to the user
    resp = make_response(response)
    if set_cookie_value:
        resp.set_cookie(app.cookie_name,set_cookie_value)

    return resp


@wamp.register('echo')
def echo(data):
    return data+" RESPONSE!"

@wamp.subscribe('hellos')
def hellos(data):
    print("Received subscribed message:", data.dump())

###########################################################################
# Activity thread
###########################################################################

def time_publisher():
    """ Publishes a simple date stamp to the uri
        'com.izaber.wamp.osso.time' every second
    """
    while True:
        now = datetime.datetime.now()
        time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        wamp.publish(
            'com.izaber.wamp.osso.time',
            kwargs={
              'time_str': time_str,
              'iso_str': now.isoformat(),
              'H': now.hour,
              'M': now.minute,
              'S': now.second,
              'Y': now.year,
              'm': now.month,
              'd': now.second
            }
        )
        time.sleep(1)

###########################################################################
# App Core
###########################################################################

def app_initialize(config=None,environment=None,):
    global authenticator
    global cookie_authenticator

    # We don't want the system to automatically connect
    # to ZERP as we use the connected user's credentials
    izaber.wamp.AUTORUN = False

    initialize(
        'osso',
        config=config or {},
        environment=environment
    )

		# We use a custom authenticator so we can pull
    # usernames/passwords out of the osso.yaml file
    authenticator = OSSOAuthenticator()
    cookie_authenticator = CookieAuthenticator()
    app.authenticators.append(authenticator)
    app.authenticators.append(cookie_authenticator)

    # We don't restrict routes for logged in users
    authorizer = WAMPAuthorizeUsersEverything('*')
    app.authorizers.append(authorizer)

    # Start the publisher threads
    time_thread = threading.Thread(
                            target=time_publisher,
                        )
    time_thread.daemon = True
    time_thread.start()

@wamp.wamp_connect()
def wamp_connect(client):
    session_id = client.session_id

@wamp.wamp_disconnect()
def wamp_disconnect(client):
    session_id = client.session_id

