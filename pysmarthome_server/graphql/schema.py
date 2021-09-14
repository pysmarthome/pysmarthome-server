from ariadne import gql, make_executable_schema
from .query_resolvers import query
from .mutation_resolvers import mutation
from .type_resolvers import device, state

type_names = {
    'base_state': 'BaseState',
    'device_state': 'DeviceState',
    'device': 'Device',
    'plugin': 'Plugin',
    'device_info': 'DevicesInfo',
}

state_fields = '''
    id: ID!
    power: String!
'''

device_fields = '''
    id: ID!
    name: String!
    addr: String
    power_by_ping: Boolean
'''

device_interface_fields = f'''
    {device_fields}
    state: {type_names['base_state']}!
'''

type_defs = f'''
    interface {type_names['base_state']} {{
        {state_fields}
    }}

    interface {type_names['device']} {{
        {device_interface_fields}
    }}

    type {type_names['device_state']} implements {type_names['base_state']} {{
        {state_fields}
    }}

    type {type_names['plugin']} {{
        id: ID!
        version: String
        description: String
        module_name: String!
        devices: [{type_names['device']}]
    }}

    type {type_names['device_info']} {{
        type: String!
        ids: [ID]!
        fields: [String]
    }}

    type Query {{
        plugins: [{type_names['plugin']}!]!
        plugin(id: ID!): {type_names['plugin']}!
        devices(type: String, power: String): [{type_names['device']}]!
        device(id: ID!): {type_names['device']}!
        devices_info: [{type_names['device_info']}]
    }}

    type Mutation {{
        install_plugins(names: [String!]!): [{type_names['plugin']}]!
        uninstall_plugins(ids: [ID!]!): [{type_names['plugin']}]!
        toggle(id: ID!): {type_names['base_state']}!
        poweroff(id: ID!): {type_names['base_state']}!
        poweron(id: ID!): {type_names['base_state']}!
        device_action(id: ID!, action: String!, args: [String]): {type_names['base_state']}!
    }}
'''


def get_types(cls):
    name = cls.graphql_name
    result = ''
    names = list(type_names.values())
    if name in names: return ''
    type_names[cls.collection] = name
    for child_cls in cls.children_model_classes.values():
        result += get_types(child_cls['class'])
    parent_names = [parent.__name__ for parent in cls.__mro__]
    interface = ''
    if 'DeviceStatesModel' in parent_names:
        interface = 'BaseState'
    elif 'DevicesModel' in parent_names:
        interface = 'Device'
    return result + cls.to_graphql_type(interface)


def mkschema(models_classes):
    global type_defs
    for cls in models_classes:
        type_defs += get_types(cls)
    return make_executable_schema(gql(type_defs), [query, mutation, state, device])
