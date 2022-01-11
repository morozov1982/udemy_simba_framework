from jinja2 import Environment, FileSystemLoader


def render(template_name, folder='templates', static_url='/static/', **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param static_url: петь к статике
    :param kwargs: параметры, передаваемые в шаблон
    :return:
    """

    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    template = env.get_template(template_name)

    # Рендерим шаблон с параметрами
    return template.render(**kwargs)
