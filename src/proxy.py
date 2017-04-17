import re
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from bottle import request, response, get, run, debug
from bs4.element import Comment
from bs4 import BeautifulSoup

TM_CHAR = '™'


@get('<path:path>')
def proxy(path):
    qs = request.query_string
    path_with_qs = path + '?' + qs if qs else path

    content, is_html = '', False
    try:
        resp = urlopen('https://habrahabr.ru'+path_with_qs)
    except HTTPError as e:
        response.status = e.code
        content = e.read()
        is_html = e.headers['Content-Type'].startswith('text/html')
    except URLError as e:
        content = ('We failed to reach a server. '
                   'Reason: {0}'.format(e.reason))
    else:
        content = resp.read()
        is_html = resp.headers['Content-Type'].startswith('text/html')

    if is_html:
        soup = BeautifulSoup(content, 'html5lib')

        for a in soup.find_all('a', href=re.compile('https://habrahabr.ru')):
            a['href'] = (a['href'] or '').replace('https://habrahabr.ru', '')

        trademarketize(soup.find('body'))

        content = str(soup)

    return content


def trademarketize(tag):
    for string in tag.find_all(string=True):
        if isinstance(string, (Comment,)) or (string.parent.name == 'script'):
            continue

        text = str(string)
        text = re.sub(r'(?<!\w)'  # must not be letter (lookbehind)
                      r'(?P<target>\w{6})'  # must be 6 letter long
                      r'(?!\w)'  # must not be letter (lookahead)
                      r'', r'\g<target>'+TM_CHAR, text)
        string.replace_with(text)


if __name__ == "__main__":
    debug(True)
    run(host='0.0.0.0', port=8232, reloader=True)
