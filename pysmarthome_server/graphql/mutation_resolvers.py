from ariadne import MutationType
from .utils import trigger_action, plugin_to_dict, dev_ctrl_to_dict
from pysmarthome import ScenesModel
import json
import asyncio

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


@mutation.field('toggle_active_plugins')
def toggle_active_plugins(_, info, ids=[]):
    pm = info.context['g'].plugin_manager
    pm.toggle_active(*ids)
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


@mutation.field('restore_device_state')
def restore_device_state(_, info, id, state_id):
    pm = info.context['g'].plugin_manager
    ctrl = pm.get_controllers()[id]
    ctrl.restore_snapshot_state(state_id)
    state = ctrl.state
    return {
        **state.to_dict(),
        'typename': state.graphql_name,
    }


@mutation.field('activate_scene')
def activate_scene(_, info, id):
    db = info.context['db']
    ctrls = info.context['g'].plugin_manager.get_controllers()
    sceneModel = ScenesModel.load(db, id)
    tasks = []
    selected_ctrls = []
    for i, id in enumerate(sceneModel.device_ids):
        if id not in ctrls: continue
        ctrl = ctrls[id]
        selected_ctrls.append(ctrl)
        func = ctrl.restore_snapshot_state
        snapshot_id = sceneModel.snapshot_state_ids[i]
        tasks.append(asyncio.to_thread(func, snapshot_id))
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
    return [dev_ctrl_to_dict(ctrl) for ctrl in selected_ctrls]
