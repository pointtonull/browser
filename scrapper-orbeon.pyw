#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from BeautifulSoup import BeautifulSoup
from litebrowser import Browser
from os import makedirs, path
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
        forms = set(re.findall(r'href="(/orbeon/fr/.*?/.*?/edit/.*?)"', html))
        for form in forms:
            form_instance = form.split("/")[-1]
            html = browser.get_html(form)
            soup = BeautifulSoup(html)

            output = []
            for div in soup("div", {"class":"fr-grid-content"}):
                for label in div("label", {"class":"xforms-label"}):
                    label = label.text
                    if label and not label.startswith(u"«"):
                        output.append(label)
                if div.find("span", {"class":"xforms-upload-filename"}):
                    span = div.find("span", {"class":"xforms-upload-filename"})
                    output.append(span.text)
                elif div.find("span", {"class":"xforms-items"}):
                    selecteds = [span.text
                        for span in div("span")
                            if "-selected" in span["class"]]
                    output.append(" - ".join(selecteds))
                elif div.find("option"):
                    for option in div("option", {"selected":"selected"}):
                        output.append(option.text)
                elif div.input:
                    try:
                        value = div.input["value"]
                        output.append(value)
                    except:
                        output.append(div.prettify())
                elif div.textarea:
                    textarea = div.textarea
                    output.append(textarea.text)
                elif div.span:
                    for span in div("span", {"class":"xforms-output-output"}):
                        output.append(span.text)

            filename = "%s %s.txt" % (form_class, form_instance)
            filename = path.join(DIRNAME, filename)
            with open(filename, "w") as file:
                file.write("\r\n".join((line.encode("utf8")
                    for line in output
                        if line)))
        print(len(forms))


if __name__ == "__main__":
    exit(main())
