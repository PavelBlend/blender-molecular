import math

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
                par_alive = [0, ] * parlen

                parnum = len(psys.particles)

                psys.particles.foreach_get('location', par_loc)
                psys.particles.foreach_get('velocity', par_vel)
                psys.particles.foreach_get('alive_state', par_alive)

                for index in range(parlen):

                    # alive
                    if par_alive[index] == 3:
                        par_alive[index] = 0

                    # dead
                    elif par_alive[index] == 1:
                        par_alive[index] = 3

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

                    params = []

                    # collision
                    params.append(psys.settings.mol.selfcollision_active)
                    params.append(psys.settings.mol.othercollision_active)
                    params.append(psys.settings.mol.collision_group)
                    params.append(psys.settings.mol.friction)
                    params.append(psys.settings.mol.collision_damp)

                    # links
                    params.append(psys.settings.mol.links_active)
                    params.append(psys.settings.mol.other_link_active)
                    params.append(psys.settings.mol.link_group)
                    params.append(psys.settings.mol.link_friction)
                    params.append(psys.settings.mol.link_frictionrand)
                    params.append(psys.settings.mol.link_max)

                    if psys.settings.mol.link_rellength:
                        params.append(psys.settings.particle_size * psys.settings.mol.link_length)
                    else:
                        params.append(psys.settings.mol.link_length)

                    # stiffness
                    params.append(psys.settings.mol.link_stiff)
                    params.append(psys.settings.mol.link_stiffrand)
                    params.append(psys.settings.mol.link_estiff)
                    params.append(psys.settings.mol.link_estiffrand)

                    # damping
                    params.append(psys.settings.mol.link_damp)
                    params.append(psys.settings.mol.link_damprand)
                    params.append(psys.settings.mol.link_edamp)
                    params.append(psys.settings.mol.link_edamprand)

                    # broken
                    params.append(psys.settings.mol.link_broken)
                    params.append(psys.settings.mol.link_brokenrand)
                    params.append(psys.settings.mol.link_ebroken)
                    params.append(psys.settings.mol.link_ebrokenrand)

                    # relink params
                    params.append(psys.settings.mol.relink_group)
                    params.append(psys.settings.mol.relink_chance)
                    params.append(psys.settings.mol.relink_chancerand)
                    params.append(psys.settings.mol.relink_max)

                    # stiffness
                    params.append(psys.settings.mol.relink_stiff)
                    params.append(psys.settings.mol.relink_stiffrand)
                    params.append(psys.settings.mol.relink_estiff)
                    params.append(psys.settings.mol.relink_estiffrand)

                    # damping
                    params.append(psys.settings.mol.relink_damp)
                    params.append(psys.settings.mol.relink_damprand)
                    params.append(psys.settings.mol.relink_edamp)
                    params.append(psys.settings.mol.relink_edamprand)

                    # broken
                    params.append(psys.settings.mol.relink_broken)
                    params.append(psys.settings.mol.relink_brokenrand)
                    params.append(psys.settings.mol.relink_ebroken)
                    params.append(psys.settings.mol.relink_ebrokenrand)

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
