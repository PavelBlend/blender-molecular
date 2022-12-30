bl_info = {
    'name': 'Molecular',
    'author':
        'Jean-Francois Gallant (PyroEvil), '
        'Pavel_Blend, '
        'Martin Felke (scorpion81)',
    'version': (1, 1, 2),
    'blender': (2, 80, 0),
    'location': 'Properties > Particle Properties',
    'description': 
        'Addon for calculating collisions '
        'and for creating links between particles',
    'wiki_url': 'https://github.com/PavelBlend/blender-molecular',
    'tracker_url': 'https://github.com/PavelBlend/blender-molecular/issues',
    'category': 'Physics'
}


def get_modules():
    from . import props
    from . import ops
    from . import ui
    from . import handlers

    modules = (props, ops, ui, handlers)

    return modules


def register():
    modules = get_modules()
    for module in modules:
        module.register()


def unregister():
    modules = get_modules()
    for module in reversed(modules):
        module.unregister()
