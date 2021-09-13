def trigger_action(ctrl, action, *args):
    ctrl.trigger_action(action, *args)
    state = ctrl.state
    return {
        **state.to_dict(),
        'typename': state.graphql_name,
    }


def dev_ctrl_to_dict(ctrl):
    children_models = ctrl.model.children_models
    children_dicts = {}
    for k, models in children_models.items():
        if len(models) == 1:
            children_dicts[k] = models[0].to_dict()
        else:
            children_dicts[k] = []
            for model in models:
                children_dicts[k].append(model.to_dict())
    return {
        **ctrl.to_dict(),
        **children_dicts,
        'typename': ctrl.model_class.graphql_name,
    }


def plugin_to_dict(plugin):
    ctrls = plugin.controllers.values()
    return {
        **plugin.to_dict(),
        'devices': [dev_ctrl_to_dict(ctrl) for ctrl in ctrls],
    }
