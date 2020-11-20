import bpy

from . import names
from .utils import get_object


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
        same_value_prop = getattr(psys.settings, 'mol_{}link_{}_samevalue'.format(prefix, name))
        draw_prop(
            main_box, psys.settings, 'mol_{}link_{}_samevalue'.format(prefix, name),
            'Same Values', boolean=True
        )
    else:
        same_value_prop = True
    if not same_value_prop:
        draw_prop(main_box, psys.settings, 'mol_{}link_{}_mode'.format(prefix, name), 'Mode')
        box = main_box.box()
        box.label(text='Compression:')
    else:
        box = main_box
        draw_prop(box, psys.settings, 'mol_{}link_{}_mode'.format(prefix, name), 'Mode')
    mode = getattr(psys.settings, 'mol_{}link_{}_mode'.format(prefix, name))
    if mode in ('CONSTANT', 'RANDOM'):
        draw_prop(box, psys.settings, 'mol_{}link_{}'.format(prefix, name), 'Value')
        if mode == 'RANDOM':
            draw_prop(box, psys.settings, 'mol_{}link_{}rand'.format(prefix, name), 'Random')
        if not same_value_prop:
            box = main_box.box()
            box.label(text='Expansion:')
            draw_prop(box, psys.settings, 'mol_{}link_e{}'.format(prefix, name), 'Value')
            if mode == 'RANDOM':
                draw_prop(box, psys.settings, 'mol_{}link_e{}rand'.format(prefix, name), 'Random')
    elif mode == 'TEXTURE':
        draw_prop(box, psys.settings, 'mol_{}link_{}tex_coeff'.format(prefix, name), 'Coefficient')
        row = box.row()
        row.label(text='Texture:')
        row.prop_search(
            psys.settings, 'mol_{}link_{}tex'.format(prefix, name),
            bpy.data, 'textures', text=''
        )
        if not same_value_prop:
            box = main_box.box()
            box.label(text='Expansion:')
            draw_prop(box, psys.settings, 'mol_{}link_e{}tex_coeff'.format(prefix, name), 'Coefficient')
            row = box.row()
            row.label(text='Texture:')
            row.prop_search(
                psys.settings, 'mol_{}link_e{}tex'.format(prefix, name),
                bpy.data, 'textures', text=''
            )


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
        layout.enabled = psys.settings.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

        draw_prop(
            layout, psys.settings, 'mol_density_active',
            'Weight by Density', boolean=True
        )

        if not psys.settings.mol_density_active:
            return

        draw_prop(layout, psys.settings, 'mol_matter', 'Preset')

        if int(psys.settings.mol_matter) >= 1:
            row = layout.row()
            row.label(text='Total Weight:') 
            row.label(text='{0:.2} Kg'.format(psys.settings.mol_matter))
            return

        draw_prop(layout, psys.settings, 'mol_density', 'Density')
        pmass = (psys.settings.particle_size ** 3) * psys.settings.mol_density
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
        stg = psys.settings

        layout.enabled = stg.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active
        # self collision
        draw_prop(layout, stg, 'mol_selfcollision_active', 'Self', boolean=True)
        # other collision
        draw_prop(layout, stg, 'mol_othercollision_active', 'Other', boolean=True)
        if stg.mol_othercollision_active:
            draw_prop(layout, stg, 'mol_collision_group', 'Group')
        if stg.mol_selfcollision_active or stg.mol_othercollision_active:
            draw_prop(layout, stg, 'mol_friction', 'Friction')
            draw_prop(layout, stg, 'mol_collision_damp', 'Damping')


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
        layout.enabled = psys.settings.mol_active

        draw_prop(layout, psys.settings, 'mol_links_active', 'Self', boolean=True)
        draw_prop(layout, psys.settings, 'mol_other_link_active', 'Other', boolean=True)


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
        stg = psys.settings
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
        )
        draw_prop(layout, psys.settings, 'mol_link_rellength', 'Relative', boolean=True)
        draw_prop(layout, psys.settings, 'mol_link_length', 'Search Length')
        draw_prop(layout, psys.settings, 'mol_link_group', 'Group')
        draw_prop(layout, psys.settings, 'mol_link_max', 'Max links')


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
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        stg = psys.settings
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
        )
        draw_prop(layout, psys.settings, 'mol_relink_group', 'Group')
        draw_prop(layout, psys.settings, 'mol_relink_max', 'Max links')

        '''
        row = layout.row()
        row.prop(psys.settings, "mol_relink_group")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_chance")
        row.prop(psys.settings, "mol_relink_chancerand")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_max")
        row = layout.row()
        layout.separator()
        row = layout.row()
        row.prop(psys.settings,"mol_relink_tension")
        row.prop(psys.settings,"mol_relink_tensionrand")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_stiff_samevalue", toggle=True)
        if not psys.settings.mol_relink_stiff_samevalue:
            layout.label(text='Compression:')
        row = layout.row()
        row.prop(psys.settings,"mol_relink_stiff")
        row.prop(psys.settings,"mol_relink_stiffrand")
        #row = layout.row()
        #row.prop(psys.settings, "mol_relink_stiffexp")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_damp")
        row.prop(psys.settings, "mol_relink_damprand")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_broken")
        row.prop(psys.settings, "mol_relink_brokenrand")
        row = layout.row()
        if not psys.settings.mol_relink_stiff_samevalue:
            layout.label(text='Expansion:')
            row = layout.row()
            row.prop(psys.settings, "mol_relink_estiff")
            row.prop(psys.settings, "mol_relink_estiffrand")
            #row = layout.row()
            #row.enabled = not psys.settings.mol_relink_samevalue
            #row.prop(psys.settings, "mol_relink_estiffexp")
            row = layout.row()
            row.prop(psys.settings, "mol_relink_edamp")
            row.prop(psys.settings, "mol_relink_edamprand")
            row = layout.row()
            row.prop(psys.settings, "mol_relink_ebroken")
            row.prop(psys.settings, "mol_relink_ebrokenrand")
            '''


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
        stg = psys.settings
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        stg = psys.settings
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        stg = psys.settings
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        stg = psys.settings
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        stg = psys.settings
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        stg = psys.settings
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
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
        layout.enabled = psys.settings.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

        box = layout.box()
        box.label(text='General:')
        draw_prop(box, scn, 'mol_cache_folder', 'Cache Folder')
        draw_prop(box, scn, 'frame_start', 'Start Frame')
        draw_prop(box, scn, 'frame_end', 'End Frame')

        # row = layout.row()
        # row.prop(scn,"mol_timescale_active", text="Activate TimeScaling")
        # row = layout.row()
        # row.enabled = scn.mol_timescale_active
        # row.prop(scn, "timescale", text="Time Scale")

        draw_prop(box, scn, 'mol_substep', 'Substeps')
        draw_prop(box, scn, 'mol_cpu', names.CPU_USED)

        box = layout.box()
        box.label(text='Actions at Ending:')
        draw_prop(box, scn, 'mol_render', 'Render', boolean=True)

        draw_prop(box, psys.settings, 'mol_bakeuv', 'Bake UV', boolean=True)
        row = box.row()
        row.active = psys.settings.mol_bakeuv
        row = row.row()
        row.label(text='UV:')
        row.prop_search(
            psys.settings, 'mol_uv_name', obj.data, 'uv_layers', text=''
        )

        box = layout.box()
        box.label(text='Operators:')
        row = box.row()

        if scn.mol_simrun == False and psys.point_cache.is_baked == False:
            row.enabled = True
            row.operator(
                "object.mol_simulate",
                text="Simulate"
            )
            box.operator("wm.mol_bake_modal", text="Bake")
            row = box.row()
            row.enabled = False
            row.operator("ptcache.free_bake_all", text="Free")

        if psys.point_cache.is_baked == True and scn.mol_simrun == False:
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

        if scn.mol_simrun == True:
            row.enabled = False
            row.operator(
                "object.mol_simulate",
                text="Process: {} left".format(scn.mol_timeremain)
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
        layout.enabled = psys.settings.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

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

        if obj.data.uv_layers.active != None:
            row.operator(
                "object.mol_set_active_uv",
                icon='GROUP_UVS',
                text = "Set Active UV (current: \"{0}\")".format(
                    obj.data.uv_layers.active.name
                )
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

        draw_prop(box, psys.settings, 'mol_var1', 'Current Particles Count')
        draw_prop(box, psys.settings, 'mol_var2', 'Current Substeps')
        draw_prop(box, psys.settings, 'mol_var3', 'Targeted Particles Count')

        diff = (psys.settings.mol_var3 / psys.settings.mol_var1)
        factor = psys.settings.mol_var3 ** (1 / 3) / psys.settings.mol_var1 ** (1 / 3)
        newsubstep = int(round(factor * psys.settings.mol_var2))
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
        layout.enabled = psys.settings.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

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


class MolecularDebugPanel(MolecularBasePanel):
    bl_label = 'Degug'
    bl_idname = "OBJECT_PT_molecular_debug"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

        draw_prop(
            layout, psys.settings, 'mol_use_debug_par_attr',
            'Debug Particles', boolean=True
        )
        if psys.settings.mol_use_debug_par_attr:
            draw_prop(layout, psys.settings, 'mol_debug_par_attr_name', 'Attribute')


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
            row.prop(psys.settings, "mol_active", text='')

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol_active


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
    MolecularDebugPanel,
    MolecularAboutPanel
)
