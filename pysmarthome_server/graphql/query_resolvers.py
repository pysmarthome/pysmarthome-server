from ariadne import QueryType
from .utils import plugin_to_dict, dev_ctrl_to_dict
from pysmarthome.models import CommandsModel, ColorsModel, ColorCommandsModel

query = QueryType()


@query.field('plugin')
def resolve_plugin(_, info, id):
    g = info.context['g']
    return plugin_to_dict(g.plugin_manager.plugins[id])


@query.field('plugins')
def resolve_plugins(_, info):
    g = info.context['g']
    return [plugin_to_dict(p) for p in g.plugin_manager.plugins.values()]


@query.field('search_plugins')
def resolve_search_plugins(_, info, query=''):
    return info.context['g'].plugin_manager.search(query)


@query.field('device')
def resolve_device(_, info, id):
    g = info.context['g']
    ctrls = g.plugin_manager.get_controllers()
    return dev_ctrl_to_dict(ctrls[id])


@query.field('devices')
def resolve_devices(_, info, type='', power=''):
    g = info.context['g']
    ctrls = g.plugin_manager.get_controllers().values()
    if type:
        ctrls = [ctrl for ctrl in ctrls if ctrl.model.graphql_name == type]
    if power:
        ctrls = [ctrl for ctrl in ctrls if ctrl.get_power() == power]
    return [dev_ctrl_to_dict(ctrl) for ctrl in ctrls]


@query.field('devices_info')
def resolve_devices_info(_, info):
    g = info.context['g']
    ctrls = g.plugin_manager.get_controllers().values()
    infos = {}
    for ctrl in ctrls:
        name = ctrl.model.graphql_name
        if name not in infos:
            fields = ctrl.model.schema_attrs.keys()
            infos[name] = {'ids': [], 'fields': fields}
        infos[name]['ids'].append(ctrl.id)
    return [{ 'type': k, 'ids': v['ids'], 'fields': v['fields'] }
        for k, v in infos.items()]


@query.field('commands')
def resolve_colors(_, info):
    db = info.context['db']
    commands = CommandsModel.load_all(db)
    return [c.to_dict() for c in commands]


@query.field('colors')
def resolve_colors(_, info):
    db = info.context['db']
    colors = ColorsModel.load_all(db)
    return [c.to_dict() for c in colors]


@query.field('color_commands')
def resolve_color_commands(_, info):
    db = info.context['db']
    color_commands = ColorCommandsModel.load_all(db)
    return [c.to_dict() for c in color_commands]
