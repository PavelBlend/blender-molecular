# standart modules
import os
import time

# blender modules
import bpy
import numpy
import mathutils

# addon modules
from . import sim
from . import core
from . import cache
from . import utils


baking = False


class MolSimulate(bpy.types.Operator):
    bl_idname = "object.mol_simulate"
    bl_label = 'Simulate'

    def execute(self, context):
        print('-' * 79)
        print('Molecular Simulation Start')

        stime = time.time()

        scene = context.scene
        mol = scene.mol

        # check cache folder
        cache_folder = bpy.path.abspath(mol.cache_folder)
        if cache_folder:
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)
        else:
            self.report({'ERROR'}, 'Cache folder not specified!')
            return {'CANCELLED'}

        # remove preview baked files
        for file in os.listdir(cache_folder):
            file_path = os.path.join(cache_folder, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[-1]
                if ext in ('.bin', '.npy'):
                    os.remove(file_path)

        for ob in bpy.data.objects:
            utils.destroy_caches(ob)

        etime = time.time()
        print("    Remove Preview Bake Files: {:.3f} sec".format(etime - stime))

        stime = time.time()

        # molecular settings
        mol.simrun = True
        mol.minsize = 1000000000.0
        mol.newlink = 0
        mol.deadlink = 0
        mol.totallink = 0
        mol.totaldeadlink = 0
        mol.timeremain = "...Simulating..."

        # scene settings
        mol_substep = scene.mol.substep

        scene.frame_set(frame=scene.frame_start)

        # fps
        if scene.mol.timescale_active:
            fps = scene.render.fps * scene.mol.timescale
        else:
            fps = scene.render.fps

        # init export data
        cpu = scene.mol.cpu
        mol_exportdata = scene.mol.exportdata
        mol_exportdata.clear()
        mol_exportdata.append([
            fps,
            mol_substep,
            0,    # particle systems count
            0,    # particles count
            cpu
        ])

        etime = time.time()
        print("    Init Settings: {:.3f} sec".format(etime - stime))

        # pack export data
        stime = time.time()

        sim.pack_data(context, True)

        etime = time.time()
        print("    Pack Data: {:.3f} sec".format(etime - stime))

        # export
        stime = time.time()
        mol_report = core.init(mol_exportdata)

        etime = time.time()
        print("    Init Core: {:.3f} sec".format(etime - stime))

        print("    Total Numbers of Particles: {}".format(mol_report))
        print("    Start processing:")

        bpy.ops.wm.mol_simulate_modal()
        return {'FINISHED'}


class MolSetGlobalUV(bpy.types.Operator):
    bl_idname = "object.mol_set_global_uv"
    bl_label = "Mol Set UV"

    def execute(self, context):
        scene = context.scene
        obj = utils.get_object(context.object)

        psys = obj.particle_systems.active
        coord = numpy.zeros(3 * len(psys.particles), dtype=numpy.float32)
        psys.particles.foreach_get("location", coord)
        psys.particles.foreach_set("angular_velocity", coord)

        return {'FINISHED'}


class MolSetActiveUV(bpy.types.Operator):
    bl_idname = "object.mol_set_active_uv"
    bl_label = "Mol Set Active UV"

    def execute(self, context):
        scene = context.scene

        # don't use rotation data here from cache, only for render mode
        psys_orig = context.object.particle_systems.active
        psys_orig.settings.use_rotations = False

        obj = utils.get_object(context.object)

        scene.mol.objuvbake = obj.name
        scene.mol.psysuvbake = obj.particle_systems.active.name
        psys = obj.particle_systems[scene.mol.psysuvbake]

        if not psys.settings.mol.bakeuv:
            return {'FINISHED'}

        uv_name = psys.settings.mol.uv_name

        if uv_name:
            if not obj.data.uv_layers.get(uv_name):
                self.report(
                    {'ERROR'},
                    'Can\'not find UV-Map: "{}"'.format(uv_name)
                )
                return {'FINISHED'}
        else:
            self.report({'ERROR'}, 'UV map not specified!')
            return {'FINISHED'}

        print('  start bake uv from:', obj.name)

        obdata = obj.data.copy()
        obj2 = bpy.data.objects.new(name="mol_uv_temp", object_data=obdata)
        obj2.matrix_world = obj.matrix_world

        context.scene.collection.objects.link(obj2)
        mod = obj2.modifiers.new("tri_for_uv", "TRIANGULATE")
        mod.ngon_method = 'BEAUTY'
        mod.quad_method = 'BEAUTY'

        ctx = bpy.context.copy()
        ctx["object"] = obj2
        bpy.ops.object.modifier_apply(ctx, modifier=mod.name)

        context.view_layer.update()

        par_uv = []
        me = obj2.data

        for par in psys.particles:

            parloc = (par.location @ obj2.matrix_world) - obj2.location

            point = obj2.closest_point_on_mesh(parloc)

            vindex1 = me.polygons[point[3]].vertices[0]
            vindex2 = me.polygons[point[3]].vertices[1]
            vindex3 = me.polygons[point[3]].vertices[2]

            v1 = (obj2.matrix_world @ me.vertices[vindex1].co).to_tuple()
            v2 = (obj2.matrix_world @ me.vertices[vindex2].co).to_tuple()
            v3 = (obj2.matrix_world @ me.vertices[vindex3].co).to_tuple()

            uvindex1 = me.polygons[point[3]].loop_start
            uvindex2 = me.polygons[point[3]].loop_start + 1
            uvindex3 = me.polygons[point[3]].loop_start + 2

            uv1 = me.uv_layers[uv_name].data[uvindex1].uv.to_3d()
            uv2 = me.uv_layers[uv_name].data[uvindex2].uv.to_3d()
            uv3 = me.uv_layers[uv_name].data[uvindex3].uv.to_3d()

            p = obj2.matrix_world @ point[1]

            v1 = mathutils.Vector(v1)
            v2 = mathutils.Vector(v2)
            v3 = mathutils.Vector(v3)

            uv1 = mathutils.Vector(uv1)
            uv2 = mathutils.Vector(uv2)
            uv3 = mathutils.Vector(uv3)

            newuv = mathutils.geometry.barycentric_transform(
                p,
                v1, v2, v3,
                uv1, uv2, uv3
            )

            parloc = par.location @ obj2.matrix_world

            dist = (mathutils.Vector((
                parloc[0] - p[0],
                parloc[1] - p[1],
                parloc[2] - p[2]
            ))).length

            newuv[2] = dist
            newuv = newuv.to_tuple()
            par.angular_velocity = newuv
            par_uv.append(newuv)

        scene.collection.objects.unlink(obj2)
        bpy.data.objects.remove(obj2)
        bpy.data.meshes.remove(obdata)

        print('         uv baked on:', psys.settings.name)
        context.object["par_uv"] = par_uv   

        return {'FINISHED'}


def convert_time_to_string(total_time):
    HOUR_IN_SECONDS = 60 * 60
    MINUTE_IN_SCEONDS = 60
    time_string = ''
    if total_time > 10.0:
        total_time = int(total_time)
        if total_time > MINUTE_IN_SCEONDS and total_time <= HOUR_IN_SECONDS:
            minutes = total_time // MINUTE_IN_SCEONDS
            seconds = total_time - minutes * MINUTE_IN_SCEONDS
            time_string = '{0} min {1} sec'.format(minutes, seconds)
        elif total_time <= MINUTE_IN_SCEONDS:
            time_string = '{0} seconds'.format(total_time)
        elif total_time > HOUR_IN_SECONDS:
            hours = total_time // HOUR_IN_SECONDS
            minutes = total_time - (total_time // HOUR_IN_SECONDS) * HOUR_IN_SECONDS
            time_string = '{0} hours {1} min'.format(hours, minutes)
    else:
        seconds = round(total_time, 2)
        time_string = '{0} seconds'.format(seconds)
    return time_string


class MolSimulateModal(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.mol_simulate_modal"
    bl_label = "Simulate Molecular"
    _timer = None

    def check_write_uv_cache(self, context):
        for ob in bpy.data.objects:
            obj = utils.get_object(ob)

            for psys in obj.particle_systems:

                # prepare object as in "open" the cache for angular velocity data
                if context.scene.frame_current == context.scene.frame_start:   
                    psys.settings.use_rotations = True
                    psys.settings.angular_velocity_mode = 'RAND'

                if psys.settings.mol.bakeuv and "par_uv" in ob:
                    par_uv = ob["par_uv"]
                    print("Writing UV data...")
                    for k, par in enumerate(psys.particles):
                        par.angular_velocity = par_uv[k]
    
    def check_bake_uv(self, context):
        # bake the UV in the beginning, and store coordinates in custom property 
        scene = context.scene
        frame_old = scene.frame_current

        for ob in bpy.data.objects:
            obj = utils.get_object(ob)

            for psys in obj.particle_systems:
                if psys.settings.mol.bakeuv:
                    
                    scene.mol.objuvbake = obj.name
                    context.view_layer.update()

                    scene.frame_set(frame=scene.frame_start)
                    context.view_layer.update()

                    bpy.ops.object.mol_set_active_uv()

        scene.frame_set(frame=frame_old)

    def modal(self, context, event):
        scene = context.scene
        frame_end = scene.frame_end
        mol_substep = scene.mol.substep

        frame_float = self.step / mol_substep
        frame_current = int(frame_float)
        subframe = frame_float - frame_current

        if event.type == 'ESC' or frame_current == frame_end:
            for ob in bpy.data.objects:
                obj = utils.get_object(ob)
                for psys in obj.particle_systems:
                    if psys.settings.mol.active and len(psys.particles):
                        par_cache = cache.ParticlesIO()
                        par_cache.add_attr(cache.VELOCITY)
                        name = '{}_{:0>6}'.format(psys.point_cache.name, frame_current)
                        cache_folder = bpy.path.abspath(scene.mol.cache_folder)
                        file_path = os.path.join(cache_folder, name)
                        if not os.path.exists(cache_folder):
                            os.makedirs(cache_folder)
                        par_cache.write(psys, file_path)

            context.view_layer.update()

            # self.check_bake_uv(context)

            if frame_current == frame_end and scene.mol.render:
                bpy.ops.render.render(animation=True)

            scene.frame_set(frame=scene.frame_start)

            core.memfree()
            scene.mol.simrun = False
            mol_exportdata = scene.mol.exportdata
            mol_exportdata.clear()
            print('-' * 50 + 'Molecular Sim end')
            # total time
            tt = time.time() - self.st
            # total time string
            tt_s = convert_time_to_string(tt)
            self.report({'INFO'}, 'Total time: {0}'.format(tt_s))
            print('Total time: {0}'.format(tt_s))
            return self.cancel(context)

        if event.type == 'TIMER':

            step_start = time.time()

            print('-'*79)
            print('Step: {}'.format(self.step))
            self.step += 1

            if frame_current == scene.frame_start:
                scene.mol.stime = time.time()

            # pack data
            stime = time.time()

            mol_exportdata = context.scene.mol.exportdata
            mol_exportdata.clear()
            sim.pack_data(context, False)

            etime = time.time()
            print("    Pack Data: {:.3f} sec".format(etime - stime))
            print()

            # core simulate
            stime = time.time()

            mol_importdata = core.simulate(mol_exportdata)

            etime = time.time()
            print("    Core Simulation: {:.3f} sec".format(etime - stime))

            # particle systems update
            stime = time.time()

            i = 0
            for ob in bpy.data.objects:
                obj = utils.get_object(ob)

                for psys in obj.particle_systems:
                    if psys.settings.mol.active and len(psys.particles):
                        psys.particles.foreach_set('velocity', mol_importdata[0][i])
                        if frame_float == int(frame_float):
                            par_cache = cache.ParticlesIO()
                            par_cache.add_attr(cache.VELOCITY)
                            name = '{}_{:0>6}'.format(psys.point_cache.name, int(frame_float))
                            cache_folder = bpy.path.abspath(scene.mol.cache_folder)
                            file_path = os.path.join(cache_folder, name)
                            if not os.path.exists(cache_folder):
                                os.makedirs(cache_folder)
                            par_cache.write(psys, file_path)
                        i += 1

            etime = time.time()
            print("    Particle Systems Update: {:.3f} sec".format(etime - stime))

            if frame_float == int(frame_float):
                etime = time.time()
                print("    Frame {}:".format(frame_current + 1))
                print("    Links Created:", scene.mol.newlink)
                if scene.mol.totallink:
                    print("    Links Broked:", scene.mol.deadlink)
                    print("    Total Links:", scene.mol.totallink - scene.mol.totaldeadlink ,"/", scene.mol.totallink," (",round((((scene.mol.totallink - scene.mol.totaldeadlink) / scene.mol.totallink) * 100), 2), "%)")
                remain = (((etime - scene.mol.stime) * (scene.frame_end - frame_current - 1)))
                days = int(time.strftime('%d', time.gmtime(remain))) - 1
                scene.mol.timeremain = time.strftime(str(days) + ' days %H hours %M mins %S secs', time.gmtime(remain))
                print("    Remaining Estimated:", scene.mol.timeremain)
                scene.mol.newlink = 0
                scene.mol.deadlink = 0
                scene.mol.stime = time.time()

            stime2 = time.time()

            scene.mol.newlink += mol_importdata[1]
            scene.mol.deadlink += mol_importdata[2]
            scene.mol.totallink = mol_importdata[3]
            scene.mol.totaldeadlink = mol_importdata[4]

            # free velocity memory
            for velocity in mol_importdata[0]:
                velocity.clear()

            self.check_write_uv_cache(context)
            scene.frame_set(frame=frame_current, subframe=subframe)

            etime2 = time.time()
            print("    Blender Frame Set: {:.3f} sec".format(etime2 - stime2))
            print()

            step_end = time.time()
            print("Step Time: {:.3f} sec".format(step_end - step_start))

        return {'PASS_THROUGH'}

    def execute(self, context):
        # start time
        self.st = time.time()
        self.check_bake_uv(context)
        self.step = 0
        self._timer = context.window_manager.event_timer_add(0.000000001, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'}


class MolBakeModal(bpy.types.Operator):
    bl_idname = "wm.mol_bake_modal"
    bl_label = "Bake Molecular"
    _timer = None

    def modal(self, context, event):
        scene = context.scene
        frame_end = scene.frame_end
        frame_current = scene.frame_current
        if event.type == 'ESC' or frame_current == frame_end:
            fake_context = context.copy()
            for ob in bpy.data.objects:
                obj = utils.get_object(ob)
                for psys in obj.particle_systems:
                    if psys.settings.mol.active and len(psys.particles):
                        fake_context["point_cache"] = psys.point_cache
                        bpy.ops.ptcache.bake_from_cache(fake_context)
            context.view_layer.update()
            scene.frame_set(frame=scene.frame_start)
            return self.cancel(context)
        if event.type == 'TIMER':
            scene.frame_set(frame=frame_current + 1)
        return {'PASS_THROUGH'}

    def execute(self, context):
        for ob in bpy.data.objects:
            obj = utils.get_object(ob)
            for psys in obj.particle_systems:
                if psys.settings.mol.active:
                    base_psys = ob.particle_systems[psys.name]
                    base_psys.settings.use_rotations = True
                    base_psys.settings.rotation_mode = 'NONE'
                    base_psys.settings.angular_velocity_mode = 'NONE'
        global baking
        baking = True
        scene = context.scene
        scene.frame_set(frame=scene.frame_start)
        self._timer = context.window_manager.event_timer_add(0.000000001, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        global baking
        baking = False
        context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'}


ops_classes = (
    MolSimulateModal,
    MolSimulate,
    MolSetGlobalUV,
    MolSetActiveUV,
    MolBakeModal
)


def register():
    for op_class in ops_classes:
        bpy.utils.register_class(op_class)


def unregister():
    for op_class in reversed(ops_classes):
        bpy.utils.unregister_class(op_class)
