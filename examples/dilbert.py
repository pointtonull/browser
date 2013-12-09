
#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import re

from litebrowser import Browser
from os import listdir, makedirs, path

BASE_URL = "http://dilbert.com/strips/comic/"
DIRNAME = "dilbert"

def main():
    browser = Browser()
    try:
        makedirs(DIRNAME)
    except OSError:
        pass
    files = sorted(listdir(DIRNAME))
    if files:
        lastfile = files[-1]
    else:
        lastfile = "1989-04-16.gif"
    lastday = lastfile.split(".")[0]
    next_url = BASE_URL + lastday + "/"
    while next_url:
        html = browser.get_html(next_url)
        img_url = re.search(r'''http://dilbert.com/dyn/str_strip.*?\.gif''', html).group(0)
        filename = path.join(DIRNAME, next_url.split("/")[-2] + ".gif")
        print filename
        print "img:", img_url
        with open(filename, "w") as file:
            file.write(browser.get_html(img_url))
        next_url = re.search(r'''href="(/strips/comic/.*?/") class="STR_Next PNG_Fix"''', html)
        if next_url:
            next_url = next_url.group(1)
        else:
            print html

if __name__ == "__main__":
    exit(main())
