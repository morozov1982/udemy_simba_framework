from views import Index, About, Blog, Shop

# Путь: Контроллер()
routes = {
    '/': Index(),
    '/about/': About(),
    '/blog/': Blog(),
    '/shop/': Shop(),
}
