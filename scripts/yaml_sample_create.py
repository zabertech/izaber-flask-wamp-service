#!/usr/bin/python

import jinja2
import os
import sys
import base64
import docopt
import six

if not sys.argv or len(sys.argv) < 2:
    six.print_("Need a output file name")
    sys.exit()

template = open('osso.yaml.sample','r').read()

parsed = jinja2.Template(template).render(
          rand_hex=lambda length: base64.b64encode(
                        os.urandom(length)
                    )[:-2].decode('utf-8')
      )


out_fname = sys.argv[1]
open(out_fname,'w').write(parsed)


