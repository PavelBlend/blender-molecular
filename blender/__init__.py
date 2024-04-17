bl_info = {
    'name': 'Molecular',
    'author':
        'Jean-Francois Gallant (PyroEvil), '
        'Pavel_Blend, '
        'Martin Felke (scorpion81), ',
        'Omid Ghotbi'
    'version': (1, 2, 0),
    'blender': (2, 80, 0),
    'location': 'Properties > Particle Properties',
    'description':
        'Addon for calculating collisions '
        'and for creating links between particles',
    'wiki_url': 'https://github.com/PavelBlend/blender-molecular',
    'tracker_url': 'https://github.com/PavelBlend/blender-molecular/issues',
    'category': 'Physics'
}


from . import props
from . import ops
from . import ui
from . import handlers


modules = (props, ops, ui, handlers)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
