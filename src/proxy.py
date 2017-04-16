from pprint import pprint
import urllib.request
import re

from bottle import request, get, run, debug
from bs4 import BeautifulSoup

@get('<path:path>')
def proxy(path):
    qs = request.query_string
    path_with_qs = path + '?' + qs if qs else path

    with urllib.request.urlopen('https://habrahabr.ru'+path_with_qs) as response:
        content = response.read()
        is_html = response.headers['Content-Type'].startswith('text/html')

    if is_html:
        soup = BeautifulSoup(content, 'html.parser')
        for a in soup.find_all('a', href=re.compile('https://habrahabr.ru')):
            a['href'] = (a['href'] or '').replace('https://habrahabr.ru', '')

        article = (soup.select('div.content') or [None])[0] #safely try get tag
        if article:
            for string in article.find_all(string=True):
                text = str(string)
                text = re.sub(r'(?<!\w)(?P<target>\w{6})(?!\w)', '\g<target>™', text)
                string.replace_with(text)

        content = str(soup)

    return content

if __name__ == "__main__":
    debug(True)
    run(host='0.0.0.0', port=8232, reloader=True)
