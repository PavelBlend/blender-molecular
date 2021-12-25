cpdef simulate(importdata):
    #PROFILER_START
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

    cdef int i = 0
    cdef int ii = 0
    cdef int profiling = 1

    cdef float minX = INT_MAX
    cdef float minY = INT_MAX
    cdef float minZ = INT_MAX
    cdef float maxX = -INT_MAX
    cdef float maxY = -INT_MAX
    cdef float maxZ = -INT_MAX
    cdef float maxSize = -INT_MAX
    cdef Pool *parPool = <Pool *>malloc(1 * cython.sizeof(Pool))
    parPool.parity = <Parity *>malloc(2 * cython.sizeof(Parity))
    parPool[0].axis = -1
    parPool[0].offset = 0
    parPool[0].max = 0

    # cdef float *zeropoint = [0,0,0]
    newlinks = 0
    for i in xrange(cpunum):
        deadlinks[i] = 0
    if profiling == 1:
        print("-->start simulate")
        stime2 = clock()
        stime = clock()

    update(importdata)

    if profiling == 1:
        print("-->update time", clock() - stime, "sec")
        stime = clock()

    for i in xrange(parnum):
        parlistcopy[i].id = parlist[i].id
        parlistcopy[i].loc[0] = parlist[i].loc[0]
        # if parlist[i].loc[0] >= FLT_MAX or parlist[i].loc[0] <= -FLT_MAX :
            # print('ALERT! INF value in X')
        if parlist[i].loc[0] < minX:
            minX = parlist[i].loc[0]
        if parlist[i].loc[0] > maxX:
            maxX = parlist[i].loc[0]
        parlistcopy[i].loc[1] = parlist[i].loc[1]
        if parlist[i].loc[1] < minY:
            minY = parlist[i].loc[1]
        if parlist[i].loc[1] > maxY:
            maxY = parlist[i].loc[1]
        parlistcopy[i].loc[2] = parlist[i].loc[2]
        if parlist[i].loc[2] < minZ:
            minZ = parlist[i].loc[2]
        if parlist[i].loc[2] > maxZ:
            maxZ = parlist[i].loc[2]
        if parlist[i].sys.links_active == 1:
            if parlist[i].links_num > 0:
                for ii in xrange(parlist[i].links_num):
                    if parlist[i].links[ii].lenght > maxSize:
                        maxSize = parlist[i].links[ii].lenght
        if (parlist[i].size * 2) > maxSize:
            maxSize = (parlist[i].size * 2)

    if (maxX - minX) >= (maxY - minY) and (maxX - minX) >= (maxZ - minZ):
        parPool[0].axis = 0
        parPool[0].offset = 0 - minX
        parPool[0].max = maxX + parPool[0].offset

    if (maxY - minY) > (maxX - minX) and (maxY - minY) > (maxZ - minZ):
        parPool[0].axis = 1
        parPool[0].offset = 0 - minY
        parPool[0].max = maxY + parPool[0].offset

    if (maxZ - minZ) > (maxY - minY) and (maxZ - minZ) > (maxX - minX):
        parPool[0].axis = 2
        parPool[0].offset = 0 - minZ
        parPool[0].max = maxZ + parPool[0].offset       

    if (parPool[0].max / ( cpunum * 10 )) > maxSize:
        maxSize = (parPool[0].max / ( cpunum * 10 ))

    # cdef float Xsize = maxX - minX
    # cdef float Ysize = maxY - minY
    # cdef float Zsize = maxZ - minZ
    # cdef float newXsize = Xsize
    # cdef float newYsize = Ysize
    # cdef float newZsize = Zsize
    # pyaxis = []
    # for i in xrange(64):
    #     if Xsize >= Ysize and Xsize >= Zsize:
    #         kdtree.axis[i] = 0
    #         newXsize = Xsize / 2
    #     if Ysize > Xsize and Ysize > Zsize:
    #         kdtree.axis[i] = 1
    #         newYsize = Ysize / 2
    #     if Zsize > Xsize and Zsize > Ysize:
    #         kdtree.axis[i] = 2
    #         newZsize = Zsize / 2
    #         
    #     Xsize = newXsize
    #     Ysize = newYsize
    #     Zsize = newZsize
    #     pyaxis.append(kdtree.axis[i])

    cdef int pair
    cdef int heaps
    cdef float scale = 1 / ( maxSize * 2.1 )

    for pair in xrange(2):

        parPool[0].parity[pair].heap = <Heap *>malloc((<int>(parPool[0].max * scale) + 1) * cython.sizeof(Heap))

        for heaps in range(<int>(parPool[0].max * scale) + 1):
            parPool[0].parity[pair].heap[heaps].parnum = 0
            parPool[0].parity[pair].heap[heaps].maxalloc = 50

            parPool[0].parity[pair].heap[heaps].par = <int *>malloc(parPool[0].parity[pair].heap[heaps].maxalloc * cython.sizeof(int))

    for i in xrange(parnum):
        pair = <int>(((parlist[i].loc[parPool[0].axis] + parPool[0].offset) * scale) % 2)
        heaps = <int>((parlist[i].loc[parPool[0].axis] + parPool[0].offset) * scale)
        parPool[0].parity[pair].heap[heaps].parnum += 1

        if parPool[0].parity[pair].heap[heaps].parnum > parPool[0].parity[pair].heap[heaps].maxalloc:

            parPool[0].parity[pair].heap[heaps].maxalloc = <int>(parPool[0].parity[pair].heap[heaps].maxalloc * 1.25)

            parPool[0].parity[pair].heap[heaps].par = <int *>realloc(parPool[0].parity[pair].heap[heaps].par, (parPool[0].parity[pair].heap[heaps].maxalloc + 2 ) * cython.sizeof(int))

        parPool[0].parity[pair].heap[heaps].par[(parPool[0].parity[pair].heap[heaps].parnum - 1)] = parlist[i].id

    if profiling == 1:
        print("-->copy data time", clock() - stime, "sec")
        stime = clock()

    KDTree_create_tree(kdtree, parlistcopy, 0, parnum - 1, 0, -1, 0, 1)

    with nogil:
        for i in prange(kdtree.thread_index, schedule='dynamic', chunksize=10, num_threads=cpunum):
            KDTree_create_tree(kdtree, parlistcopy, kdtree.thread_start[i], kdtree.thread_end[i], kdtree.thread_name[i], kdtree.thread_parent[i], kdtree.thread_depth[i], 0)

    if profiling == 1:
        print("-->create tree time", clock() - stime,"sec")
        stime = clock()

    with nogil:
        for i in prange(<int>parnum, schedule='dynamic', chunksize=10, num_threads=cpunum):
            KDTree_rnn_query(kdtree, &parlist[i], parlist[i].loc, parlist[i].size * 2)

    if profiling == 1:
        print("-->neighbours time", clock() - stime, "sec")
        stime = clock()

    with nogil:
        for pair in xrange(2):
            for heaps in prange(<int>(parPool[0].max * scale) + 1, schedule='dynamic', chunksize=1, num_threads=cpunum):
                for i in xrange(parPool[0].parity[pair].heap[heaps].parnum):

                    collide(&parlist[parPool[0].parity[pair].heap[heaps].par[i]])

                    solve_link(&parlist[parPool[0].parity[pair].heap[heaps].par[i]])

                    if parlist[parPool[0].parity[pair].heap[heaps].par[i]].neighboursnum > 1:

                        # free(parlist[i].neighbours)

                        parlist[parPool[0].parity[pair].heap[heaps].par[i]].neighboursnum = 0

    # with nogil:
    #     for i in xrange(parnum):
    #         collide(&parlist[i])
    #         solve_link(&parlist[i])
    #         if parlist[i].neighboursnum > 1:
    #             #free(parlist[i].neighbours)
    #             parlist[i].neighboursnum = 0

    if profiling == 1:
        print("-->collide/solve link time", clock() - stime, "sec")
        stime = clock()

    exportdata = []
    parloc = []
    parvel = []
    parloctmp = []
    parveltmp = []

    for i in xrange(psysnum):
        for ii in xrange(psys[i].parnum):
            parloctmp.append(psys[i].particles[ii].loc[0])
            parloctmp.append(psys[i].particles[ii].loc[1])
            parloctmp.append(psys[i].particles[ii].loc[2])
            parveltmp.append(psys[i].particles[ii].vel[0])
            parveltmp.append(psys[i].particles[ii].vel[1])
            parveltmp.append(psys[i].particles[ii].vel[2])
        parloc.append(parloctmp)
        parvel.append(parveltmp)
        parloctmp = []
        parveltmp = [] 

    totallinks += newlinks
    pydeadlinks = 0
    for i in xrange(cpunum):
        pydeadlinks += deadlinks[i]
    totaldeadlinks += pydeadlinks

    exportdata = [parloc, parvel, newlinks, pydeadlinks, totallinks, totaldeadlinks]

    for pair in xrange(2):
        for heaps in range(<int>(parPool[0].max * scale) + 1):
            parPool[0].parity[pair].heap[heaps].parnum = 0
            free(parPool[0].parity[pair].heap[heaps].par)
        free(parPool[0].parity[pair].heap)
    free(parPool[0].parity)
    free(parPool)

    if profiling == 1:
        print("-->export time", clock() - stime, "sec")
        print("-->all process time", clock() - stime2, "sec")
        print("\n\n")
    #PROFILER_END
    return exportdata


cdef void update(mol_data):
    #PROFILER_START
    global parnum
    global psysnum
    global kdtree
    global psys

    cdef int i = 0
    cdef int ii = 0
    for i in xrange(psysnum):
        for ii in xrange(psys[i].parnum):
            psys[i].particles[ii].loc[0] = mol_data[i][0][(ii * 3)]
            psys[i].particles[ii].loc[1] = mol_data[i][0][(ii * 3) + 1]
            psys[i].particles[ii].loc[2] = mol_data[i][0][(ii * 3) + 2]
            psys[i].particles[ii].vel[0] = mol_data[i][1][(ii * 3)]
            psys[i].particles[ii].vel[1] = mol_data[i][1][(ii * 3) + 1]
            psys[i].particles[ii].vel[2] = mol_data[i][1][(ii * 3) + 2]

            if psys[i].particles[ii].state == 0 and mol_data[i][2][ii] == 0:
                psys[i].particles[ii].state = mol_data[i][2][ii] + 1
                if psys[i].links_active == 1:
                    KDTree_rnn_query(kdtree, &psys[i].particles[ii], psys[i].particles[ii].loc, psys[i].particles[ii].sys.link_length)
                    create_link(psys[i].particles[ii].id, psys[i].link_max, 0)
                    # free(psys[i].particles[ii].neighbours)
                    psys[i].particles[ii].neighboursnum = 0

            elif psys[i].particles[ii].state == 1 and mol_data[i][2][ii] == 0:
                psys[i].particles[ii].state = 1

            else:
                psys[i].particles[ii].state = mol_data[i][2][ii]

            psys[i].particles[ii].collided_with = <int *>realloc(psys[i].particles[ii].collided_with, 1 * cython.sizeof(int))
            psys[i].particles[ii].collided_num = 0
    #PROFILER_END
