from views import Index, About, Blog, Contacts, StudyPrograms, CoursesList, \
    CreateCourse, CreateCategory, CategoryList

# Путь: Контроллер()
routes = {
    '/': Index(),
    '/about/': About(),
    '/blog/': Blog(),
    '/contacts/': Contacts(),
    '/study-programs/': StudyPrograms(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
}
