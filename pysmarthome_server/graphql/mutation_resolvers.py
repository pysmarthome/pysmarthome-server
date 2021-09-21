from ariadne import MutationType
from .utils import trigger_action, plugin_to_dict, dev_ctrl_to_dict
import json

mutation = MutationType()


@mutation.field('install_plugins')
def install_plugins(_, info, names=[]):
    g = info.context['g']
    pm = g.plugin_manager
    pm.install(*names)
    return [plugin_to_dict(p) for p in pm.sync_plugins_with_db()]


@mutation.field('uninstall_plugins')
def uninstall_plugins(_, info, ids=[]):
    pm = info.context['g'].plugin_manager
    pm.uninstall(*ids)
    return [plugin_to_dict(p) for p in pm.sync_plugins_with_db()]


@mutation.field('toggle')
def toggle(_, info, id):
    g = info.context['g']
    ctrl = g.plugin_manager.get_controllers()[id]
    return trigger_action(ctrl, 'toggle')


@mutation.field('poweron')
def poweron(_, info, id):
    g = info.context['g']
    ctrl = g.plugin_manager.get_controllers()[id]
    return trigger_action(ctrl, 'on')


@mutation.field('poweroff')
def poweroff(_, info, id):
    g = info.context['g']
    ctrl = g.plugin_manager.get_controllers()[id]
    return trigger_action(ctrl, 'off')


@mutation.field('device_action')
def device_action(_, info, id, action, args=[]):
    g = info.context['g']
    ctrl = g.plugin_manager.get_controllers()[id]
    return trigger_action(ctrl, action, *args)


@mutation.field('device_update')
def device_update(_, info, id, fields='', state=''):
    pm = info.context['g'].plugin_manager
    ctrl = pm.get_controllers()[id]
    if fields:
        ctrl.update(**json.loads(fields))
    if state:
        ctrl.state.update(**json.loads(state))
    return dev_ctrl_to_dict(ctrl)
