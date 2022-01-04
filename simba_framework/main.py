import quopri
from framework_requests import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    """Класс Framework -  основа WSGI-фреймворка"""

    def __init__(self, routes_obj):
        self.routes_lst = routes_obj

    def __call__(self, environ, start_response):
        # Адрес, по которому пользователь выполнил переход
        path = environ['PATH_INFO'].lower()  # не уверен, что это хорошо ;-)

        # Добавляем закрывающий /
        if not path.endswith('/'):
            path = f'{path}/'

        # Получаем все данные запроса
        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
            print(f'Пришёл POST-запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Пришли GET-параметры: {request_params}')

        # Контроллер в зависимости от пути
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        # Запуск контроллера
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'utf-8')
            val_decode_str = quopri.decodestring(val).decode('utf-8')
            new_data[k] = val_decode_str
        return new_data
