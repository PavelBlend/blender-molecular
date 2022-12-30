import multiprocessing

import bpy

from . import desc
from . import defs


def define_customizable_props_values(
        parset,
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

    value_prop_name = 'mol_{}_{}'.format(base, name)
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

    setattr(parset, value_prop_name, value_prop)



    # random property

    value_random_prop_name = 'mol_{}_{}rand'.format(base, name)
    default, minimum, maximum = defs.values[value_random_prop_name]

    value_random_prop = bpy.props.FloatProperty(
        name='Random {}'.format(name.capitalize()),
        description='',
        min=minimum,
        max=maximum,
        default=default,
        precision=6, subtype='FACTOR'
    )

    setattr(parset, value_random_prop_name, value_random_prop)



    # texture property

    tex_coeff_prop_name = 'mol_{}_{}tex_coeff'.format(base, name)
    default, minimum, maximum = defs.values[tex_coeff_prop_name]

    tex_coeff_prop = bpy.props.FloatProperty(
        name="Multiply Coefficient",
        default=default,
        min=minimum,
        max=maximum
    )

    setattr(parset, tex_coeff_prop_name, tex_coeff_prop)
    tex_prop = bpy.props.StringProperty(name='Broken Texture')
    setattr(parset, 'mol_{}_{}tex'.format(base, name), tex_prop)


def define_customizable_props(
        parset,
        name,
        use_same_values=True,
        relink=False,
        minimum=0.0,
        maximum=1.0,
        text=None
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
        items=mode_items,
        default='CONSTANT'
    )

    setattr(parset, 'mol_{}link_{}_mode'.format(prefix, name), mode_prop)

    define_customizable_props_values(
        parset,
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

        same_value_name = 'mol_{}link_{}_samevalue'.format(prefix, name)
        setattr(parset, same_value_name, same_value_prop)

        define_customizable_props_values(
            parset,
            name,
            compress=False,
            relink=relink,
            minimum=0.0,
            maximum=1.0,
            text=label
        )


def define_density_props(parset):
    parset.mol_density_active = bpy.props.BoolProperty(
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
    parset.mol_matter = bpy.props.EnumProperty(
        name='Preset',
        items=matter_items,
        description=desc.MATTER
    )
    parset.mol_density = bpy.props.FloatProperty(
        name="Kg Per Cube Meter:",
        description=desc.DENSITY,
        default=1000.0,
        min=0.001
    )


def define_collision_props(parset):
    parset.mol_selfcollision_active = bpy.props.BoolProperty(
        name="Self",
        description=desc.SELF_COLLISION_ACTIVE,
        default=False
    )
    parset.mol_othercollision_active = bpy.props.BoolProperty(
        name="Others",
        description=desc.OTHER_COLLISION_ACTIVE,
        default=False
    )
    parset.mol_friction = bpy.props.FloatProperty(
        name='Friction:',
        description=desc.FRICTION,
        default=0.005,
        min=0.0,
        max=1.0,
        precision=6,
        subtype='FACTOR'
    )
    parset.mol_collision_damp = bpy.props.FloatProperty(
        name="Damping:",
        description=desc.COLLISION_DAMPING,
        default=0.005,
        min=0.0,
        max=1.0,
        precision=6,
        subtype='FACTOR'
    )
    parset.mol_collision_group = bpy.props.IntProperty(
        name='Collide Only With:',
        default=1,
        min=1,
        description=desc.COLLISION_GROUP
    )


def define_links_general_props(parset):
    parset.mol_links_active = bpy.props.BoolProperty(
        name="Self",
        description=desc.LINKS_ACTIVE,
        default=False
    )
    parset.mol_other_link_active = bpy.props.BoolProperty(
        name="Others",
        description=desc.LINK_OTHER_ACTIVE,
        default=False
        )

    parset.mol_link_group = bpy.props.IntProperty(
        name='Linking only with:',
        default=1,
        min=1,
        description=desc.LINK_GROUP
    )


def define_links_birth_general_props(parset):
    parset.mol_link_rellength = bpy.props.BoolProperty(
        name="Relative",
        description=desc.LINK_RELATIVE_LENGTH,
        default=True
    )
    parset.mol_link_length = bpy.props.FloatProperty(
        name="Search Length", description=desc.LINK_LENGTH,
        min=0.0,
        precision=6,
        default=1.0
    )
    parset.mol_link_max = bpy.props.IntProperty(
        name="Max links", description=desc.LINK_MAX,
        min=0,
        default=16
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
        default=1,
        min=1,
        description=desc.RELINK_GROUP
    )
    parset.mol_relink_max = bpy.props.IntProperty(
        name="Max links",
        description=desc.RELINK_MAX,
        min=0,
        default=16
    )


def define_links_collision_props(parset):
    define_links_collision_general_props(parset)
    define_customizable_props(
        parset,
        'chance',
        use_same_values=False,
        relink=True,
        minimum=0.0,
        maximum=100.0,
        text='Linking'
    )
    define_customizable_props(
        parset,
        'friction',
        use_same_values=False,
        relink=True
    )
    define_customizable_props(
        parset,
        'tension',
        use_same_values=False,
        relink=True
    )
    define_customizable_props(
        parset,
        'stiff',
        use_same_values=True,
        relink=True
    )
    define_customizable_props(
        parset,
        'damp',
        use_same_values=True,
        relink=True
    )
    define_customizable_props(
        parset,
        'broken',
        use_same_values=True,
        relink=True
    )


def define_links_props(parset):
    define_links_general_props(parset)
    define_links_birth_props(parset)
    define_links_collision_props(parset)


def define_general_props(parset):
    parset.mol_active = bpy.props.BoolProperty(
        name="mol_active",
        description=desc.ACTIVE,
        default=False
    )
    parset.mol_refresh = bpy.props.BoolProperty(
        name="mol_refresh",
        description=desc.REFRESH,
        default=True
    )


def define_tools_props(parset):
    parset.mol_var1 = bpy.props.IntProperty(
        name="Current numbers of particles",
        description=desc.VAR_1,
        min=1,
        default=1000
    )
    parset.mol_var2 = bpy.props.IntProperty(
        name="Current substep",
        description=desc.VAR_2,
        min=1,
        default=4
    )
    parset.mol_var3=bpy.props.IntProperty(
        name="Targeted numbers of particles",
        description=desc.VAR_3,
        min=1,
        default=1000
    )


def define_uv_props(parset):
    parset.mol_bakeuv = bpy.props.BoolProperty(
        name="mol_bakeuv",
        description=desc.BAKE_UV,
        default=False
    )
    parset.mol_uv_name = bpy.props.StringProperty(name='UV Name')


def define_debug_props(parset):
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


def define_scene_props():
    scn = bpy.types.Scene

    scn.mol_timescale_active = bpy.props.BoolProperty(
        name="mol_timescale_active",
        description=desc.TIME_SCALE_ACTIVE,
        default=False
    )
    scn.timescale = bpy.props.FloatProperty(
        name="timescale",
        description=desc.TIME_SCALE,
        default=1
    )
    scn.mol_substep = bpy.props.IntProperty(
        name="Substeps",
        description=desc.SUBSTEP,
        min=0,
        max=900,
        default=4
    )
    scn.mol_render = bpy.props.BoolProperty(
        name="Render",
        description=desc.RENDER,
        default=False
    )
    scn.mol_cpu = bpy.props.IntProperty(
        name="CPU",
        description=desc.CPU,
        default=multiprocessing.cpu_count(),
        min=1,
        max=multiprocessing.cpu_count()
    )
    scn.mol_cache_folder = bpy.props.StringProperty(
        name='Cache Folder',
        subtype='DIR_PATH'
    )
    scn.mol_use_cache = bpy.props.BoolProperty(
        name='Use Molecular Cache',
        default=True
    )

    scn.mol_exportdata = []

    scn.mol_minsize = bpy.props.FloatProperty()
    scn.mol_simrun = bpy.props.BoolProperty(default=False)
    scn.mol_timeremain = bpy.props.StringProperty()
    scn.mol_old_endframe = bpy.props.IntProperty()
    scn.mol_newlink = bpy.props.IntProperty()
    scn.mol_deadlink = bpy.props.IntProperty()
    scn.mol_totallink = bpy.props.IntProperty()
    scn.mol_totaldeadlink = bpy.props.IntProperty()
    scn.mol_objuvbake = bpy.props.StringProperty()
    scn.mol_psysuvbake = bpy.props.StringProperty()
    scn.mol_stime = bpy.props.FloatProperty()


def define_pars_props():
    parset = bpy.types.ParticleSettings

    define_general_props(parset)
    define_density_props(parset)
    define_collision_props(parset)
    define_links_props(parset)
    define_tools_props(parset)
    define_uv_props(parset)
    define_debug_props(parset)


def register():
    define_pars_props()
    define_scene_props()


def unregister():
    pass
