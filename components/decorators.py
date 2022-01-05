"""Декоратор для реализации маршрутизации"""


class AppRoute:
    def __init__(self, routes, url):
        """
        Сохраняем значение переданного параметра
        :param routes:
        :param url:
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        Декоратор
        :param cls:
        :return:
        """
        self.routes[self.url] = cls()
