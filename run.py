from wsgiref.simple_server import make_server
from simba_framework.main import Framework
from views import routes

# Создаём объект WSGI-приложения
app = Framework(routes)

with make_server('', 8080, app) as httpd:
    print('Запуск на порту 8080...')
    print('http://127.0.0.1:8080')
    httpd.serve_forever()
