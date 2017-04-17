from urllib.request import urlopen
import re

from bottle import request, get, run, debug
from bs4 import BeautifulSoup

TM_CHAR = '™'


@get('<path:path>')
def proxy(path):
    qs = request.query_string
    path_with_qs = path + '?' + qs if qs else path

    content, is_html = '', False
    with urlopen('https://habrahabr.ru'+path_with_qs) as response:
        content = response.read()
        is_html = response.headers['Content-Type'].startswith('text/html')

    if is_html:
        soup = BeautifulSoup(content, 'html.parser')

        for a in soup.find_all('a', href=re.compile('https://habrahabr.ru')):
            a['href'] = (a['href'] or '').replace('https://habrahabr.ru', '')

        article = (soup.select('div.content') or [None])[0]
        comments = (soup.select('ul#comments-list') or [None])[0]
        for tag in filter(bool, (article, comments,)):
            trademarketize(tag)

        content = str(soup)

    return content


def trademarketize(tag):
    for string in tag.find_all(string=True):
        text = str(string)
        text = re.sub(r'(?<!\w)'  # must not be letter (lookbehind)
                      r'(?P<target>\w{6})'  # must be 6 letter long
                      r'(?!\w)'  # must not be letter (lookahead)
                      r'', r'\g<target>'+TM_CHAR, text)
        string.replace_with(text)


if __name__ == "__main__":
    debug(True)
    run(host='0.0.0.0', port=8232, reloader=True)
