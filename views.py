"""Модуль с контроллерами вэб-приложения"""
from datetime import date

from simba_framework.templator import render
from components.models import Engine, MapperRegistry
from components.decorators import AppRoute
from components.cbv import ListView, CreateView
from components.unit_of_work import UnitOfWork

site = Engine()
routes = {}

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppRoute(routes=routes, url='/')
class Index(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()
    # def __call__(self, request):
    #     return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(routes=routes, url='/blog/')
class Blog:
    def __call__(self, request):
        return '200 OK', 'Blog without html ;-)'


@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html')


@AppRoute(routes=routes, url='/study-programs/')
class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 Page not Found'


# TODO: Переписать с использованием ListView
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    def __call__(self, request):
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('course-list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course-list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CategoriesCreateView(CreateView):
    template_name = 'create-category.html'

    def create_obj(self, data: dict):
        name = data.get('name')
        name = site.decode_value(name)

        new_category = site.create_category()
        site.categories.append(new_category)

        schema = {'name': name}
        new_category.mark_new(schema)
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/category-list/')
class CategoryListView(ListView):
    template_name = 'category-list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student-list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create-student.html'

    def create_obj(self, data: dict):
        name = data.get('name')
        name = site.decode_value(name)

        new_obj = site.create_user('student')
        site.students.append(new_obj)

        schema = {'name': name}
        new_obj.mark_new(schema)
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add-student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)
