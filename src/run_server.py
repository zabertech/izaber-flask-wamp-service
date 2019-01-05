#!/usr/bin/python

"""Server Completion

Usage:
  run_server.py [options]
  run_server.py test <payrun_id> [options]

Options:
  -h --help          Show this screen.
  --version          Show version.
  -e <environment>   Select Environment

"""

from server import *

if __name__ == '__main__':
    args = docopt.docopt(__doc__, version='2.0')
    app_initialize()
    blueprint.run(host='0.0.0.0',port=5000,debug=True)

