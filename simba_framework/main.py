import quopri
from os import path

from framework_requests import GetRequests, PostRequests
from components.content_types import CONTENT_TYPES_MAP


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    """Класс Framework - основа WSGI-фреймворка"""

    def __init__(self, settings, routes_obj):
        self.routes_lst = routes_obj
        self.settings = settings

    def __call__(self, environ, start_response):
        # Адрес, по которому пользователь выполнил переход
        path = environ['PATH_INFO'].lower()  # не уверен, что это хорошо ;-)

        # Добавляем закрывающий слеш
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
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')
        elif path.startswith(self.settings.STATIC_URL):
            # /static/img/logo.jpg/ -> img/logo.jpg
            file_path = path[len(self.settings.STATIC_URL):len(path)-1]
            content_type = self.get_content_type(file_path)
            code, body = self.get_static(self.settings.STATIC_FILES_DIR,
                                         file_path)
        else:
            view = PageNotFound404()
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')

        # Запуск контроллера
        start_response(code, [('Content-Type', content_type)])
        return [body]

    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = path.basename(file_path).lower()
        extention = path.splitext(file_name)[1]
        return content_types_map.get(extention, "text/html")

    @staticmethod
    def get_static(static_dir, file_path):
        path_to_file = path.join(static_dir, file_path)
        with open(path_to_file, 'rb') as f:
            file_content = f.read()
        status_code = '200 OK'
        return status_code, file_content

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'utf-8')
            val_decode_str = quopri.decodestring(val).decode('utf-8')
            new_data[k] = val_decode_str
        return new_data
