import urllib.request

from bottle import request, get, run, debug

@get('<path:path>')
def proxy(path):
    qs = request.query_string
    path_with_qs = path + '?' + qs if qs else path
    print(path_with_qs)

    with urllib.request.urlopen('https://habrahabr.ru'+path_with_qs) as response:
       content = response.read()

    return content

if __name__ == "__main__":
    debug(True)
    run(host='0.0.0.0', port=8232, reloader=True)
