from views import Index, About, Blog, Contacts

# Путь: Контроллер()
routes = {
    '/': Index(),
    '/about/': About(),
    '/blog/': Blog(),
    '/contacts/': Contacts(),
}
