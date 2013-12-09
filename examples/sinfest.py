#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from litebrowser import Browser
import re

def main():
    browser = Browser()
    next_url = "http://sinfest.net/archive_page.php?comicID=4323"
    while next_url:
        html = browser.get_html(next_url)
        img_url = re.search(r'''http://sinfest.net/comikaze/comics/[\d-]*.gif''', html).group(0)
        next_url = re.search(r'''"(http://sinfest.net/archive_page.php\?comicID=\d*)"><img src="images/next_a.gif"''', html)
        if next_url:
            next_url = next_url.group(1)
        filename = img_url.split("/")[-1]
        print filename
        with open(filename, "w") as file:
            file.write(browser.get_html(img_url))
        print "img:", img_url
        print "next:", next_url

if __name__ == "__main__":
    exit(main())
