import bpy

from . import names
from . import utils


def get_bool_text(prop):
    if prop:
        return 'Yes'
    else:
        return 'No'


def draw_prop(layout, owner, prop, text, boolean=False):
    row = layout.row()
    row.label(text=text + ':')

    if boolean:
        bool_text = get_bool_text(getattr(owner, prop))
        row.prop(owner, prop, toggle=True, text=bool_text)

    else:
        row.prop(owner, prop, text='')


def draw_customizable_props(layout, psys, name, same=False, relink=False):
    main_box = layout.box()

    if relink:
        prefix = 're'
    else:
        prefix = ''

    if not same:
        same_value_name = '{}link_{}_samevalue'.format(prefix, name)
        same_value_prop = getattr(psys.settings.mol, same_value_name)
        draw_prop(
            main_box,
            psys.settings.mol,
            same_value_name,
            'Same Values',
            boolean=True
        )
    else:
        same_value_prop = True

    if not same_value_prop:
        box = main_box.box()
        box.label(text='Compression:')
    else:
        box = main_box

    prop_name = '{}link_{}'.format(prefix, name)
    draw_prop(box, psys.settings.mol, prop_name, 'Value')

    rand_name = prop_name + 'rand'
    draw_prop(box, psys.settings.mol, rand_name, 'Random')

    if not same_value_prop:
        box = main_box.box()
        box.label(text='Expansion:')
        exp_name = '{}link_e{}'.format(prefix, name)
        draw_prop(box, psys.settings.mol, exp_name, 'Value')

        exp_rand_name = '{}link_e{}rand'.format(prefix, name)
        draw_prop(box, psys.settings.mol, exp_rand_name, 'Random')


class MolecularBasePanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"
    bl_options = {'DEFAULT_CLOSED', }

    @classmethod
    def poll(cls, context):
        return context.object.particle_systems.active


class MolecularDensityPanel(MolecularBasePanel):
    bl_label = names.DENSITY
    bl_idname = "OBJECT_PT_molecular_density"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol.active
        # for the data    
        psys_eval = utils.get_object(context.object).particle_systems.active

        draw_prop(
            layout,
            psys.settings.mol,
            'density_active',
            'Weight by Density',
            boolean=True
        )

        if not psys.settings.mol.density_active:
            return

        draw_prop(layout, psys.settings.mol, 'matter', 'Preset')

        if int(psys.settings.mol.matter) != -1:
            preset_density = float(psys.settings.mol.matter)
            row = layout.row()
            row.label(text='Density:') 
            row.label(text='{0:.2f} Kg'.format(preset_density))

            pmass = (psys.settings.particle_size ** 3) * preset_density
            row = layout.row()
            row.label(text='Total Weight:') 
            row.label(text='{0:.2f} Kg'.format(len(psys_eval.particles) * pmass)) 
            return

        draw_prop(layout, psys.settings.mol, 'density', 'Density')

        pmass = (psys.settings.particle_size ** 3) * psys.settings.mol.density
        row = layout.row()
        row.label(text='Total Weight:') 
        row.label(text='{0:.2f} Kg'.format(len(psys_eval.particles) * pmass)) 


class MolecularCollisionPanel(MolecularBasePanel):
    bl_label = names.COLLISION
    bl_idname = "OBJECT_PT_molecular_collision"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        # particle system settings
        stg = psys.settings.mol

        layout.enabled = stg.active
        # for the data    
        psys_eval = utils.get_object(context.object).particle_systems.active
        # self collision
        draw_prop(layout, stg, 'selfcollision_active', 'Self', boolean=True)
        # other collision
        draw_prop(layout, stg, 'othercollision_active', 'Other', boolean=True)
        if stg.othercollision_active:
            draw_prop(layout, stg, 'collision_group', 'Group')
        if stg.selfcollision_active or stg.othercollision_active:
            draw_prop(layout, stg, 'friction', 'Friction')
            draw_prop(layout, stg, 'collision_damp', 'Damping')


class MolecularLinksPanel(MolecularBasePanel):
    bl_label = names.LINKS
    bl_idname = "OBJECT_PT_molecular_links"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol.active

        draw_prop(layout, psys.settings.mol, 'links_active', 'Self', boolean=True)
        draw_prop(layout, psys.settings.mol, 'other_link_active', 'Other', boolean=True)
        if psys.settings.mol.other_link_active:
            draw_prop(layout, psys.settings.mol, 'link_group', 'Group')


class MolecularInitLinksPanel(MolecularBasePanel):
    bl_label = names.INITIAL_LINKING
    bl_idname = "OBJECT_PT_molecular_init_links"
    bl_parent_id = 'OBJECT_PT_molecular_links'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings.mol
        layout.enabled = stg.active and (
            stg.links_active or stg.other_link_active
        )
        draw_prop(layout, stg, 'link_rellength', 'Relative', boolean=True)
        draw_prop(layout, stg, 'link_length', 'Search Length')
        draw_prop(layout, stg, 'link_max', 'Max links')


class MolecularInitLinksFrictionPanel(MolecularBasePanel):
    bl_label = names.FRICTION
    bl_idname = "OBJECT_PT_molecular_init_links_friction"
    bl_parent_id = 'OBJECT_PT_molecular_init_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings
        layout.enabled = stg.mol.active and (
            stg.mol.links_active or stg.mol.other_link_active
        )
        draw_customizable_props(layout, psys, 'friction', same=True)


class MolecularInitLinksTensionPanel(MolecularBasePanel):
    bl_label = names.TENSION
    bl_idname = "OBJECT_PT_molecular_init_links_tension"
    bl_parent_id = 'OBJECT_PT_molecular_init_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings
        layout.enabled = stg.mol.active and (
            stg.mol.links_active or stg.mol.other_link_active
        )
        draw_customizable_props(layout, psys, 'tension', same=True)


class MolecularInitLinksStiffnessPanel(MolecularBasePanel):
    bl_label = names.STIFFNESS
    bl_idname = "OBJECT_PT_molecular_init_links_stiffness"
    bl_parent_id = 'OBJECT_PT_molecular_init_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings
        layout.enabled = stg.mol.active and (
            stg.mol.links_active or stg.mol.other_link_active
        )
        draw_customizable_props(layout, psys, 'stiff')


class MolecularInitLinksDampingPanel(MolecularBasePanel):
    bl_label = names.DAMPING
    bl_idname = "OBJECT_PT_molecular_init_links_damping"
    bl_parent_id = 'OBJECT_PT_molecular_init_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings
        layout.enabled = stg.mol.active and (
            stg.mol.links_active or stg.mol.other_link_active
        )
        draw_customizable_props(layout, psys, 'damp')


class MolecularInitLinksBrokenPanel(MolecularBasePanel):
    bl_label = names.BROKEN
    bl_idname = "OBJECT_PT_molecular_init_links_broken"
    bl_parent_id = 'OBJECT_PT_molecular_init_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings
        layout.enabled = stg.mol.active and (
            stg.mol.links_active or stg.mol.other_link_active
        )
        draw_customizable_props(layout, psys, 'broken')


class MolecularNewLinksPanel(MolecularBasePanel):
    bl_label = names.NEW_LINKING
    bl_idname = "OBJECT_PT_molecular_new_links"
    bl_parent_id = 'OBJECT_PT_molecular_links'

    def draw(self, context):
    
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings.mol
        layout.enabled = stg.active and (
            stg.links_active or stg.other_link_active
        )
        draw_prop(layout, stg, 'relink_group', 'Group')
        draw_prop(layout, stg, 'relink_max', 'Max links')


class MolecularNewLinksLinkingPanel(MolecularBasePanel):
    bl_label = 'Linking'
    bl_idname = "OBJECT_PT_molecular_new_links_linking"
    bl_parent_id = 'OBJECT_PT_molecular_new_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings.mol
        layout.enabled = stg.active and (
            stg.links_active or stg.other_link_active
        )
        draw_customizable_props(layout, psys, 'chance', same=True, relink=True)


class MolecularNewLinksFrictionPanel(MolecularBasePanel):
    bl_label = names.FRICTION
    bl_idname = "OBJECT_PT_molecular_new_links_friction"
    bl_parent_id = 'OBJECT_PT_molecular_new_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings.mol
        layout.enabled = stg.active and (
            stg.links_active or stg.other_link_active
        )
        draw_customizable_props(layout, psys, 'friction', same=True, relink=True)


class MolecularNewLinksTensionPanel(MolecularBasePanel):
    bl_label = names.TENSION
    bl_idname = "OBJECT_PT_molecular_new_links_tension"
    bl_parent_id = 'OBJECT_PT_molecular_new_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings.mol
        layout.enabled = stg.active and (
            stg.links_active or stg.other_link_active
        )
        draw_customizable_props(layout, psys, 'tension', same=True, relink=True)


class MolecularNewLinksStiffnessPanel(MolecularBasePanel):
    bl_label = names.STIFFNESS
    bl_idname = "OBJECT_PT_molecular_new_links_stiffness"
    bl_parent_id = 'OBJECT_PT_molecular_new_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings.mol
        layout.enabled = stg.active and (
            stg.links_active or stg.other_link_active
        )
        draw_customizable_props(layout, psys, 'stiff', relink=True)


class MolecularNewLinksDampingPanel(MolecularBasePanel):
    bl_label = names.DAMPING
    bl_idname = "OBJECT_PT_molecular_new_links_damping"
    bl_parent_id = 'OBJECT_PT_molecular_new_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings.mol
        layout.enabled = stg.active and (
            stg.links_active or stg.other_link_active
        )
        draw_customizable_props(layout, psys, 'damp', relink=True)


class MolecularNewLinksBrokenPanel(MolecularBasePanel):
    bl_label = names.BROKEN
    bl_idname = "OBJECT_PT_molecular_new_links_broken"
    bl_parent_id = 'OBJECT_PT_molecular_new_links'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings.mol
        layout.enabled = stg.active and (
            stg.links_active or stg.other_link_active
        )
        draw_customizable_props(layout, psys, 'broken', relink=True)


class MolecularSimulatePanel(MolecularBasePanel):
    bl_label = names.SIMULATE
    bl_idname = "OBJECT_PT_molecular_simulate"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol.active
        # for the data    
        psys_eval = utils.get_object(context.object).particle_systems.active

        box = layout.box()
        box.label(text='General:')
        draw_prop(box, scn.mol, 'cache_folder', 'Cache Folder')
        draw_prop(box, scn.mol, 'use_cache', 'Use Molecular Cache', boolean=True)
        draw_prop(box, scn, 'frame_start', 'Start Frame')
        draw_prop(box, scn, 'frame_end', 'End Frame')

        draw_prop(box, scn.mol, 'substep', 'Substeps')
        draw_prop(box, scn.mol, 'cpu', names.CPU_USED)

        box = layout.box()
        box.label(text='Actions at Ending:')
        draw_prop(box, scn.mol, 'render', 'Render', boolean=True)

        draw_prop(box, psys.settings.mol, 'bakeuv', 'Bake UV', boolean=True)
        row = box.row()
        row.active = psys.settings.mol.bakeuv
        row = row.row()
        row.label(text='UV:')
        row.prop_search(
            psys.settings.mol, 'uv_name', obj.data, 'uv_layers', text=''
        )

        box = layout.box()
        box.label(text='Operators:')
        row = box.row()

        if scn.mol.simrun == False and psys.point_cache.is_baked == False:
            row.enabled = True
            row.operator(
                "object.mol_simulate",
                text="Simulate"
            )
            box.operator("wm.mol_bake_modal", text="Bake")
            row = box.row()
            row.enabled = False
            row.operator("ptcache.free_bake_all", text="Free")

        if psys.point_cache.is_baked == True and scn.mol.simrun == False:
            row.operator(
                "object.mol_simulate",
                text="Simulate"
            )
            row = box.row()
            row.enabled = False
            row.operator("wm.mol_bake_modal", text="Bake")
            row = box.row()
            row.enabled = True
            row.operator("ptcache.free_bake_all", text="Free")

        if scn.mol.simrun == True:
            row.enabled = False
            row.operator(
                "object.mol_simulate",
                text="Process: {} left".format(scn.mol.timeremain)
            )
            row = box.row()
            row.enabled = False
            row.operator("wm.mol_bake_modal", text="Bake")
            row = box.row()
            row.enabled = False
            row.operator("ptcache.free_bake_all", text="Free")


class MolecularToolsPanel(MolecularBasePanel):
    bl_label = names.MOLECULAR_TOOLS
    bl_idname = "OBJECT_PT_molecular_tools"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol.active
        # for the data    
        psys_eval = utils.get_object(context.object).particle_systems.active

        box = layout.box()
        row = box.row()
        row.label(text=names.PARTICLE_UV)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(icon='INFO', text=names.SET_POSITION)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.UV_HELP)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.CYCLES_HELP)
        row = box.row()
        row.operator(
            "object.mol_set_global_uv",
            icon='GROUP_UVS',
            text="Set Global UV"
        )

        row = box.row()
        row.label(text='UV:')
        row.prop_search(
            psys.settings.mol,
            'uv_name',
            obj.data,
            'uv_layers',
            text=''
        )

        row = box.row()

        uv_name = psys.settings.mol.uv_name

        if uv_name:
            uv_info = '(current: "{0}")'.format(uv_name)

            row.operator(
                "object.mol_set_active_uv",
                icon='GROUP_UVS',
                text = 'Set Active UV ' + uv_info
            )
        else:
            row.active = False
            row.operator(
                "object.mol_set_active_uv",
                icon='GROUP_UVS',
                text="Set Active UV (no uvs found)"
            )

        box = layout.box()
        row = box.row()
        row.label(text=names.SUBSTEPS_CALCULATOR)
        row = box.row()
        row.label(text='Particles Count:')
        row.label(text='{}'.format(len(psys_eval.particles)))

        draw_prop(box, psys.settings.mol, 'var1', 'Current Particles Count')
        draw_prop(box, psys.settings.mol, 'var2', 'Current Substeps')
        draw_prop(box, psys.settings.mol, 'var3', 'Targeted Particles Count')

        diff = (psys.settings.mol.var3 / psys.settings.mol.var1)
        factor = psys.settings.mol.var3 ** (1 / 3) / psys.settings.mol.var1 ** (1 / 3)
        newsubstep = int(round(factor * psys.settings.mol.var2))
        row = box.row()
        row.label(text='New Substeps:')
        row.label(text='{}'.format(newsubstep))
        row = box.row()
        row.label(text='Multiply Particles Size by:')
        row.label(text='{}'.format(round(1 / factor, 5)))
        row = box.row()
        row.label(text='Particles Count Changed to:')
        row.label(text='{}'.format(round(diff, 5)))


class MolecularAboutPanel(MolecularBasePanel):
    bl_label = 'About'
    bl_idname = "OBJECT_PT_molecular_about"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol.active
        # for the data    
        psys_eval = utils.get_object(context.object).particle_systems.active

        box = layout.box()
        row = box.row()
        box.active = False
        box.alert = False
        row.alignment = 'CENTER'
        row.label(text=names.THANKS)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.SUPPORT_WORK)
        row = box.row()
        row.alignment = 'CENTER'
        row.operator(
            "wm.url_open",
            text="click here to Donate",
            icon='URL'
        ).url = "www.pyroevil.com/donate/"
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.VISIT)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.SITE)


class MolecularPanel(MolecularBasePanel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Molecular"
    bl_idname = "OBJECT_PT_molecular"

    def draw_header(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        row = layout.row()
        if not psys is None:
            row.prop(psys.settings.mol, 'active', text='')

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol.active


panel_classes = (
    MolecularPanel,
    MolecularSimulatePanel,
    MolecularDensityPanel,
    MolecularCollisionPanel,
    MolecularLinksPanel,
    MolecularInitLinksPanel,
        MolecularInitLinksFrictionPanel,
        MolecularInitLinksTensionPanel,
        MolecularInitLinksStiffnessPanel,
        MolecularInitLinksDampingPanel,
        MolecularInitLinksBrokenPanel,
    MolecularNewLinksPanel,
        MolecularNewLinksLinkingPanel,
        MolecularNewLinksFrictionPanel,
        MolecularNewLinksTensionPanel,
        MolecularNewLinksStiffnessPanel,
        MolecularNewLinksDampingPanel,
        MolecularNewLinksBrokenPanel,
    MolecularToolsPanel,
    MolecularAboutPanel
)


def register():
    for panel in panel_classes:
        bpy.utils.register_class(panel)


def unregister():
    for panel in reversed(panel_classes):
        bpy.utils.unregister_class(panel)
