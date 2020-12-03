cpdef init(importdata):
    #PROFILER_START
    global fps
    global substep
    global deltatime
    global cpunum
    global newlinks
    global totallinks
    global totaldeadlinks
    global deadlinks
    global parnum
    global psysnum
    global kdtree
    global parlist
    global parlistcopy
    global psys
    global par_id_list

    cdef int i = 0
    cdef int ii = 0
    cdef int profiling = 0
    newlinks = 0
    totallinks = 0
    totaldeadlinks = 0
    fps = float(importdata[0][0])
    substep = int(importdata[0][1])
    deltatime = (fps * (substep + 1))
    psysnum = importdata[0][2]
    parnum = importdata[0][3]
    cpunum = importdata[0][4]
    deadlinks = <int *>malloc(cpunum * cython.sizeof(int))
    print("  Number of cpu's used:", cpunum)
    psys = <ParSys *>malloc(psysnum * cython.sizeof(ParSys))
    parlist = <Particle *>malloc(parnum * cython.sizeof(Particle))
    par_id_list = <int *>malloc(parnum * cython.sizeof(int))
    parlistcopy = <SParticle *>malloc(parnum * cython.sizeof(SParticle))
    cdef int jj = 0
    cdef int index = 0

    for i in xrange(psysnum):
        psys[i].id = i
        psys[i].parnum = importdata[i + 1][0]
        psys[i].particles = <Particle *>malloc(psys[i].parnum * cython.sizeof(Particle))
        psys[i].particles = &parlist[jj]

        ########################################################################
        ######################## TEXTURES VALUES START #########################
        ########################################################################

        index = 48
        # link tension
        psys[i].use_link_tension_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_link_tension_tex:
            psys[i].link_tension_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].link_tension_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # link stiffness
        psys[i].use_link_stiff_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_link_stiff_tex:
            psys[i].link_stiff_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].link_stiff_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # link expansion stiffness
        psys[i].use_link_estiff_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_link_estiff_tex:
            psys[i].link_estiff_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].link_estiff_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # link damping
        psys[i].use_link_damp_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_link_damp_tex:
            psys[i].link_damp_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].link_damp_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # link expansion damping
        psys[i].use_link_edamp_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_link_edamp_tex:
            psys[i].link_edamp_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].link_edamp_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # link broken
        psys[i].use_link_broken_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_link_broken_tex:
            psys[i].link_broken_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].link_broken_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # link expansion broken
        psys[i].use_link_ebroken_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_link_ebroken_tex:
            psys[i].link_ebroken_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].link_ebroken_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # relink tension
        psys[i].use_relink_tension_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_relink_tension_tex:
            psys[i].relink_tension_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].relink_tension_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # relink stiffness
        psys[i].use_relink_stiff_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_relink_stiff_tex:
            psys[i].relink_stiff_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].relink_stiff_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # relink expansion stiffness
        psys[i].use_relink_estiff_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_relink_estiff_tex:
            psys[i].relink_estiff_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].relink_estiff_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # relink damping
        psys[i].use_relink_damp_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_relink_damp_tex:
            psys[i].relink_damp_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].relink_damp_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # relink expansion damping
        psys[i].use_relink_edamp_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_relink_edamp_tex:
            psys[i].relink_edamp_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].relink_edamp_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # relink broken
        psys[i].use_relink_broken_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_relink_broken_tex:
            psys[i].relink_broken_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].relink_broken_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # relink expansion broken
        psys[i].use_relink_ebroken_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_relink_ebroken_tex:
            psys[i].relink_ebroken_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].relink_ebroken_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # link friction
        psys[i].use_link_friction_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_link_friction_tex:
            psys[i].link_friction_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].link_friction_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # relink friction
        psys[i].use_relink_friction_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_relink_friction_tex:
            psys[i].relink_friction_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].relink_friction_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        # relink tension
        psys[i].use_relink_chance_tex = importdata[i + 1][6][index + 1]
        if psys[i].use_relink_chance_tex:
            psys[i].relink_chance_tex = <float *>malloc(psys[i].parnum * cython.sizeof(float))
            for ii in xrange(psys[i].parnum):
                psys[i].relink_chance_tex[ii] = importdata[i + 1][6][index][ii]
        index += 2

        ########################################################################
        ######################### TEXTURES VALUES END ##########################
        ########################################################################

        psys[i].selfcollision_active = importdata[i + 1][6][0]
        psys[i].othercollision_active = importdata[i + 1][6][1]
        psys[i].collision_group = importdata[i + 1][6][2]
        psys[i].friction = importdata[i + 1][6][3]
        psys[i].collision_damp = importdata[i + 1][6][4]
        psys[i].links_active = importdata[i + 1][6][5]
        psys[i].link_length = importdata[i + 1][6][6]
        psys[i].link_max = importdata[i + 1][6][7]
        psys[i].link_tension = importdata[i + 1][6][8]
        psys[i].link_tensionrand = importdata[i + 1][6][9]
        psys[i].link_stiff = importdata[i + 1][6][10] * 0.5
        psys[i].link_stiffrand = importdata[i + 1][6][11]
        psys[i].link_stiffexp = importdata[i + 1][6][12]
        psys[i].link_damp = importdata[i + 1][6][13]
        psys[i].link_damprand = importdata[i + 1][6][14]
        psys[i].link_broken = importdata[i + 1][6][15]
        psys[i].link_brokenrand = importdata[i + 1][6][16]
        psys[i].link_estiff = importdata[i + 1][6][17] * 0.5
        psys[i].link_estiffrand = importdata[i + 1][6][18]
        psys[i].link_estiffexp = importdata[i + 1][6][19]
        psys[i].link_edamp = importdata[i + 1][6][20]
        psys[i].link_edamprand = importdata[i + 1][6][21]
        psys[i].link_ebroken = importdata[i + 1][6][22]
        psys[i].link_ebrokenrand = importdata[i + 1][6][23]
        psys[i].relink_group = importdata[i + 1][6][24]
        psys[i].relink_chance = importdata[i + 1][6][25]
        psys[i].relink_chancerand = importdata[i + 1][6][26]
        psys[i].relink_max = importdata[i + 1][6][27]
        psys[i].relink_tension = importdata[i + 1][6][28]
        psys[i].relink_tensionrand = importdata[i + 1][6][29]
        psys[i].relink_stiff = importdata[i + 1][6][30] * 0.5
        psys[i].relink_stiffexp = importdata[i + 1][6][31]
        psys[i].relink_stiffrand = importdata[i + 1][6][32]
        psys[i].relink_damp = importdata[i + 1][6][33]
        psys[i].relink_damprand = importdata[i + 1][6][34]
        psys[i].relink_broken = importdata[i + 1][6][35]
        psys[i].relink_brokenrand = importdata[i + 1][6][36]
        psys[i].relink_estiff = importdata[i + 1][6][37] * 0.5
        psys[i].relink_estiffexp = importdata[i + 1][6][38]
        psys[i].relink_estiffrand = importdata[i + 1][6][39]
        psys[i].relink_edamp = importdata[i + 1][6][40]
        psys[i].relink_edamprand = importdata[i + 1][6][41]
        psys[i].relink_ebroken = importdata[i + 1][6][42]
        psys[i].relink_ebrokenrand = importdata[i + 1][6][43]
        psys[i].link_friction = importdata[i + 1][6][44]
        psys[i].link_group = importdata[i + 1][6][45]
        psys[i].other_link_active = importdata[i + 1][6][46]
        psys[i].link_frictionrand = importdata[i + 1][6][47]

        for ii in xrange(psys[i].parnum):
            parlist[jj].id = jj
            par_id_list[jj] = ii
            parlist[jj].loc[0] = importdata[i + 1][1][(ii * 3)]
            parlist[jj].loc[1] = importdata[i + 1][1][(ii * 3) + 1]
            parlist[jj].loc[2] = importdata[i + 1][1][(ii * 3) + 2]
            parlist[jj].vel[0] = importdata[i + 1][2][(ii * 3)]
            parlist[jj].vel[1] = importdata[i + 1][2][(ii * 3) + 1]
            parlist[jj].vel[2] = importdata[i + 1][2][(ii * 3) + 2]
            parlist[jj].size = importdata[i + 1][3][ii]
            parlist[jj].mass = importdata[i + 1][4][ii]
            parlist[jj].state = importdata[i + 1][5][ii]

            parlist[jj].sys = &psys[i]
            parlist[jj].collided_with = <int *>malloc(1 * cython.sizeof(int))
            parlist[jj].collided_num = 0
            parlist[jj].links = <Links *>malloc(1 * cython.sizeof(Links))
            parlist[jj].links_num = 0
            parlist[jj].links_activnum = 0
            parlist[jj].link_with = <int *>malloc(1 * cython.sizeof(int))
            parlist[jj].link_withnum = 0
            parlist[jj].neighboursmax = 10
            parlist[jj].neighbours = <int *>malloc(parlist[jj].neighboursmax * cython.sizeof(int))
            parlist[jj].neighboursnum = 0
            jj += 1

    jj = 0
    kdtree = <KDTree *>malloc(1 * cython.sizeof(KDTree))
    KDTree_create_nodes(kdtree, parnum)

    with nogil:
        for i in prange(<int>parnum, schedule='dynamic', chunksize=10, num_threads=cpunum):
            parlistcopy[i].id = parlist[i].id
            parlistcopy[i].loc[0] = parlist[i].loc[0]
            parlistcopy[i].loc[1] = parlist[i].loc[1]
            parlistcopy[i].loc[2] = parlist[i].loc[2]

    KDTree_create_tree(kdtree, parlistcopy, 0, parnum - 1, 0, -1, 0, 1)

    with nogil:
        for i in prange(kdtree.thread_index, schedule='dynamic', chunksize=10, num_threads=cpunum):
            KDTree_create_tree(kdtree, parlistcopy, kdtree.thread_start[i], kdtree.thread_end[i], kdtree.thread_name[i], kdtree.thread_parent[i], kdtree.thread_depth[i], 0)

    with nogil:
        for i in prange(<int>parnum, schedule='dynamic', chunksize=10, num_threads=cpunum):
            if parlist[i].sys.links_active == 1:
                KDTree_rnn_query(kdtree, &parlist[i], parlist[i].loc, parlist[i].sys.link_length)

    for i in xrange(parnum):
        create_link(parlist[i].id, parlist[i].sys.link_max, 1)
        if parlist[i].neighboursnum > 1:
            # free(parlist[i].neighbours)
            parlist[i].neighboursnum = 0

    totallinks += newlinks
    print("  New links created: ", newlinks)
    #PROFILER_END
    return parnum
