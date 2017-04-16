FROM python:3.5.3-alpine

RUN pip install pudb bottle

COPY /src /src

CMD ["python3", "/src/proxy.py"]
