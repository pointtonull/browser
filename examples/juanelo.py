#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import litebrowser
import re
from subprocess import call

def download(url):
    #TODO: Must be done by browser instance
    return call(["wget", "--no-verbose", url])

def main():
    browser = litebrowser.Browser()
    next_url = 'http://www.juanelo.cl/1999/09/el-origen-de-juanelo-i/'

    while next_url:
        browser.go(next_url)
        html = browser.get_html()

        entry = re.search(r'''(?xs)<div\ class="entry">(.*?)
            <div\ class="postmetadata">''', html).group(1)
        for image in re.finditer(r'src="(.*?)"', entry):
            image_url = image.group(1)
            print(image_url)
            download(image_url)

        match = re.search(r"""a href="(.*?)" title="next post:""", html)
        if match:
            next_url = match.group(1)
            print(next_url)
        else:
            next_url = None

if __name__ == "__main__":
    exit(main())

