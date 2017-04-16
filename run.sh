docker build --tag=sergunich-habr-proxy .
docker run -it --rm -p 8232:8232 -v $(pwd)/src:/src sergunich-habr-proxy
