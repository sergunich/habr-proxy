# habr-proxy

Поскольку "отображаться и работать полностью корректно" несколько расплывчатая формулировка, пока что я сделал необходимый минимум, чтобы протестировать идею для стартапа "добавлять к словам значок«™»". Поэтому сейчас не реализованы сессии и post запросы, но могу добавить во второй итерации. Главная мотивация: не делать лишнего и быстро получить фидбек от заказчика на основе прототипа.

Как запустить: 
1) ./run.sh (или python3 ./src/proxy.py, но нужно установить зависимости pip install bottle beautifulsoup4)
2) Открыть в браузере http://localhost:8232/company/yandex/blog/258673/
