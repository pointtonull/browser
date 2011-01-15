#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import ClientForm
import cookielib
import urllib2
import urllib

class FORM(object):

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


class COOKIE(cookielib.CookieJar):
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

    def save_cookies(self, filename):
        """
            save the cookies to a file
        """

    def load_cookies(self, filename):
        """
            load cookies from a file
        """


class CACHE:
    def __init__(self, backend=None):
        """
            initialize the backend connection
        """

    def get_html(self, url):
        """
            returns the html and the time it was fetched
        """


class BROWSER(object):
    def __init__(self, preset):
        """
            instante a cookie manager
            instance a urllib2 opener for private use
            instance a cache manager
        """

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
        debug(temppath)

        if not openon:
            return webbrowser.open(temppath)
        else:
            return webbrowser.GenericBrowser(openon).open(temppath)

    def go(self, url):
        """
            request the html and update the statuses
        """

    def get_html(self, url=None, *args, **kw):
        """
            returns the html
        """
        if url:
            self.go(url)
        return self._html

    def get_title(self, url=None, *args, **kwargs):
        """
            returns the title
        """
        if url:
            self.go(url)
        return self._title

    def get_code(self, url=None):
        """
            returns the error code
        """
        if url:
            self.go(url)
        return self._code

    def get_url(self):
        """
            returns the current url
        """
        return self._url

    def get_forms(self, url=None, *args, **kw):
        """
            return the forms
        """


def main():
    pass

if __name__ == "__main__":
    exit(main())
