import math
import struct
import os

import bpy
import numpy

from . import utils


def write_debug_data(file_path, data):
    bin_data = bytearray()
    values_count = len(data)
    for i in range(values_count):
        value = struct.pack('f', data[i])
        bin_data.extend(value)
    with open(file_path, 'wb') as file:
        file.write(bin_data)


def pack_tex_data(psys, name, prefix, index, clear_indexes, params, par_loc, exp=True):
    mode = getattr(psys.settings.mol, '{}link_{}_mode'.format(prefix, name))
    etex = None
    params[index] = []
    scene = bpy.context.scene
    cache_folder = bpy.path.abspath(scene.mol.cache_folder)
    if mode == 'TEXTURE':
        tex = bpy.data.textures.get(
            getattr(psys.settings.mol, '{}link_{}tex'.format(prefix, name), None)
        )
        if exp:
            etex = bpy.data.textures.get(
                getattr(psys.settings.mol, '{}link_e{}tex'.format(prefix, name), None)
            )
        else:
            exp = None
        if tex:
            for i in range(0, len(par_loc), 3):
                value = tex.evaluate((
                    par_loc[i],
                    par_loc[i + 1],
                    par_loc[i + 2]
                ))[-1]
                params[index].append(
                    value * getattr(psys.settings.mol, '{}link_{}tex_coeff'.format(prefix, name))
                )
            if psys.settings.mol.use_debug_par_attr:
                cache_file_name = '{}_{}link_{}.bin'.format(psys.point_cache.name, prefix, name)
                file_path = os.path.join(cache_folder, cache_file_name)
                write_debug_data(file_path, params[index])
            params[index + 1] = 1
            for clear_index in clear_indexes:
                params[clear_index] = 0
            same = getattr(psys.settings.mol, '{}link_{}_samevalue'.format(prefix, name), None)
            if same:
                params[index + 2] = params[index]
                params[index + 3] = 1
            if not etex:
                params[index + 2] = params[index]
                params[index + 3] = 1
            if etex and not same:
                params[index + 2] = []
                for i in range(0, len(par_loc), 3):
                    value = etex.evaluate((
                        par_loc[i],
                        par_loc[i + 1],
                        par_loc[i + 2]
                    ))[-1]
                    params[index + 2].append(
                        value * getattr(psys.settings.mol, '{}link_e{}tex_coeff'.format(prefix, name))
                    )
                params[index + 3] = 1
    else:
        params[index + 1] = 0
        if exp:
            params[index + 2] = []
            params[index + 3] = 0


def pack_data(context, initiate):
    psyslen = 0
    parnum = 0
    scene = context.scene
    for ob in bpy.data.objects:
        obj = utils.get_object(ob)

        for psys in obj.particle_systems:           
            if psys.settings.mol.matter != "-1":
                psys.settings.mol.density = float(psys.settings.mol.matter)
            if psys.settings.mol.active and len(psys.particles):
                parlen = len(psys.particles)
                par_loc = numpy.zeros(parlen * 3, dtype=numpy.float32)
                par_vel = numpy.zeros(parlen * 3, dtype=numpy.float32)
                par_size = numpy.zeros(parlen, dtype=numpy.float32)
                par_alive = []
                for par in psys.particles:
                    parnum += 1
                    if par.alive_state == "UNBORN":
                        par_alive.append(2)
                    if par.alive_state == "ALIVE":
                        par_alive.append(0)
                    if par.alive_state == "DEAD":
                        par_alive.append(3)

                psys.particles.foreach_get('location', par_loc)
                psys.particles.foreach_get('velocity', par_vel)

                if initiate:
                    par_mass = []

                    if psys.settings.mol.density_active:
                        for par in psys.particles:
                            par_mass.append(psys.settings.mol.density * (4 / 3 * math.pi * ((par.size / 2) ** 3)))
                    else:
                        for par in psys.particles:
                            par_mass.append(psys.settings.mass)

                    psyslen += 1
                    psys.particles.foreach_get('size', par_size)
                    if bpy.context.scene.mol.minsize > min(par_size):
                        bpy.context.scene.mol.minsize = min(par_size)

                    if psys.settings.mol.link_stiff_samevalue:
                        psys.settings.mol.link_estiff = psys.settings.mol.link_stiff
                        psys.settings.mol.link_estiffrand = psys.settings.mol.link_stiffrand
                    if psys.settings.mol.link_damp_samevalue:
                        psys.settings.mol.link_edamp = psys.settings.mol.link_damp
                        psys.settings.mol.link_edamprand = psys.settings.mol.link_damprand
                    if psys.settings.mol.link_broken_samevalue:
                        psys.settings.mol.link_ebroken = psys.settings.mol.link_broken
                        psys.settings.mol.link_ebrokenrand = psys.settings.mol.link_brokenrand

                    if psys.settings.mol.relink_stiff_samevalue:
                        psys.settings.mol.relink_estiff = psys.settings.mol.relink_stiff
                        psys.settings.mol.relink_estiffrand = psys.settings.mol.relink_stiffrand
                    if psys.settings.mol.relink_damp_samevalue:
                        psys.settings.mol.relink_edamp = psys.settings.mol.relink_damp
                        psys.settings.mol.relink_edamprand = psys.settings.mol.relink_damprand
                    if psys.settings.mol.relink_broken_samevalue:
                        psys.settings.mol.relink_ebroken = psys.settings.mol.relink_broken
                        psys.settings.mol.relink_ebrokenrand = psys.settings.mol.relink_brokenrand

                    params = [0] * 84

                    params[0] = psys.settings.mol.selfcollision_active
                    params[1] = psys.settings.mol.othercollision_active
                    params[2] = psys.settings.mol.collision_group
                    params[3] = psys.settings.mol.friction
                    params[4] = psys.settings.mol.collision_damp
                    params[5] = psys.settings.mol.links_active

                    if psys.settings.mol.link_rellength:
                        params[6] = psys.settings.particle_size * psys.settings.mol.link_length
                    else:
                        params[6] = psys.settings.mol.link_length

                    params[7] = psys.settings.mol.link_max
                    params[8] = psys.settings.mol.link_tension
                    if psys.settings.mol.link_tension_mode == 'RANDOM':
                        params[9] = psys.settings.mol.link_tensionrand
                    else:
                        params[9] = 0.0
                    params[10] = psys.settings.mol.link_stiff
                    if psys.settings.mol.link_stiff_mode == 'RANDOM':
                        params[11] = psys.settings.mol.link_stiffrand
                        params[18] = psys.settings.mol.link_estiffrand
                    else:
                        params[11] = 0.0
                        params[18] = 0.0
                    params[12] = 1.0    # mol_link_stiffexp
                    params[13] = psys.settings.mol.link_damp
                    if psys.settings.mol.link_damp_mode == 'RANDOM':
                        params[14] = psys.settings.mol.link_damprand
                        params[21] = psys.settings.mol.link_edamprand
                    else:
                        params[14] = 0.0
                        params[21] = 0.0
                    params[15] = psys.settings.mol.link_broken
                    if psys.settings.mol.link_broken_mode == 'RANDOM':
                        params[16] = psys.settings.mol.link_brokenrand
                        params[23] = psys.settings.mol.link_ebrokenrand
                    else:
                        params[16] = 0.0
                        params[23] = 0.0
                    params[17] = psys.settings.mol.link_estiff
                    params[19] = 1.0    # mol_link_estiffexp
                    params[20] = psys.settings.mol.link_edamp
                    params[22] = psys.settings.mol.link_ebroken
                    params[24] = psys.settings.mol.relink_group
                    params[25] = psys.settings.mol.relink_chance
                    if psys.settings.mol.relink_chance_mode == 'RANDOM':
                        params[26] = psys.settings.mol.relink_chancerand
                    else:
                        params[26] = 0.0
                    params[27] = psys.settings.mol.relink_max
                    params[28] = psys.settings.mol.relink_tension
                    if psys.settings.mol.relink_tension_mode == 'RANDOM':
                        params[29] = psys.settings.mol.relink_tensionrand
                    else:
                        params[29] = 0.0
                    params[30] = psys.settings.mol.relink_stiff
                    params[31] = 1.0    # mol_relink_stiffexp
                    if psys.settings.mol.relink_stiff_mode == 'RANDOM':
                        params[32] = psys.settings.mol.relink_stiffrand
                        params[39] = psys.settings.mol.relink_estiffrand
                    else:
                        params[32] = 0.0
                        params[39] = 0.0
                    params[33] = psys.settings.mol.relink_damp
                    if psys.settings.mol.relink_damp_mode == 'RANDOM':
                        params[34] = psys.settings.mol.relink_damprand
                        params[41] = psys.settings.mol.relink_edamprand
                    else:
                        params[34] = 0.0
                        params[41] = 0.0
                    params[35] = psys.settings.mol.relink_broken
                    if psys.settings.mol.relink_broken_mode == 'RANDOM':
                        params[36] = psys.settings.mol.relink_brokenrand
                        params[43] = psys.settings.mol.relink_ebrokenrand
                    else:
                        params[36] = 0.0
                        params[43] = 0.0
                    params[37] = psys.settings.mol.relink_estiff
                    params[38] = 1.0    # mol_relink_estiffexp
                    params[40] = psys.settings.mol.relink_edamp
                    params[42] = psys.settings.mol.relink_ebroken
                    params[44] = psys.settings.mol.link_friction
                    params[45] = psys.settings.mol.link_group
                    params[46] = psys.settings.mol.other_link_active
                    if psys.settings.mol.link_friction_mode == 'RANDOM':
                        params[47] = psys.settings.mol.link_frictionrand
                    else:
                        params[47] = 0.0

                    # pack textures
                    index = 48
                    pack_tex_data(psys, 'tension', '', index, (9, ), params, par_loc, exp=False)
                    index += 2
                    pack_tex_data(psys, 'stiff', '', index, (11, 18), params, par_loc)
                    index += 4
                    pack_tex_data(psys, 'damp', '', index, (14, 21), params, par_loc)
                    index += 4
                    pack_tex_data(psys, 'broken', '', index, (16, 23), params, par_loc)
                    index += 4

                    pack_tex_data(psys, 'tension', 're', index, (29, ), params, par_loc, exp=False)
                    index += 2
                    pack_tex_data(psys, 'stiff', 're', index, (32, 39), params, par_loc)
                    index += 4
                    pack_tex_data(psys, 'damp', 're', index, (34, 41), params, par_loc)
                    index += 4
                    pack_tex_data(psys, 'broken', 're', index, (36, 43), params, par_loc)
                    index += 4

                    pack_tex_data(psys, 'friction', '', index, (), params, par_loc, exp=False)
                    index += 2
                    pack_tex_data(psys, 'friction', 're', index, (), params, par_loc, exp=False)
                    index += 2
                    pack_tex_data(psys, 'chance', 're', index, (), params, par_loc, exp=False)
                    index += 2

                mol_exportdata = bpy.context.scene.mol.exportdata

                if initiate:
                    mol_exportdata[0][2] = psyslen
                    mol_exportdata[0][3] = parnum
                    mol_exportdata.append((
                        parlen,
                        par_loc,
                        par_vel,
                        par_size,
                        par_mass,
                        par_alive,
                        params
                    ))

                else:
                    mol_exportdata.append((par_loc, par_vel, par_alive))
