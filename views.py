"""Модуль с контроллерами вэб-приложения"""
from simba_framework.templator import render


class Index:
    def __call__(self):
        return '200 OK', render('index.html')


class About:
    def __call__(self):
        return '200 OK', 'about'


class Blog:
    def __call__(self):
        return '200 OK', 'Blog without html ;-)'


class Shop:
    def __call__(self):
        return '200 OK', 'Shop without html ;-)'
