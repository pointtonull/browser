#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import ClientForm
import cookielib
import urllib2
import urllib
import webbrowser
from tempfile import mkdtemp
import os
import time

#SOME GLOBALS
TEMPDIR = mkdtemp()
HOME = os.environ["HOME"]

#Will include some default presets
DEFAULT = {
    }
FIREFOX = {
    }
CHROMIUM = {
    }

#And a presets maker wizzard to use your browser settings
class Real_browser(object):
    def __init__(self, browser="default"):
        pass


class Form(object):
    def __init__(self, parent, form):
        self.parent = parent
        self._form = form
        self.names = [control.name for control in self._form.controls]

    def click_request_data(self):
        return self._form.click_request_data()

    def __getitem__(self, y):
        return self._form.__getitem__(y)

    def __setitem__(self, i, y):
        return self._form.__setitem__(i, y)

    def __repr__(self):
        return str(self.names)

    def __str__(self):
        return self._form.__str__()

    def click(self):
        return self._form.click()

    def submit(self, *args, **kw):
        return self.parent.put_form(self, *args, **kw)

    def set_all_readonly(self, *args, **kw):
        return self._form.set_all_readonly(*args, **kw)


class Cookies_mngr(cookielib.CookieJar):
    def __init__(self, *args, **kwargs):
        """
            initialize the CookieJar class that implements:
                .add_cookie_header
                .clear
                .clear_expired_cookies
                .clear_session_cookies
                .domain_re
                .dots_re
                .extract_cookies
                .magic_re
                .make_cookies
                .non_word_re
                .quote_re
                .set_cookie
                .set_cookie_if_ok
                .set_policy
                .strict_domain_re
        """

        cookielib.CookieJar.__init__(self)

    def save_cookies(self, filename):
        """
            save the cookies to a file
        """

    def load_cookies(self, filename):
        """
            load cookies from a file
        """


class Cache_mngr(urllib2.BaseHandler):
    def __init__(self, backend=None):
        """
            initialize the backend connection
        """

    def get_html(self, url):
        """
            returns the html and the time it was fetched
        """


class Browser(object):
    def __init__(self, preset=DEFAULT, cookiesmngr=None, cachemngr=None,
            proxiesmngr=None):
        """
            instante a cookie manager if not given
            instance a cache manager if not given
            instance a proxies manager if not given
            instance a urllib2 opener for private use
        """

        #FIXME: Must depend on presets
        self.cache = cachemngr or Cache_mngr()
        self.cookies = cookiesmngr or Cookies_mngr()
        self.proxies = proxiesmngr or urllib2.ProxyHandler()
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookies),
            self.proxies,
            self.cache,
            )
        
        

    def config(self):
        """
            getter and setter to the self._config dict
        """

    def reload(self):
        """
            reload the current url and update states

            return result
        """

    def show(self, url=None, openon=None):
        """
            open a copy of the html in a webbrowser
        """

        if url:
            self.go(url)
        temppath = "%s/%d.html" % (TEMPDIR, time.time())
        tempfile = open(temppath, "w")
        tempfile.write(self.get_html())
        tempfile.close()

        if not openon:
            return webbrowser.open(temppath)
        else:
            return webbrowser.GenericBrowser(openon).open(temppath)

    def go(self, url, data=None, timeout=None):
        """
            request the html and update the statuses
        """
        self._last_req = self.opener.open(url, data, timeout)
        return self._update_status()

    def _update_status(self, request=None):
        request = request or self._last_req
        self._code = request.code
        self._url = request.url
        self._msg = request.msg
        self._headers = request.headers
        self._html = request.read()
        return self._msg

    def get_html(self, url=None, data=None, timeout=None):
        """
            returns the html
        """
        if url:
            self.go(url, data, timeout)
        return self._html

    def get_title(self, url=None, data=None, timeout=None):
        """
            returns the title
        """
        if url:
            self.go(url, data, timeout)
        return self._title

    def get_code(self, url=None, data=None, timeout=None):
        """
            returns the error code
        """
        if url:
            self.go(url, data, timeout)
        return self._code

    def get_url(self):
        """
            returns the current url
        """
        return self._url

    def get_forms(self, url=None, data=None, timeout=None):
        """
            return the forms
        """


def main():
    pass

if __name__ == "__main__":
    exit(main())
