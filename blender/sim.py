import math
import struct
import os

import bpy

from . import utils


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
                par_loc = [0.0, ] * (parlen * 3)
                par_vel = [0.0, ] * (parlen * 3)
                par_size = [0.0, ] * parlen
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

                    params = [0] * 48

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
                    params[9] = psys.settings.mol.link_tensionrand
                    params[10] = psys.settings.mol.link_stiff
                    params[11] = psys.settings.mol.link_stiffrand
                    params[18] = psys.settings.mol.link_estiffrand
                    params[12] = 1.0    # mol_link_stiffexp
                    params[13] = psys.settings.mol.link_damp
                    params[14] = psys.settings.mol.link_damprand
                    params[21] = psys.settings.mol.link_edamprand
                    params[15] = psys.settings.mol.link_broken
                    params[16] = psys.settings.mol.link_brokenrand
                    params[23] = psys.settings.mol.link_ebrokenrand
                    params[17] = psys.settings.mol.link_estiff
                    params[19] = 1.0    # mol_link_estiffexp
                    params[20] = psys.settings.mol.link_edamp
                    params[22] = psys.settings.mol.link_ebroken
                    params[24] = psys.settings.mol.relink_group
                    params[25] = psys.settings.mol.relink_chance
                    params[26] = psys.settings.mol.relink_chancerand
                    params[27] = psys.settings.mol.relink_max
                    params[28] = psys.settings.mol.relink_tension
                    params[29] = psys.settings.mol.relink_tensionrand
                    params[30] = psys.settings.mol.relink_stiff
                    params[31] = 1.0    # mol_relink_stiffexp
                    params[32] = psys.settings.mol.relink_stiffrand
                    params[39] = psys.settings.mol.relink_estiffrand
                    params[33] = psys.settings.mol.relink_damp
                    params[34] = psys.settings.mol.relink_damprand
                    params[41] = psys.settings.mol.relink_edamprand
                    params[35] = psys.settings.mol.relink_broken
                    params[36] = psys.settings.mol.relink_brokenrand
                    params[43] = psys.settings.mol.relink_ebrokenrand
                    params[37] = psys.settings.mol.relink_estiff
                    params[38] = 1.0    # mol_relink_estiffexp
                    params[40] = psys.settings.mol.relink_edamp
                    params[42] = psys.settings.mol.relink_ebroken
                    params[44] = psys.settings.mol.link_friction
                    params[45] = psys.settings.mol.link_group
                    params[46] = psys.settings.mol.other_link_active
                    params[47] = psys.settings.mol.link_frictionrand

                    for index, param in enumerate(params):
                        if type(param) == bool:
                            params[index] = int(param)

                mol_exportdata = bpy.context.scene.mol.exportdata

                if initiate:
                    mol_exportdata[0][2] = psyslen
                    mol_exportdata[0][3] = parnum
                    mol_exportdata.append([
                        parlen,
                        par_loc,
                        par_vel,
                        par_size,
                        par_mass,
                        par_alive,
                        params
                    ])

                else:
                    mol_exportdata.append([par_loc, par_vel, par_alive])
