import os
import struct

import bpy
import numpy

from . import utils
from . import cache


is_rendering = False


debug_attrs = {
    # link
    'LINK_FRICTION': 'link_friction',
    'LINK_TENSION': 'link_tension',
    'LINK_STIFFNESS': 'link_stiffness',
    'LINK_ESTIFFNESS': 'link_estiffness',
    'LINK_DAMPING': 'link_damping',
    'LINK_EDAMPING': 'link_edamping',
    'LINK_BROKEN': 'link_broken',
    'LINK_EBROKEN': 'link_ebroken',

    # relink
    'RELINK_FRICTION': 'relink_friction',
    'RELINK_TENSION': 'relink_tension',
    'RELINK_STIFFNESS': 'relink_stiffness',
    'RELINK_ESTIFFNESS': 'relink_estiffness',
    'RELINK_DAMPING': 'relink_damping',
    'RELINK_EDAMPING': 'relink_edamping',
    'RELINK_BROKEN': 'relink_broken',
    'RELINK_EBROKEN': 'relink_ebroken',
    'RELINK_LINKING': 'relink_chance'
}


def get_debug_values(file_path):
    # get particle debug values from debug file

    if not os.path.exists(file_path):
        return

    if not os.path.isfile(file_path):
        return

    with open(file_path, 'rb') as file:
        values = numpy.fromfile(file, dtype=numpy.float32)

    return values


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
def frame_change_pre_handler(scene):
    if not scene.mol_use_cache:
        return

    global is_rendering

    if is_rendering:
        return

    if scene.mol_simrun:
        return

    cache_folder = bpy.path.abspath(scene.mol_cache_folder)

    for obj in bpy.data.objects:
        obj = utils.get_object(bpy.context, obj)

        for psys in obj.particle_systems:

            if not psys.settings.mol_active:
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

                if not psys.settings.mol_use_debug_par_attr:
                    # set velocity
                    vel_values = par_attrs.get(cache.VELOCITY, None)
                    if not vel_values is None:
                        vel_name = cache.attribute_name[cache.VELOCITY]
                        pars.foreach_set(vel_name, vel_values)

                else:
                    attr_name = psys.settings.mol_debug_par_attr_name
                    attr = debug_attrs[attr_name]

                    debug_file_name = '{}_{}{}'.format(
                        psys.point_cache.name,
                        attr,
                        cache.EXT_HEAD
                    )

                    debug_file_path = os.path.join(
                        cache_folder,
                        debug_file_name
                    )

                    values = get_debug_values(debug_file_path)

                    if not values is None:
                        nulls = numpy.zeros(par_count, dtype=cache.VEC_TYPE)
                        vector_values = numpy.dstack(
                            [values, nulls, nulls]
                        )[0].ravel()
                        del values
                        del nulls

                    else:
                        vector_values = numpy.full(
                            par_count * 3,
                            0.0,
                            dtype=cache.VEC_TYPE
                        )

                    pars.foreach_set('velocity', vector_values)
                    pars.foreach_set('angular_velocity', vector_values)

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
    bpy.app.handlers.frame_change_post.append(frame_change_pre_handler)
    bpy.app.handlers.render_init.append(render_init_handler)
    bpy.app.handlers.render_post.append(render_post_handler)


def unregister():
    bpy.app.handlers.render_init.remove(render_init_handler)
    bpy.app.handlers.render_post.remove(render_post_handler)
    bpy.app.handlers.frame_change_post.remove(frame_change_pre_handler)
