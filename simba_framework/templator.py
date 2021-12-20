from os.path import join
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры, передаваемые в шаблон
    :return:
    """
    file_path = join(folder, template_name)

    with open(file_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())

    # Рендерим шаблон с параметрами
    return template.render(**kwargs)
