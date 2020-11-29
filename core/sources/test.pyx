cdef testkdtree(int verbose = 0):
    if verbose >= 3:
        print("RootNode:", kdtree.root_node[0].index)
        for i in xrange(parnum):
            print(
                "Parent",
                kdtree.nodes[i].index,
                "Particle:",
                kdtree.nodes[i].particle[0].id
            )
            print("    Left", kdtree.nodes[i].left_child[0].index)
            print("    Right", kdtree.nodes[i].right_child[0].index)

    cdef float *a = [0, 0, 0]
    cdef Particle *b
    b = <Particle *>malloc(1 * cython.sizeof(Particle))
    if verbose >= 1:
        print("start searching")
    KDTree_rnn_query(kdtree, b, a, 2)
    output = []
    if verbose >= 2:
        print("Result")
        for i in xrange(b[0].neighboursnum):
            print(" Query Particle:", parlist[b[0].neighbours[i]].id)
    if verbose >= 1:
        print("number of particle find:", b[0].neighboursnum)
    free(b)


cdef void printdb(int linenumber, text = ""):
    cdef int dbactive = 1
    if dbactive == 1:
        print(linenumber)
