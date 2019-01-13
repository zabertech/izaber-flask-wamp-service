#!/usr/bin/python

"""Server Completion

Usage:
  run_server.py [options]

Options:
  -h --help          Show this screen.
  --version          Show version.
  --host <host>      IP to bind to (overrides yaml)
  --port <port>      Port to bind to (overrides yaml)
  -c <config_file>   Configuration file
  -e <environment>   Select Environment

"""

from server import *

if __name__ == '__main__':
    args = docopt.docopt(__doc__, version='2.0')
    config_args = None
    if args['-c']:
        config_args = {'config_filename':args['-c']}
    app_initialize(
        environment=args['-e'],
        config=config_args
    )

    # If the demo mode is on, let's show the user login information
    if config.demo:
        print("As this is in demo mode in osso.yaml, we're printing the user/pass")
        for username,user_data in config.osso.users.dict().items():
            print("{u}: '{d[password]}'".format(u=username,d=user_data))

    blueprint.run(
        host=args['--host'] or config.flask.host,
        port=int(args['--port'] or config.flask.port),
        debug=config.debug
    )

