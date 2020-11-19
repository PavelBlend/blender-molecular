import multiprocessing

import bpy

from . import descriptions, defaults


def define_density_props(parset):
    parset.mol_density_active = bpy.props.BoolProperty(
        name="Calculate Particles Weight by Density",
        description=descriptions.DENSITY_ACTIVE,
        default=False
    )
    matter_items = [
        ("-1", "Custom", descriptions.MATTER_CUSTOM),
        ("1555", "Sand", descriptions.MATTER_SAND),
        ("1000", "Water", descriptions.MATTER_WATER),
        ("7800", "Iron", descriptions.MATTER_IRON)
    ]
    parset.mol_matter = bpy.props.EnumProperty(
        name='Preset',
        items=matter_items,
        description=descriptions.MATTER
    )
    parset.mol_density = bpy.props.FloatProperty(
        name="Kg Per Cube Meter:", description=descriptions.DENSITY,
        default=1000.0, min=0.001
    )


def define_collision_props(parset):
    parset.mol_selfcollision_active = bpy.props.BoolProperty(
        name="Self",
        description=descriptions.SELF_COLLISION_ACTIVE,
        default=False
    )
    parset.mol_othercollision_active = bpy.props.BoolProperty(
        name="Others",
        description=descriptions.OTHER_COLLISION_ACTIVE,
        default=False
    )
    parset.mol_friction = bpy.props.FloatProperty(
        name='Friction:', description=descriptions.FRICTION,
        default=0.005, min=0.0, max=1.0, precision=6, subtype='FACTOR'
    )
    parset.mol_collision_damp = bpy.props.FloatProperty(
        name="Damping:", description=descriptions.COLLISION_DAMPING,
        default=0.005, min=0.0, max=1.0, precision=6, subtype='FACTOR'
    )
    parset.mol_collision_group = bpy.props.IntProperty(
        name='Collide Only With:', default=1, min=1,
        description=descriptions.COLLISION_GROUP
    )


def define_links_general_props(parset):
    parset.mol_links_active = bpy.props.BoolProperty(
        name="Self",
        description=descriptions.LINKS_ACTIVE,
        default=False
    )
    parset.mol_other_link_active = bpy.props.BoolProperty(
        name="Others",
        description=descriptions.LINK_OTHER_ACTIVE, default=False
        )

    parset.mol_link_group = bpy.props.IntProperty(
        name='Linking only with:', default=1, min=1,
        description=descriptions.LINK_GROUP
    )


def define_links_birth_general_props(parset):
    parset.mol_link_rellength = bpy.props.BoolProperty(
        name="Relative",
        description=descriptions.LINK_RELATIVE_LENGTH,
        default=True
    )
    parset.mol_link_length = bpy.props.FloatProperty(
        name="Search Length", description=descriptions.LINK_LENGTH,
        min=0.0, precision=6, default=1
    )
    parset.mol_link_max = bpy.props.IntProperty(
        name="Max links", description=descriptions.LINK_MAX,
        min=0, default=16
    )


def define_customizable_props_values(
        parset, name, compress=True, relink=False,
        minimum=0.0, maximum=1.0, text=None
    ):

    if not compress:
        name = 'e' + name    # expansion property
    base = 'link'
    if relink:
        base = 're' + base
    value_prop_name = 'mol_{}_{}'.format(base, name)
    default, minimum, maximum = defaults.values[value_prop_name]
    if minimum == 0.0 and maximum == 1.0:
        subtype = 'FACTOR'
    else:
        subtype = 'NONE'
    value_prop = bpy.props.FloatProperty(
        name=name.capitalize(), description='',
        min=minimum, max=maximum, default=default, precision=6, subtype=subtype
    )
    setattr(parset, value_prop_name, value_prop)
    value_random_prop_name = 'mol_{}_{}rand'.format(base, name)
    default, minimum, maximum = defaults.values[value_random_prop_name]
    value_random_prop = bpy.props.FloatProperty(
        name='Random {}'.format(name.capitalize()),
        description='',
        min=minimum, max=maximum, default=default, precision=6, subtype='FACTOR'
    )
    setattr(parset, value_random_prop_name, value_random_prop)
    tex_coeff_prop_name = 'mol_{}_{}tex_coeff'.format(base, name)
    default, minimum, maximum = defaults.values[tex_coeff_prop_name]
    tex_coeff_prop = bpy.props.FloatProperty(
        name="Multiply Coefficient", default=default, min=minimum, max=maximum
    )
    setattr(parset, tex_coeff_prop_name, tex_coeff_prop)
    tex_prop = bpy.props.StringProperty(name='Broken Texture')
    setattr(parset, 'mol_{}_{}tex'.format(base, name), tex_prop)


def define_customizable_props(
        parset, name, use_same_values=True, relink=False,
        minimum=0.0, maximum=1.0, text=None
    ):

    mode_items = [
        ('CONSTANT', 'Constant', ''),
        ('RANDOM', 'Random', ''),
        ('TEXTURE', 'Texture', '')
    ]
    if text:
        label = text
    else:
        label = name.capitalize()
    prefix = ''
    if relink:
        prefix = 're'
    mode_prop = bpy.props.EnumProperty(
        name='{} Mode'.format(label),
        items=mode_items, default='CONSTANT'
    )
    setattr(parset, 'mol_{}link_{}_mode'.format(prefix, name), mode_prop)
    define_customizable_props_values(
        parset, name, relink=relink, minimum=0.0, maximum=1.0, text=label
    )
    if use_same_values:
        same_value_prop = bpy.props.BoolProperty(
            name="Same values for compression/expansion",
            description=descriptions.LINK_SAME_VALUE,
            default=True
        )
        setattr(parset, 'mol_{}link_{}_samevalue'.format(prefix, name), same_value_prop)
        define_customizable_props_values(
            parset, name, compress=False, relink=relink,
            minimum=0.0, maximum=1.0, text=label
        )


def define_links_birth_props(parset):
    define_links_birth_general_props(parset)
    define_customizable_props(parset, 'friction', use_same_values=False)
    define_customizable_props(parset, 'tension', use_same_values=False)
    define_customizable_props(parset, 'stiff', use_same_values=True)
    define_customizable_props(parset, 'damp', use_same_values=True)
    define_customizable_props(parset, 'broken', use_same_values=True)


def define_links_collision_general_props(parset):
    parset.mol_relink_group = bpy.props.IntProperty(
        name='Only links with:',
        default=1, min=1, description=descriptions.RELINK_GROUP
    )
    parset.mol_relink_max = bpy.props.IntProperty(
        name="Max links",
        description=descriptions.RELINK_MAX,
        min=0, default=16
    )


def define_links_collision_props(parset):
    define_links_collision_general_props(parset)
    define_customizable_props(
        parset, 'chance', use_same_values=False, relink=True,
        minimum=0.0, maximum=100.0, text='Linking'
    )
    define_customizable_props(parset, 'friction', use_same_values=False, relink=True)
    define_customizable_props(parset, 'tension', use_same_values=False, relink=True)
    define_customizable_props(parset, 'stiff', use_same_values=True, relink=True)
    define_customizable_props(parset, 'damp', use_same_values=True, relink=True)
    define_customizable_props(parset, 'broken', use_same_values=True, relink=True)


def define_links_props(parset):
    define_links_general_props(parset)
    define_links_birth_props(parset)
    define_links_collision_props(parset)


def define_general_props(parset):
    parset.mol_active = bpy.props.BoolProperty(
        name="mol_active", description=descriptions.ACTIVE, default=False
    )
    parset.mol_refresh = bpy.props.BoolProperty(
        name="mol_refresh", description=descriptions.REFRESH, default=True
    )


def define_props():
    parset = bpy.types.ParticleSettings
    define_general_props(parset)
    define_density_props(parset)
    define_collision_props(parset)
    define_links_props(parset)
    parset.mol_var1 = bpy.props.IntProperty(
        name="Current numbers of particles",
        description=descriptions.VAR_1,
        min=1, default=1000
    )
    parset.mol_var2 = bpy.props.IntProperty(
        name="Current substep",
        description=descriptions.VAR_2,
        min=1, default=4
    )
    parset.mol_var3=bpy.props.IntProperty(
        name="Targeted numbers of particles",
        description=descriptions.VAR_3,
        min=1, default=1000
    )
    parset.mol_bakeuv = bpy.props.BoolProperty(
        name="mol_bakeuv",
        description=descriptions.BAKE_UV,
        default=False
    )
    # debug particle attribute
    parset.mol_use_debug_par_attr = bpy.props.BoolProperty(default=False)
    items = (
        # link
        ('LINK_FRICTION', 'Link Friction', ''),
        ('LINK_TENSION', 'Link Tension', ''),
        ('LINK_STIFFNESS', 'Link C-Stiffness', ''),
        ('LINK_ESTIFFNESS', 'Link E-Stiffness', ''),
        ('LINK_DAMPING', 'Link C-Damping', ''),
        ('LINK_EDAMPING', 'Link E-Damping', ''),
        ('LINK_BROKEN', 'Link C-Broken', ''),
        ('LINK_EBROKEN', 'Link E-Broken', ''),
        # relink
        ('RELINK_FRICTION', 'Relink Friction', ''),
        ('RELINK_TENSION', 'Relink Tension', ''),
        ('RELINK_STIFFNESS', 'Relink C-Stiffness', ''),
        ('RELINK_ESTIFFNESS', 'Relink E-Stiffness', ''),
        ('RELINK_DAMPING', 'Relink C-Damping', ''),
        ('RELINK_EDAMPING', 'Relink E-Damping', ''),
        ('RELINK_BROKEN', 'Relink C-Broken', ''),
        ('RELINK_EBROKEN', 'Relink E-Broken', ''),
        ('RELINK_LINKING', 'Relink Linking', '')
    )
    parset.mol_debug_par_attr_name = bpy.props.EnumProperty(
        items=items, name='Attribute Name'
    )
    bpy.types.Scene.mol_timescale_active = bpy.props.BoolProperty(
        name="mol_timescale_active",
        description=descriptions.TIME_SCALE_ACTIVE,
        default=False
    )
    bpy.types.Scene.timescale = bpy.props.FloatProperty(
        name="timescale",
        description=descriptions.TIME_SCALE,
        default=1
    )
    bpy.types.Scene.mol_substep = bpy.props.IntProperty(
        name="Substeps",
        description=descriptions.SUBSTEP,
        min=0, max=900, default=4
    )
    bpy.types.Scene.mol_bake = bpy.props.BoolProperty(
        name="Bake All",
        description=descriptions.BAKE,
        default=True
    )
    bpy.types.Scene.mol_render = bpy.props.BoolProperty(
        name="Render",
        description=descriptions.RENDER,
        default=False
    )
    bpy.types.Scene.mol_cpu = bpy.props.IntProperty(
        name="CPU",
        description=descriptions.CPU,
        default=multiprocessing.cpu_count(),
        min=1, max=multiprocessing.cpu_count()
    )
    bpy.types.Scene.mol_exportdata = []
    bpy.types.Scene.mol_minsize = bpy.props.FloatProperty()
    bpy.types.Scene.mol_simrun = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.mol_timeremain = bpy.props.StringProperty()
    bpy.types.Scene.mol_old_endframe = bpy.props.IntProperty()
    bpy.types.Scene.mol_newlink = bpy.props.IntProperty()
    bpy.types.Scene.mol_deadlink = bpy.props.IntProperty()
    bpy.types.Scene.mol_totallink = bpy.props.IntProperty()
    bpy.types.Scene.mol_totaldeadlink = bpy.props.IntProperty()
    bpy.types.Scene.mol_objuvbake = bpy.props.StringProperty()
    bpy.types.Scene.mol_psysuvbake = bpy.props.StringProperty()
    bpy.types.Scene.mol_stime = bpy.props.FloatProperty()
    bpy.types.Scene.mol_cache_folder = bpy.props.StringProperty(
        name='Cache Folder', subtype='DIR_PATH'
    )
