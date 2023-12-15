import os

import bpy
import numpy

from . import utils
from . import cache


is_rendering = False


def get_par_attrs(cache_name, cache_folder, frame_index):
    cache_file_name = '{}_{:0>6}'.format(cache_name, frame_index)
    cache_file_path = os.path.join(cache_folder, cache_file_name)
    full_path = cache_file_path + cache.EXT_HEAD

    if not os.path.exists(full_path):
        return

    if not os.path.isfile(full_path):
        return

    par_cache = cache.ParticlesIO()
    par_attrs = par_cache.read(cache_file_path)

    return par_attrs


@bpy.app.handlers.persistent
def render_post_handler(scene):
    global is_rendering
    is_rendering = False


@bpy.app.handlers.persistent
def render_init_handler(scene):
    global is_rendering
    is_rendering = True


@bpy.app.handlers.persistent
def frame_change_post_handler(scene):
    if not scene.mol.use_cache:
        return

    global is_rendering

    if is_rendering:
        return

    if scene.mol.simrun:
        return

    cache_folder = bpy.path.abspath(scene.mol.cache_folder)

    for obj in bpy.data.objects:
        obj = utils.get_object(obj)

        for psys in obj.particle_systems:

            if not psys.settings.mol.active:
                continue

            if psys.point_cache.is_baked:
                continue

            frame_index = scene.frame_current
            cache_name = psys.point_cache.name
            pars = psys.particles
            par_count = len(pars)
            par_attrs = get_par_attrs(cache_name, cache_folder, frame_index)

            if par_attrs:
                # set location
                loc_name = cache.attribute_name[cache.LOCATION]
                loc_values = par_attrs[cache.LOCATION]
                pars.foreach_set(loc_name, loc_values)

                # set velocity
                vel_values = par_attrs.get(cache.VELOCITY, None)
                if not vel_values is None:
                    vel_name = cache.attribute_name[cache.VELOCITY]
                    pars.foreach_set(vel_name, vel_values)

            else:
                null_values = numpy.full(
                    par_count * 3,
                    -1000.0,
                    dtype=cache.VEC_TYPE
                )
                pars.foreach_set('location', null_values)
                pars.foreach_set('velocity', null_values)
                pars.foreach_set('angular_velocity', null_values)


def register():
    bpy.app.handlers.frame_change_post.append(frame_change_post_handler)
    bpy.app.handlers.render_init.append(render_init_handler)
    bpy.app.handlers.render_post.append(render_post_handler)


def unregister():
    bpy.app.handlers.render_init.remove(render_init_handler)
    bpy.app.handlers.render_post.remove(render_post_handler)
    bpy.app.handlers.frame_change_post.remove(frame_change_post_handler)
