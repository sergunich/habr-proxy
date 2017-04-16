from bottle import request, get, run, debug

@get('<path:path>')
def proxy(path):
    qs = request.query_string
    content = path + '?' + qs if qs else path
    print(content)
    return content

if __name__ == "__main__":
    debug(True)
    run(host='0.0.0.0', port=8232, reloader=True)
