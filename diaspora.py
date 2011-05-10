#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from ConfigParser import SafeConfigParser
from optparse import OptionParser
import litebrowser
import logging
import os
import sys

APP_NAME = "diaspora"
LOG_FILE = os.path.expanduser("~/.%s.log" % APP_NAME)
CONFIG_FILES = [os.path.expanduser("~/.%s" % APP_NAME),
    os.path.expanduser("~/%s.ini" % APP_NAME)]
VERBOSE = 20


def get_depth():
    """
    Returns the current recursion level. Nice to look and debug
    """
    def exist_frame(number):
        """
        True if frame number exists
        """
        try:
            if sys._getframe(number):
                return True
        except ValueError:
            return False

    maxn = 1
    minn = 0

    while exist_frame(maxn):
        minn = maxn
        maxn *= 2

    middle = (minn + maxn) / 2

    while minn < middle:
        if exist_frame(middle):
            minn = middle
        else:
            maxn = middle

        middle = (minn + maxn) / 2

    return max(minn - 4, 0)


def ident(func, identation="  "):
    """
    Decorates func to add identation prior arg[0]
    """
    def decorated(message, *args, **kwargs):
        newmessage = "%s%s" % (identation * (get_depth() - 1), message)
        return func(newmessage, *args, **kwargs)
    return decorated


class Diaspora(object):
    def __init__(self, baseurl, account, password):
        self.browser = litebrowser.Browser()

        self.baseurl = baseurl
        self.account = account
        self.password = password

        self.login()

    def login(self, account=None, password=None):
        loginurl = "%s/users/sign_in" % self.baseurl
        DEBUG("Diaspora:login::loginurl: %s" % loginurl)
        DEBUG("Diaspora:login:: %s" % self.browser.go(loginurl))
        forms = self.browser.get_forms()
        DEBUG("Diaspora:login::forms: %s" % forms)
        form = forms[0]
        form["user[username]"] = self.account
        form["user[password]"] = self.password
        return form.submit()

    def post(self, message, public=False):
        homeurl = "%s/aspects" % self.baseurl
        if homeurl not in self.browser.get_url():
            self.browser.go = homeurl
        forms = self.browser.get_forms()
        form = forms[2]
        form.set_all_readonly(False)

        if public:
            form["status_message[public]"] = "true"

        form["status_message[text]"] = message
        return form.submit()


def get_options():
    """
    Parse the arguments
    """
    # Instance the parser and define the usage message
    optparser = OptionParser(usage="""
    %prog [-clvq]""", version="%prog .1")

    # Define the options and the actions of each one
    optparser.add_option("-c", "--config", help=("Uses the given conf file "
        "inteast of the default"), action="store", dest="conffile")
    optparser.add_option("-l", "--log", help=("Uses the given log file "
        "inteast of the default"), action="store", dest="logfile")
    optparser.add_option("-v", "--verbose", action="count", dest="verbose",
        help="Increment verbosity")
    optparser.add_option("-q", "--quiet", action="count", dest="quiet",
        help="Decrement verbosity")

    # Define the default options
    optparser.set_defaults(verbose=0, quiet=0, logfile=LOG_FILE,
        conffile="")

    # Process the options
    options, args = optparser.parse_args()
    return options, args


def get_config(conf_file=None):
    """
    Read config files
    """
    config = SafeConfigParser()
    read_from = conf_file or CONFIG_FILES
    files = config.read(read_from)
    DEBUG("get_config::readed %s" % files)

    return config


def main(options, args):
    """The main routine"""
    # Read the config values from the config files
    config = get_config(options.conffile)
    config = dict(config.items("CONFIG"))
    diaspora = Diaspora(
        config["baseurl"],
        config["account"],
        config["password"]
    )

    message = sys.stdin.read()
    diaspora.post(message, public=True)


if __name__ == "__main__":
    # == Reading the options of the execution ==
    options, args = get_options()

    VERBOSE = (options.quiet - options.verbose) * 10 + 30
    format_str = "%(message)s"
    logging.basicConfig(format=format_str, level=VERBOSE)
    logger = logging.getLogger()

    DEBUG = ident(logger.debug) # For developers
    MOREINFO = ident(logger.info) # Plus info
    INFO = ident(logger.warning) # Default
    WARNING = ident(logger.error) # Non critical errors
    ERROR = ident(logger.critical) # Critical (will break)

    DEBUG("get_options::options: %s" % options)
    DEBUG("get_options::args: %s" % args)

    DEBUG("Verbose level: %s" % VERBOSE)
    exit(main(options, args))
