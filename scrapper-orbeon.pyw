#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from litebrowser import Browser
import re

def main():
    browser = Browser()
    url = "http://localhost:8080/orbeon/fr/orbeon/w9/summary"
    browser.go(url)
    html = browser.get_html()
    forms = set(re.findall(r'href="(/orbeon/fr/.*?/.*?/edit/.*?)"', html))
    for form in forms:
        url = form.replace("edit", "pdf")
        instance = url.split("/")[-1]
        with open(instance + ".pdf", "w") as file:
            file.write(browser.get_html(url))
        print url


if __name__ == "__main__":
    exit(main())
