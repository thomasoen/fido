from bs4 import BeautifulSoup
import htmlentitydefs
import re


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def extractData(souplist):
    if souplist is None:
        return ""
    return map(lambda s: s.getText(), souplist)


def replaceRecursive(x):
    x = x.replace("  ", " ")
    x = x.replace("\n", "")
    if "  " in x:
        return replaceRecursive(x)
    else:
        return x
