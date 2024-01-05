import multiprocessing

import bpy

from . import desc
from . import defs


def define_customizable_props_values(
        mol,
        name,
        compress=True,
        relink=False,
        minimum=0.0,
        maximum=1.0,
        text=None
    ):

    # value property

    base = 'link'

    if not compress:
        # expansion property
        name = 'e' + name

    if relink:
        base = 're' + base

    value_prop_name = '{}_{}'.format(base, name)
    default, minimum, maximum = defs.values[value_prop_name]

    if minimum == 0.0 and maximum == 1.0:
        subtype = 'FACTOR'
    else:
        subtype = 'NONE'

    value_prop = bpy.props.FloatProperty(
        name=name.capitalize(),
        description='',
        min=minimum,
        max=maximum,
        default=default,
        precision=6,
        subtype=subtype
    )

    setattr(mol, value_prop_name, value_prop)

    # random property

    value_random_prop_name = '{}_{}rand'.format(base, name)
    default, minimum, maximum = defs.values[value_random_prop_name]

    value_random_prop = bpy.props.FloatProperty(
        name='Random {}'.format(name.capitalize()),
        description='',
        min=minimum,
        max=maximum,
        default=default,
        precision=6,
        subtype='FACTOR'
    )

    setattr(mol, value_random_prop_name, value_random_prop)


def define_customizable_props(
        mol,
        name,
        use_same_values=True,
        relink=False,
        minimum=0.0,
        maximum=1.0,
        text=None
    ):

    if text:
        label = text
    else:
        label = name.capitalize()

    prefix = ''
    if relink:
        prefix = 're'

    define_customizable_props_values(
        mol,
        name,
        relink=relink,
        minimum=0.0,
        maximum=1.0,
        text=label
    )

    if use_same_values:
        same_value_prop = bpy.props.BoolProperty(
            name="Same values for compression/expansion",
            description=desc.LINK_SAME_VALUE,
            default=True
        )

        same_value_name = '{}link_{}_samevalue'.format(prefix, name)
        setattr(mol, same_value_name, same_value_prop)

        define_customizable_props_values(
            mol,
            name,
            compress=False,
            relink=relink,
            minimum=0.0,
            maximum=1.0,
            text=label
        )


def define_density_props(mol):
    mol.density_active = bpy.props.BoolProperty(
        name="Calculate Particles Weight by Density",
        description=desc.DENSITY_ACTIVE,
        default=False
    )
    matter_items = [
        ("-1", "Custom", desc.MATTER_CUSTOM),
        ("1555", "Sand", desc.MATTER_SAND),
        ("1000", "Water", desc.MATTER_WATER),
        ("7800", "Iron", desc.MATTER_IRON)
    ]
    mol.matter = bpy.props.EnumProperty(
        name='Preset',
        items=matter_items,
        description=desc.MATTER
    )
    mol.density = bpy.props.FloatProperty(
        name="Kg Per Cube Meter:",
        description=desc.DENSITY,
        default=1000.0,
        min=0.001
    )


def define_collision_props(mol):
    mol.selfcollision_active = bpy.props.BoolProperty(
        name="Self",
        description=desc.SELF_COLLISION_ACTIVE,
        default=False
    )
    mol.othercollision_active = bpy.props.BoolProperty(
        name="Others",
        description=desc.OTHER_COLLISION_ACTIVE,
        default=False
    )
    mol.friction = bpy.props.FloatProperty(
        name='Friction:',
        description=desc.FRICTION,
        default=0.005,
        min=0.0,
        max=1.0,
        precision=6,
        subtype='FACTOR'
    )
    mol.collision_damp = bpy.props.FloatProperty(
        name="Damping:",
        description=desc.COLLISION_DAMPING,
        default=0.005,
        min=0.0,
        max=1.0,
        precision=6,
        subtype='FACTOR'
    )
    mol.collision_group = bpy.props.IntProperty(
        name='Collide Only With:',
        default=1,
        min=1,
        description=desc.COLLISION_GROUP
    )


def define_links_general_props(mol):
    mol.links_active = bpy.props.BoolProperty(
        name="Self",
        description=desc.LINKS_ACTIVE,
        default=False
    )
    mol.other_link_active = bpy.props.BoolProperty(
        name="Others",
        description=desc.LINK_OTHER_ACTIVE,
        default=False
        )

    mol.link_group = bpy.props.IntProperty(
        name='Linking only with:',
        default=1,
        min=1,
        description=desc.LINK_GROUP
    )


def define_links_birth_general_props(mol):
    mol.link_rellength = bpy.props.BoolProperty(
        name="Relative",
        description=desc.LINK_RELATIVE_LENGTH,
        default=True
    )
    mol.link_length = bpy.props.FloatProperty(
        name="Search Length", description=desc.LINK_LENGTH,
        min=0.0,
        precision=6,
        default=1.0
    )
    mol.link_max = bpy.props.IntProperty(
        name="Max links", description=desc.LINK_MAX,
        min=0,
        default=16
    )


def define_links_birth_props(mol):
    define_links_birth_general_props(mol)
    define_customizable_props(mol, 'friction', use_same_values=False)
    define_customizable_props(mol, 'tension', use_same_values=False)
    define_customizable_props(mol, 'stiff', use_same_values=True)
    define_customizable_props(mol, 'damp', use_same_values=True)
    define_customizable_props(mol, 'broken', use_same_values=True)


def define_links_collision_general_props(mol):
    mol.relink_group = bpy.props.IntProperty(
        name='Only links with:',
        default=1,
        min=1,
        description=desc.RELINK_GROUP
    )
    mol.relink_max = bpy.props.IntProperty(
        name="Max links",
        description=desc.RELINK_MAX,
        min=0,
        default=16
    )


def define_links_collision_props(mol):
    define_links_collision_general_props(mol)
    define_customizable_props(
        mol,
        'chance',
        use_same_values=False,
        relink=True,
        minimum=0.0,
        maximum=100.0,
        text='Linking'
    )
    define_customizable_props(
        mol,
        'friction',
        use_same_values=False,
        relink=True
    )
    define_customizable_props(
        mol,
        'tension',
        use_same_values=False,
        relink=True
    )
    define_customizable_props(
        mol,
        'stiff',
        use_same_values=True,
        relink=True
    )
    define_customizable_props(
        mol,
        'damp',
        use_same_values=True,
        relink=True
    )
    define_customizable_props(
        mol,
        'broken',
        use_same_values=True,
        relink=True
    )


def define_links_props(mol):
    define_links_general_props(mol)
    define_links_birth_props(mol)
    define_links_collision_props(mol)


def define_general_props(mol):
    mol.active = bpy.props.BoolProperty(
        name="mol.active",
        description=desc.ACTIVE,
        default=False
    )
    mol.refresh = bpy.props.BoolProperty(
        name="mol.refresh",
        description=desc.REFRESH,
        default=True
    )


def define_tools_props(mol):
    mol.var1 = bpy.props.IntProperty(
        name="Current numbers of particles",
        description=desc.VAR_1,
        min=1,
        default=1000
    )
    mol.var2 = bpy.props.IntProperty(
        name="Current substep",
        description=desc.VAR_2,
        min=1,
        default=4
    )
    mol.var3 = bpy.props.IntProperty(
        name="Targeted numbers of particles",
        description=desc.VAR_3,
        min=1,
        default=1000
    )


def define_uv_props(mol):
    mol.bakeuv = bpy.props.BoolProperty(
        name="Bake UV",
        description=desc.BAKE_UV,
        default=False
    )
    mol.uv_name = bpy.props.StringProperty(name='UV Name')


class MolScnProps(bpy.types.PropertyGroup):
    # molecular scene properties
    pass


def define_scene_props():
    bpy.utils.register_class(MolScnProps)

    MolScnProps.timescale_active = bpy.props.BoolProperty(
        name="timescale_active",
        description=desc.TIME_SCALE_ACTIVE,
        default=False
    )
    MolScnProps.timescale = bpy.props.FloatProperty(
        name="timescale",
        description=desc.TIME_SCALE,
        default=1
    )
    MolScnProps.substep = bpy.props.IntProperty(
        name="Steps per Frame",
        description=desc.SUBSTEP,
        min=1,
        max=10_000,
        default=4
    )
    MolScnProps.render = bpy.props.BoolProperty(
        name="Render",
        description=desc.RENDER,
        default=False
    )
    MolScnProps.cpu = bpy.props.IntProperty(
        name="CPU",
        description=desc.CPU,
        default=multiprocessing.cpu_count(),
        min=1,
        max=multiprocessing.cpu_count()
    )
    MolScnProps.cache_folder = bpy.props.StringProperty(
        name='Cache Folder',
        subtype='DIR_PATH'
    )
    MolScnProps.use_cache = bpy.props.BoolProperty(
        name='Use Molecular Cache',
        default=True
    )

    MolScnProps.exportdata = []

    MolScnProps.minsize = bpy.props.FloatProperty()
    MolScnProps.simrun = bpy.props.BoolProperty(default=False)
    MolScnProps.timeremain = bpy.props.StringProperty()
    MolScnProps.newlink = bpy.props.IntProperty()
    MolScnProps.deadlink = bpy.props.IntProperty()
    MolScnProps.totallink = bpy.props.IntProperty()
    MolScnProps.totaldeadlink = bpy.props.IntProperty()
    MolScnProps.objuvbake = bpy.props.StringProperty()
    MolScnProps.psysuvbake = bpy.props.StringProperty()
    MolScnProps.stime = bpy.props.FloatProperty()

    pointer = bpy.props.PointerProperty(type=MolScnProps)
    bpy.types.Scene.mol = pointer


class MolParsProps(bpy.types.PropertyGroup):
    # molecular particles properties
    pass


def define_pars_props():
    bpy.utils.register_class(MolParsProps)

    define_general_props(MolParsProps)
    define_density_props(MolParsProps)
    define_collision_props(MolParsProps)
    define_links_props(MolParsProps)
    define_tools_props(MolParsProps)
    define_uv_props(MolParsProps)

    pointer = bpy.props.PointerProperty(type=MolParsProps)
    bpy.types.ParticleSettings.mol = pointer


def register():
    define_pars_props()
    define_scene_props()


def unregister():
    del bpy.types.ParticleSettings.mol
    bpy.utils.unregister_class(MolParsProps)

    del bpy.types.Scene.mol
    bpy.utils.unregister_class(MolScnProps)
