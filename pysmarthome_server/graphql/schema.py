from ariadne import gql, make_executable_schema
from .query_resolvers import query
from .mutation_resolvers import mutation
from .type_resolvers import device, state

type_names = {
    'base_state': 'BaseState',
    'device_state': 'DeviceState',
    'rgb_lamp_state': 'RgbLampState',
    'tv_state': 'TvState',
    'ac_state': 'AcState',
    'device': 'Device',
    'pingable_device': 'PingableDevice',
    'multi_command_device': 'MultiCommandDevice',
    'multi_command_rgb_lamp': 'MultiCommandRgbLamp',
    'rgb_lamp': 'RgbLamp',
    'snapshot_base_state': 'SnapshotBaseState',
    'snapshot_state': 'SnapshotState',
    'snapshot_tv_state': 'SnapshotTvState',
    'snapshot_ac_state': 'SnapshotAcState',
    'snapshot_rgb_lamp_state': 'SnapshotRgbLampState',
    'tv': 'Tv',
    'ac': 'Ac',
    'color': 'Color',
    'command': 'Command',
    'color_command': 'ColorCommand',
    'plugin_info': 'PluginInfo',
    'plugin': 'Plugin',
    'device_info': 'DevicesInfo',
    'scene': 'Scene',
}

state_fields = '''
    id: ID!
    power: String!
'''

snapshot_state_fields = '''
    id: ID!
    power: String
'''

device_fields = '''
    id: ID!
    name: String!
'''

pingable_device_fields = '''
    addr: String
    power_by_ping: Boolean
'''

device_interface_fields = f'''
    {device_fields}
    snapshot_states: [{type_names['snapshot_base_state']}]!
    state: {type_names['base_state']}!
'''

rgb_lamp_interface_fields = f'''
    {device_fields}
    state: {type_names['rgb_lamp_state']}!
'''

multi_command_device_fields = f'''
    commands: [{type_names['command']}]
'''

multi_command_rgb_lamp_fields = f'''
    brightness_min: Int
    brightness_max: Int
    color_commands: [{type_names['color_command']}]
'''

type_defs = f'''
    interface {type_names['base_state']} {{
        {state_fields}
    }}

    interface {type_names['snapshot_base_state']} {{
        {snapshot_state_fields}
    }}

    interface {type_names['device']} {{
        {device_interface_fields}
    }}

    interface {type_names['multi_command_device']} {{
        {device_interface_fields}
        {multi_command_device_fields}
    }}

    interface {type_names['multi_command_rgb_lamp']} {{
        {rgb_lamp_interface_fields}
        {multi_command_device_fields}
        {multi_command_rgb_lamp_fields}
    }}

    interface {type_names['rgb_lamp']} {{
        {rgb_lamp_interface_fields}
    }}

    interface {type_names['tv']} {{
        {device_fields}
        {pingable_device_fields}
        state: {type_names['tv_state']}!
        volume_min: Int
        volume_max: Int
    }}

    interface {type_names['ac']} {{
        {device_fields}
        state: {type_names['ac_state']}!
        temp_min: Int
        temp_max: Int
    }}

    type {type_names['device_state']} implements {type_names['base_state']} {{
        {state_fields}
    }}

    type {type_names['snapshot_state']} implements {type_names['snapshot_base_state']} {{
        {snapshot_state_fields}
    }}

    type {type_names['rgb_lamp_state']} implements {type_names['base_state']} {{
        {state_fields}
        color: String!
        brightness: Float
    }}

    type {type_names['snapshot_rgb_lamp_state']} implements {type_names['snapshot_base_state']} {{
        {snapshot_state_fields}
        color: String
        brightness: Float
    }}

    type {type_names['ac_state']} implements {type_names['base_state']} {{
        {state_fields}
        temp: Int
    }}

    type {type_names['snapshot_ac_state']} implements {type_names['snapshot_base_state']} {{
        {snapshot_state_fields}
        temp: Int
    }}

    type {type_names['tv_state']} implements {type_names['base_state']} {{
        {state_fields}
        volume: Int
        mute: Boolean
    }}

    type {type_names['snapshot_tv_state']} implements {type_names['snapshot_base_state']} {{
        {snapshot_state_fields}
        volume: Int
        mute: Boolean
    }}

    type {type_names['color']} {{
        id: ID!
        name: String!
        label: String!
        rgb: [Int]
        hex: String
    }}

    type {type_names['command']} {{
        id: ID!
        name: String
        label: String
        data: String!
    }}

    type {type_names['color_command']} {{
        id: ID!
        color: {type_names['color']}
        command: {type_names['command']}
    }}

    type {type_names['plugin_info']} {{
        version: String
        description: String
        module_name: String!
    }}

    type {type_names['plugin']} {{
        id: ID!
        version: String
        description: String
        active: Boolean!
        module_name: String!
        devices: [{type_names['device']}]
    }}

    type {type_names['device_info']} {{
        type: String!
        ids: [ID]!
        fields: [String]
    }}

    type {type_names['scene']} {{
        id: ID!
        name: String!
        snapshot_state_ids: [ID]!
        devices: [{type_names['device']}]!
    }}

    type Query {{
        plugins: [{type_names['plugin']}!]!
        plugin(id: ID!): {type_names['plugin']}!
        search_plugins(query: String): [{type_names['plugin_info']}]
        devices(type: String, power: String): [{type_names['device']}]!
        device(id: ID!): {type_names['device']}!
        devices_info: [{type_names['device_info']}]
        commands: [{type_names['command']}]!
        colors: [{type_names['color']}]!
        color_commands: [{type_names['color_command']}]!
    }}

    type Mutation {{
        install_plugins(names: [String!]!): [{type_names['plugin']}]!
        uninstall_plugins(ids: [ID!]!): [{type_names['plugin']}]!
        toggle_active_plugins(ids: [ID!]!): [{type_names['plugin']}]!
        toggle(id: ID!): {type_names['base_state']}!
        poweroff(id: ID!): {type_names['base_state']}!
        poweron(id: ID!): {type_names['base_state']}!
        device_action(id: ID!, action: String!, args: [String]): {type_names['base_state']}!
        device_update(id: ID!, fields: String, state: String): {type_names['device']}!
        restore_device_state(id: ID!, state_id: ID!): {type_names['base_state']}!
        activate_scene(id: ID!): [{type_names['device']}]
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
    if 'DevicesModel' in parent_names:
        interface = type_names['device']
    if 'AcsModel' in parent_names:
        interface += ' & ' + type_names['ac']
    elif 'TvsModel' in parent_names:
        interface += ' & ' + type_names['tv']
    elif 'RgbLampsModel' in parent_names:
        interface += ' & ' + type_names['rgb_lamp']
    if 'MultiCommandDevicesModel' in parent_names:
        interface += ' & ' + type_names['multi_command_device']
    if 'DeviceStatesModel' in parent_names:
        interface = type_names['device_state']
    elif 'RgbState' in parent_names:
        interface += ' & ' + type_names['rgb_lamp_state']
    elif 'TvStateModel' in parent_names:
        interface += ' & ' + type_names['tv_state']
    elif 'AcStateModel' in parent_names:
        interface += ' & ' + type_names['ac_state']
    return result + cls.to_graphql_type(interface)


def mkschema(models_classes):
    global type_defs
    for cls in models_classes:
        type_defs += get_types(cls)
    return make_executable_schema(gql(type_defs), [query, mutation, state, device])
