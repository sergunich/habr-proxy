FROM python:3.5.3-alpine

RUN pip install pudb bottle beautifulsoup4 pep8

COPY /src /src

RUN pep8  --show-source --show-pep8 /src/proxy.py

CMD ["python3", "/src/proxy.py"]
