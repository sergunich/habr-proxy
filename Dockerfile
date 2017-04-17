FROM python:3.5.3-alpine

RUN pip install pudb bottle beautifulsoup4 pylint
RUN pip install pycodestyle

COPY /src /src

RUN touch /.pylintrc
RUN pylint --rcfile=/.pylintrc --disable=C /src/proxy.py || true
RUN pycodestyle --show-source --show-pep8 /src/proxy.py || true

CMD ["python3", "/src/proxy.py"]
