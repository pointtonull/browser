#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from BeautifulSoup import BeautifulSoup
from litebrowser import Browser
from os import makedirs, path
from zipfile import ZipFile

import re
import sys

DIRNAME = path.join("tmp", "encuestas")

def main():
    browser = Browser()
    urls = sys.argv[1:]
    try:
        makedirs(DIRNAME)
    except:
        pass
    for url in urls:
        form_class = url.split("/")[-2]
        html = browser.get_html(url)
        soup = BeautifulSoup(html)
        forms = [(f["href"], f.text)
            for f in soup("a", {"id":re.compile(u"xf-399⊙\\d+-1")})]
        for form, timestamp in forms:
            form_instance = form.split("/")[-1]
            print form_instance
            html = browser.get_html(form)

            filename = "%s_%s_%s.zip.txtconin" % (form_class, form_instance,
                timestamp)
            filename = path.join(DIRNAME, filename)
            with ZipFile(filename, 'w', 8) as file:
                file.writestr("encuesta.xml", html)

        print(len(forms))


if __name__ == "__main__":
    exit(main())
