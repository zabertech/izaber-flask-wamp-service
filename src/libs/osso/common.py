import docopt
import struct
import fcntl

from pprint import pprint
import datetime
import time

import traceback
import dateutil.parser
import six
import logging
import sys
import re
import pytz
import json
import threading

import os
import select
import termios
import tty
import pty
import subprocess
import base64
import signal
import random

from flask import Flask, render_template, \
                    jsonify, session, request, \
                    redirect, url_for, make_response

import izaber
import izaber.wamp
import izaber.wamp.zerp
import izaber.flask
import izaber.flask.wamp

from izaber import initialize, config
from izaber.date import Date
from izaber.templates import parse
from izaber.log import log
from izaber.paths import paths
from izaber.flask.wamp import IZaberFlask, \
                                IZaberFlaskPermissive, \
                                wamp, \
                                app, \
                                SimpleTicketAuthenticator, \
                                CookieAuthenticator, \
                                WAMPAuthorizeUsersEverything

from .utils import *

##################################################
# MISC Helpers
##################################################

rng = random.SystemRandom()
def secure_rand():
    rand_value = rng.randint(0,sys.maxsize)
    return hex(rand_value)[1:]

###########################################
# Data mangling and syntax sugar classes
###########################################

class DictObject(dict):
    def __init__(self, noerror=False, *args, **kwargs):
        super(DictObject, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self.noerror_ = noerror

    def __getattr__(self,k):
        if self.noerror_:
            return self.__dict__.get(k)
        return super(DictObject).__getattr__(k)

    def __nonzero__(self):
        # Evaluate the object to "True" only if there is data contained within
        return bool(self.__dict__.keys())

class DictInterface(object):
    """ Merely provides a way to manipulate attributes via
        obj[key] access rather than obj.key. Particularly
        useful for dynamic attributes
    """

    def __getitem__(self,k):
        return getattr(self,k)

    def __setitem__(self,k,v):
        return setattr(self,k,v)

class Listable(object):
    def __init__(self,data=None):
        if data is None:
            data = []
        self.data = data

    def filter(self,filter_function):
        item = filter(filter_function,self.data)
        return type(self)(item)

    def append(self,item):
        self.data.append(item)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for item in self.data:
            yield item

