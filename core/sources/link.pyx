cdef float RANDOM_MAX = 32767.0


cdef float randomize_value(float value, float random)nogil:
    return value * (1.0 + ((rand() / RANDOM_MAX) * random) - (random / 2))


cdef float average_value(float value_1, float value_2)nogil:
    return (value_1 + value_2) / 2


cdef void create_link(int par_id, int max_link, int init, int parothers_id=-1)nogil:
    #PROFILER_START_NOGIL
    global deltatime
    global newlinks
    global parlist
    global par_id_list

    cdef Links *link = <Links *>malloc(1 * cython.sizeof(Links))
    cdef int *neighbours = NULL
    cdef int ii = 0
    cdef int neighboursnum = 0
    cdef Particle *par = NULL
    cdef Particle *par2 = NULL
    cdef Particle *fakepar = NULL
    cdef int create_links
    fakepar = <Particle *>malloc(1 * cython.sizeof(Particle))
    par = &parlist[par_id]
    cdef int p_id
    # link params
    cdef float link_friction_1 = 0.0
    cdef float link_friction_2 = 0.0
    cdef float link_tension_1 = 0.0
    cdef float link_tension_2 = 0.0
    cdef float link_stiff_1 = 0.0
    cdef float link_stiff_2 = 0.0
    cdef float link_estiff_1 = 0.0
    cdef float link_estiff_2 = 0.0
    cdef float link_damp_1 = 0.0
    cdef float link_damp_2 = 0.0
    cdef float link_edamp_1 = 0.0
    cdef float link_edamp_2 = 0.0
    cdef float link_broken_1 = 0.0
    cdef float link_broken_2 = 0.0
    cdef float link_ebroken_1 = 0.0
    cdef float link_ebroken_2 = 0.0
    # relink params
    cdef float relink_chance_1 = 0.0
    cdef float relink_chance_2 = 0.0
    cdef float relink_random = 0.0
    cdef float relink_friction_1 = 0.0
    cdef float relink_friction_2 = 0.0
    cdef float relink_tension_1 = 0.0
    cdef float relink_tension_2 = 0.0
    cdef float relink_stiff_1 = 0.0
    cdef float relink_stiff_2 = 0.0
    cdef float relink_estiff_1 = 0.0
    cdef float relink_estiff_2 = 0.0
    cdef float relink_damp_1 = 0.0
    cdef float relink_damp_2 = 0.0
    cdef float relink_edamp_1 = 0.0
    cdef float relink_edamp_2 = 0.0
    cdef float relink_broken_1 = 0.0
    cdef float relink_broken_2 = 0.0
    cdef float relink_ebroken_1 = 0.0
    cdef float relink_ebroken_2 = 0.0

    if par.state >= 2:
        return
    if par.links_activnum >= max_link:
        return
    if par.sys.links_active == 0:
        return

    if parothers_id == -1:
        # KDTree_rnn_query(kdtree, &fakepar[0], par.loc, par.sys.link_length)
        # neighbours = fakepar[0].neighbours
        neighbours = par.neighbours
        neighboursnum = par.neighboursnum
    else:
        neighbours = <int *>malloc(1 * cython.sizeof(int))
        neighbours[0] = parothers_id
        neighboursnum = 1

    link.start = par.id
    p_id = par_id_list[par.id]

    # link friction
    if par.sys.use_link_friction_tex:
        link_friction_1 = par.sys.link_friction_tex[p_id]
    else:
        link_friction_1 = randomize_value(par.sys.link_friction, par.sys.link_frictionrand)

    # link tension
    if par.sys.use_link_tension_tex:
        link_tension_1 = par.sys.link_tension_tex[p_id]
    else:
        link_tension_1 = randomize_value(par.sys.link_tension, par.sys.link_tensionrand)

    # link stiffness
    if par.sys.use_link_stiff_tex:
        link_stiff_1 = par.sys.link_stiff_tex[p_id]
    else:
        link_stiff_1 = randomize_value(par.sys.link_stiff, par.sys.link_stiffrand)

    # link estiffness
    if par.sys.use_link_estiff_tex:
        link_estiff_1 = par.sys.link_estiff_tex[p_id]
    else:
        link_estiff_1 = randomize_value(par.sys.link_estiff, par.sys.link_estiffrand)

    # link damping
    if par.sys.use_link_damp_tex:
        link_damp_1 = par.sys.link_damp_tex[p_id]
    else:
        link_damp_1 = randomize_value(par.sys.link_damp, par.sys.link_damprand)

    # link edamping
    if par.sys.use_link_edamp_tex:
        link_edamp_1 = par.sys.link_edamp_tex[p_id]
    else:
        link_edamp_1 = randomize_value(par.sys.link_edamp, par.sys.link_edamprand)

    # link broken
    if par.sys.use_link_broken_tex:
        link_broken_1 = par.sys.link_broken_tex[p_id]
    else:
        link_broken_1 = randomize_value(par.sys.link_broken, par.sys.link_brokenrand)

    # link ebroken
    if par.sys.use_link_ebroken_tex:
        link_ebroken_1 = par.sys.link_ebroken_tex[p_id]
    else:
        link_ebroken_1 = randomize_value(par.sys.link_ebroken, par.sys.link_ebrokenrand)

    # relink chance
    if par.sys.use_relink_chance_tex:
        relink_chance_1 = par.sys.relink_chance_tex[p_id]
    else:
        relink_chance_1 = randomize_value(par.sys.relink_chance, par.sys.relink_chancerand)

    # relink tension
    if par.sys.use_relink_tension_tex:
        relink_tension_1 = par.sys.relink_tension_tex[p_id]
    else:
        relink_tension_1 = randomize_value(par.sys.relink_tension, par.sys.relink_tensionrand)

    # relink stiffness
    if par.sys.use_relink_stiff_tex:
        relink_stiff_1 = par.sys.relink_stiff_tex[p_id]
    else:
        relink_stiff_1 = randomize_value(par.sys.relink_stiff, par.sys.relink_stiffrand)

    # relink estiffness
    if par.sys.use_relink_estiff_tex:
        relink_estiff_1 = par.sys.relink_estiff_tex[p_id]
    else:
        relink_estiff_1 = randomize_value(par.sys.relink_estiff, par.sys.relink_estiffrand)

    # relink damping
    if par.sys.use_relink_damp_tex:
        relink_damp_1 = par.sys.relink_damp_tex[p_id]
    else:
        relink_damp_1 = randomize_value(par.sys.relink_damp, par.sys.relink_damprand)

    # relink edamping
    if par.sys.use_relink_edamp_tex:
        relink_edamp_1 = par.sys.relink_edamp_tex[p_id]
    else:
        relink_edamp_1 = randomize_value(par.sys.relink_edamp, par.sys.relink_edamprand)

    # relink broken
    if par.sys.use_relink_broken_tex:
        relink_broken_1 = par.sys.relink_broken_tex[p_id]
    else:
        relink_broken_1 = randomize_value(par.sys.relink_broken, par.sys.relink_brokenrand)

    # relink ebroken
    if par.sys.use_relink_ebroken_tex:
        relink_ebroken_1 = par.sys.relink_ebroken_tex[p_id]
    else:
        relink_ebroken_1 = randomize_value(par.sys.relink_ebroken, par.sys.relink_ebrokenrand)

    for ii in xrange(neighboursnum):
        if par.links_activnum >= max_link:
            break
        if parothers_id == -1:
            par2 = &parlist[neighbours[ii]]
        else:
            par2 = &parlist[neighbours[0]]
        if par.id != par2.id:
            # arraysearch(par2.id, par.link_with, par.link_withnum)

            if arraysearch(par.id,par2.link_with,par2.link_withnum) == -1 and par2.state <= 1 and par.state <= 1:

            #if par not in par2.link_with and par2.state <= 1 \
            #   and par.state <= 1:

                link.end = par2.id

                # link friction
                if par2.sys.use_link_friction_tex:
                    link_friction_2 = par2.sys.link_friction_tex[p_id]
                else:
                    link_friction_2 = randomize_value(par2.sys.link_friction, par2.sys.link_frictionrand)

                link.friction = average_value(link_friction_1, link_friction_2)

                if parothers_id == -1 and par.sys.link_group == par2.sys.link_group:
                    if par.sys.id != par2.sys.id:
                        if par.sys.other_link_active and par2.sys.other_link_active:
                            create_links = 1
                        else:
                            create_links = 0
                    else:
                        create_links = 1

                    if create_links == 1:

                        # link tension
                        if par2.sys.use_link_tension_tex:
                            link_tension_2 = par2.sys.link_tension_tex[p_id]
                        else:
                            link_tension_2 = randomize_value(par2.sys.link_tension, par2.sys.link_tensionrand)

                        tension = average_value(link_tension_1, link_tension_2)

                        # link length
                        link.lenght = ((square_dist(par.loc, par2.loc, 3)) ** 0.5) * tension

                        # link stiffness
                        if par2.sys.use_link_stiff_tex:
                            link_link_stiff_2 = par2.sys.link_stiff_tex[p_id]
                        else:
                            link_link_stiff_2 = randomize_value(par2.sys.link_stiff, par2.sys.link_stiffrand)

                        link.stiffness = average_value(link_stiff_1, link_stiff_2)

                        # link estiffness
                        if par2.sys.use_link_estiff_tex:
                            link_estiff_2 = par2.sys.link_estiff_tex[p_id]
                        else:
                            link_estiff_2 = randomize_value(par2.sys.link_estiff, par2.sys.link_estiffrand)

                        link.estiffness = average_value(link_estiff_1, link_estiff_2)

                        # link exponent
                        link.exponent = abs(int((par.sys.link_stiffexp + par2.sys.link_stiffexp) / 2))
                        link.eexponent = abs(int((par.sys.link_estiffexp + par2.sys.link_estiffexp) / 2))

                        # link damping
                        if par2.sys.use_link_damp_tex:
                            link_damp_2 = par2.sys.link_damp_tex[p_id]
                        else:
                            link_damp_2 = randomize_value(par2.sys.link_damp, par2.sys.link_damprand)

                        link.damping = average_value(link_damp_1, link_damp_2)

                        # link edamping
                        if par2.sys.use_link_edamp_tex:
                            link_edamp_2 = par2.sys.link_edamp_tex[p_id]
                        else:
                            link_edamp_2 = randomize_value(par2.sys.link_edamp, par2.sys.link_edamprand)

                        link.edamping = average_value(link_edamp_1, link_edamp_2)

                        # link broken
                        if par2.sys.use_link_broken_tex:
                            link_broken_2 = par2.sys.link_broken_tex[p_id]
                        else:
                            link_broken_2 = randomize_value(par2.sys.link_broken, par2.sys.link_brokenrand)

                        link.broken = average_value(link_broken_1, link_broken_2)

                        # link ebroken
                        if par2.sys.use_link_ebroken_tex:
                            link_ebroken_2 = par2.sys.link_ebroken_tex[p_id]
                        else:
                            link_ebroken_2 = randomize_value(par2.sys.link_ebroken, par2.sys.link_ebrokenrand)

                        link.ebroken = average_value(link_ebroken_1, link_ebroken_2)

                        par.links[par.links_num] = link[0]
                        par.links_num += 1
                        par.links_activnum += 1
                        par.links = <Links *>realloc(par.links,(par.links_num + 2) * cython.sizeof(Links))

                        par.link_with[par.link_withnum] = par2.id
                        par.link_withnum += 1

                        par.link_with = <int *>realloc(par.link_with,(par.link_withnum + 2) * cython.sizeof(int))

                        par2.link_with[par2.link_withnum] = par.id
                        par2.link_withnum += 1

                        par2.link_with = <int *>realloc(par2.link_with,(par2.link_withnum + 2) * cython.sizeof(int))
                        newlinks += 1
                        # free(link)

                if parothers_id != -1 and par.sys.relink_group == par2.sys.relink_group:

                    # relink chance
                    if par2.sys.use_relink_chance_tex:
                        relink_chance_2 = par2.sys.relink_chance_tex[p_id]
                    else:
                        relink_chance_2 = randomize_value(par2.sys.relink_chance, par2.sys.relink_chancerand)

                    relink_random = rand() / RANDOM_MAX

                    if relink_random <= average_value(relink_chance_1, relink_chance_2):

                        # relink tension
                        if par2.sys.use_relink_tension_tex:
                            relink_tension_2 = par2.sys.relink_tension_tex[p_id]
                        else:
                            relink_tension_2 = randomize_value(par2.sys.relink_tension, par2.sys.relink_tensionrand)

                        tension = average_value(relink_tension_1, relink_tension_2)

                        # relink length
                        link.lenght = ((square_dist(par.loc, par2.loc, 3)) ** 0.5) * tension

                        # relink stiffness
                        if par2.sys.use_relink_stiff_tex:
                            relink_stiff_2 = par2.sys.relink_stiff_tex[p_id]
                        else:
                            relink_stiff_2 = randomize_value(par2.sys.relink_stiff, par2.sys.relink_stiffrand)

                        # relink estiffness
                        if par2.sys.use_relink_estiff_tex:
                            relink_estiff_2 = par2.sys.relink_estiff_tex[p_id]
                        else:
                            relink_estiff_2 = randomize_value(par2.sys.relink_estiff, par2.sys.relink_estiffrand)

                        link.stiffness = average_value(relink_stiff_1, relink_stiff_2)
                        link.estiffness = average_value(relink_estiff_1, relink_estiff_2)

                        # relink exponent
                        link.exponent = abs(int((par.sys.relink_stiffexp + par2.sys.relink_stiffexp) / 2))
                        link.eexponent = abs(int((par.sys.relink_estiffexp + par2.sys.relink_estiffexp) / 2))

                        # relink damping
                        if par2.sys.use_relink_damp_tex:
                            relink_damp_2 = par2.sys.relink_damp_tex[p_id]
                        else:
                            relink_damp_2 = randomize_value(par2.sys.relink_damp, par2.sys.relink_damprand)

                        # relink edamping
                        if par2.sys.use_relink_edamp_tex:
                            relink_edamp_2 = par2.sys.relink_edamp_tex[p_id]
                        else:
                            relink_edamp_2 = randomize_value(par2.sys.relink_edamp, par2.sys.relink_edamprand)

                        link.damping = average_value(relink_damp_1, relink_damp_2)
                        link.edamping = average_value(relink_edamp_1, relink_edamp_2)

                        # relink broken
                        if par2.sys.use_relink_broken_tex:
                            relink_broken_2 = par2.sys.relink_broken_tex[p_id]
                        else:
                            relink_broken_2 = randomize_value(par2.sys.relink_broken, par2.sys.relink_brokenrand)

                        # relink ebroken
                        if par2.sys.use_relink_ebroken_tex:
                            relink_ebroken_2 = par2.sys.relink_ebroken_tex[p_id]
                        else:
                            relink_ebroken_2 = randomize_value(par2.sys.relink_ebroken, par2.sys.relink_ebrokenrand)

                        link.broken = average_value(relink_broken_1, relink_broken_2)
                        link.ebroken = average_value(relink_ebroken_1, relink_ebroken_2)

                        par.links[par.links_num] = link[0]
                        par.links_num += 1
                        par.links_activnum += 1
                        par.links = <Links *>realloc(par.links,(par.links_num + 1) * cython.sizeof(Links))
                        par.link_with[par.link_withnum] = par2.id
                        par.link_withnum += 1
                        par.link_with = <int *>realloc(par.link_with,(par.link_withnum + 1) * cython.sizeof(int))
                        par2.link_with[par2.link_withnum] = par.id
                        par2.link_withnum += 1
                        par2.link_with = <int *>realloc(par2.link_with,(par2.link_withnum + 1) * cython.sizeof(int))
                        newlinks += 1
                        # free(link)

    # free(neighbours)
    free(fakepar)
    free(link)
    # free(par)
    # free(par2)
    #PROFILER_END_NOGIL


cdef void solve_link(Particle *par)nogil:
    #PROFILER_START_NOGIL
    global deltatime
    global newlinks
    global deadlinks
    global parlist

    cdef int i = 0
    cdef float stiff = 0
    cdef float damping = 0
    cdef float timestep = 0
    cdef float exp = 0
    cdef Particle *par1 = NULL
    cdef Particle *par2 = NULL
    cdef float *Loc1 = [0, 0, 0]
    cdef float *Loc2 = [0, 0, 0]
    cdef float *V1 = [0, 0, 0]
    cdef float *V2 = [0, 0, 0]
    cdef float LengthX = 0
    cdef float LengthY = 0
    cdef float LengthZ = 0
    cdef float Length = 0
    cdef float Vx = 0
    cdef float Vy = 0
    cdef float Vz = 0
    cdef float V = 0
    cdef float ForceSpring = 0
    cdef float ForceDamper = 0
    cdef float ForceX = 0
    cdef float ForceY = 0
    cdef float ForceZ = 0
    cdef float *Force1 = [0, 0, 0]
    cdef float *Force2 = [0, 0, 0]
    cdef float ratio1 = 0
    cdef float ratio2 = 0
    cdef int parsearch = 0
    cdef int par2search = 0
    cdef float *normal1 = [0, 0, 0]
    cdef float *normal2 = [0, 0, 0]
    cdef float factor1 = 0
    cdef float factor2 = 0
    cdef float friction1 = 0
    cdef float friction2 = 0
    cdef float *ypar1_vel = [0, 0, 0]
    cdef float *xpar1_vel = [0, 0, 0]
    cdef float *ypar2_vel = [0, 0, 0]
    cdef float *xpar2_vel = [0, 0, 0]
    # broken_links = []
    if par.state >= 2:
        return
    for i in xrange(par.links_num):
        if par.links[i].start != -1:
            par1 = &parlist[par.links[i].start]
            par2 = &parlist[par.links[i].end]
            Loc1[0] = par1.loc[0]
            Loc1[1] = par1.loc[1]
            Loc1[2] = par1.loc[2]
            Loc2[0] = par2.loc[0]
            Loc2[1] = par2.loc[1]
            Loc2[2] = par2.loc[2]
            V1[0] = par1.vel[0]
            V1[1] = par1.vel[1]
            V1[2] = par1.vel[2]
            V2[0] = par2.vel[0]
            V2[1] = par2.vel[1]
            V2[2] = par2.vel[2]
            LengthX = Loc2[0] - Loc1[0]
            LengthY = Loc2[1] - Loc1[1]
            LengthZ = Loc2[2] - Loc1[2]
            Length = (LengthX ** 2 + LengthY ** 2 + LengthZ ** 2) ** (0.5)
            if par.links[i].lenght != Length and Length != 0:
                if par.links[i].lenght > Length:
                    stiff = par.links[i].stiffness * deltatime
                    damping = par.links[i].damping
                    exp = par.links[i].exponent
                if par.links[i].lenght < Length:
                    stiff = par.links[i].estiffness * deltatime
                    damping = par.links[i].edamping
                    exp = par.links[i].eexponent
                Vx = V2[0] - V1[0]
                Vy = V2[1] - V1[1]
                Vz = V2[2] - V1[2]
                V = (Vx * LengthX + Vy * LengthY + Vz * LengthZ) / Length
                ForceSpring = ((Length - par.links[i].lenght) ** (exp)) * stiff
                ForceDamper = damping * V
                ForceX = (ForceSpring + ForceDamper) * LengthX / Length
                ForceY = (ForceSpring + ForceDamper) * LengthY / Length
                ForceZ = (ForceSpring + ForceDamper) * LengthZ / Length
                Force1[0] = ForceX
                Force1[1] = ForceY
                Force1[2] = ForceZ
                Force2[0] = -ForceX
                Force2[1] = -ForceY
                Force2[2] = -ForceZ
                ratio1 = (par2.mass/(par1.mass + par2.mass))
                ratio2 = (par1.mass/(par1.mass + par2.mass))

                if par1.state == 3: #dead particle, correct velocity ratio of alive partner
                    ratio1 = 0
                    ratio2 = 1
                elif par2.state == 3:
                    ratio1 = 1
                    ratio2 = 0

                par1.vel[0] += Force1[0] * ratio1
                par1.vel[1] += Force1[1] * ratio1
                par1.vel[2] += Force1[2] * ratio1
                par2.vel[0] += Force2[0] * ratio2
                par2.vel[1] += Force2[1] * ratio2
                par2.vel[2] += Force2[2] * ratio2

                normal1[0] = LengthX / Length
                normal1[1] = LengthY / Length
                normal1[2] = LengthZ / Length
                normal2[0] = normal1[0] * -1
                normal2[1] = normal1[1] * -1
                normal2[2] = normal1[2] * -1

                factor1 = dot_product(par1.vel, normal1)

                ypar1_vel[0] = factor1 * normal1[0]
                ypar1_vel[1] = factor1 * normal1[1]
                ypar1_vel[2] = factor1 * normal1[2]
                xpar1_vel[0] = par1.vel[0] - ypar1_vel[0]
                xpar1_vel[1] = par1.vel[1] - ypar1_vel[1]
                xpar1_vel[2] = par1.vel[2] - ypar1_vel[2]

                factor2 = dot_product(par2.vel, normal2)

                ypar2_vel[0] = factor2 * normal2[0]
                ypar2_vel[1] = factor2 * normal2[1]
                ypar2_vel[2] = factor2 * normal2[2]
                xpar2_vel[0] = par2.vel[0] - ypar2_vel[0]
                xpar2_vel[1] = par2.vel[1] - ypar2_vel[1]
                xpar2_vel[2] = par2.vel[2] - ypar2_vel[2]

                friction1 = 1 - ((par.links[i].friction) * ratio1)
                friction2 = 1 - ((par.links[i].friction) * ratio2)

                par1.vel[0] = ypar1_vel[0] + ((xpar1_vel[0] * friction1) + (xpar2_vel[0] * ( 1 - friction1)))

                par1.vel[1] = ypar1_vel[1] + ((xpar1_vel[1] * friction1) + (xpar2_vel[1] * ( 1 - friction1)))

                par1.vel[2] = ypar1_vel[2] + ((xpar1_vel[2] * friction1) + (xpar2_vel[2] * ( 1 - friction1)))

                par2.vel[0] = ypar2_vel[0] + ((xpar2_vel[0] * friction2) + (xpar1_vel[0] * ( 1 - friction2)))

                par2.vel[1] = ypar2_vel[1] + ((xpar2_vel[1] * friction2) + (xpar1_vel[1] * ( 1 - friction2)))

                par2.vel[2] = ypar2_vel[2] + ((xpar2_vel[2] * friction2) + (xpar1_vel[2] * ( 1 - friction2)))

                if Length > (par.links[i].lenght * (1 + par.links[i].ebroken)) or Length < (par.links[i].lenght  * (1 - par.links[i].broken)):

                    par.links[i].start = -1
                    par.links_activnum -= 1
                    deadlinks[threadid()] += 1

                    parsearch = arraysearch(par2.id, par.link_with, par.link_withnum)

                    if parsearch != -1:
                        par.link_with[parsearch] = -1

                    par2search = arraysearch(par.id, par2.link_with, par2.link_withnum)

                    if par2search != -1:
                        par2.link_with[par2search] = -1

                    # broken_links.append(link)
                    # if par2 in par1.link_with:
                        # par1.link_with.remove(par2)
                    # if par1 in par2.link_with:
                        # par2.link_with.remove(par1)

    # par.links = list(set(par.links) - set(broken_links))
    # free(par1)
    # free(par2)
    #PROFILER_END_NOGIL
