static PyObject* simulate(PyObject *self, PyObject *args) {

    PyObject* importdata;

    int parse_result = PyArg_ParseTuple(args, "O", &importdata);
    if (!parse_result) {
        printf("importdata parse error\n");
        return NULL;
    }

    int i = 0;
    int ii = 0;
    int profiling = 1;

    float minX = INT_MAX;
    float minY = INT_MAX;
    float minZ = INT_MAX;

    float maxX = -INT_MAX;
    float maxY = -INT_MAX;
    float maxZ = -INT_MAX;

    float maxSize = -INT_MAX;

    clock_t stime2;
    clock_t stime;

    Pool *parPool = (Pool*) malloc(sizeof(Pool));

    parPool->parity = (Parity*) malloc(2 * sizeof(Parity));
    parPool[0].axis = -1;
    parPool[0].offset = 0;
    parPool[0].max = 0;

    newlinks = 0;
    deadlinks = 0;

    if (profiling == 1) {
        printf("-->start simulate\n");
        stime2 = clock();
        stime = clock();
    }

    update(importdata);

    if (profiling == 1) {
        printf("-->update time %.12f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    for (i=0; i<parnum; i++) {

        parlistcopy[i].id = parlist[i].id;
        parlistcopy[i].loc[0] = parlist[i].loc[0];

        if (parlist[i].loc[0] < minX) {
            minX = parlist[i].loc[0];
        }

        if (parlist[i].loc[0] > maxX) {
            maxX = parlist[i].loc[0];
        }

        parlistcopy[i].loc[1] = parlist[i].loc[1];

        if (parlist[i].loc[1] < minY) {
            minY = parlist[i].loc[1];
        }

        if (parlist[i].loc[1] > maxY) {
            maxY = parlist[i].loc[1];
        }

        parlistcopy[i].loc[2] = parlist[i].loc[2];

        if (parlist[i].loc[2] < minZ) {
            minZ = parlist[i].loc[2];
        }

        if (parlist[i].loc[2] > maxZ) {
            maxZ = parlist[i].loc[2];
        }

        if (parlist[i].sys->links_active == 1) {
            if (parlist[i].links_num > 0) {

                for (ii=0; ii<parlist[i].links_num; ii++) {
                    if (parlist[i].links[ii].lenght > maxSize) {
                        maxSize = parlist[i].links[ii].lenght;
                    }
                }

            }
        }

        if (parlist[i].size*2 > maxSize) {
            maxSize = parlist[i].size * 2;
        }
    }

    if ((maxX - minX) >= (maxY - minY) && (maxX - minX) >= (maxZ - minZ)) {
        parPool[0].axis = 0;
        parPool[0].offset = 0 - minX;
        parPool[0].max = maxX + parPool[0].offset;
    }

    if ((maxY - minY) > (maxX - minX) && (maxY - minY) > (maxZ - minZ)) {
        parPool[0].axis = 1;
        parPool[0].offset = 0 - minY;
        parPool[0].max = maxY + parPool[0].offset;
    }

    if ((maxZ - minZ) > (maxY - minY) && (maxZ - minZ) > (maxX - minX)) {
        parPool[0].axis = 2;
        parPool[0].offset = 0 - minZ;
        parPool[0].max = maxZ + parPool[0].offset;
    }

    if (parPool[0].max / 10 > maxSize) {
        maxSize = parPool[0].max / 10;
    }

    int pair;
    int heaps;
    float scale = 1 / (maxSize*2.1);

    for (pair=0; pair<2; pair++) {

        parPool[0].parity[pair].heap = (Heap*) malloc(((int)(parPool[0].max * scale) + 1) * sizeof(Heap));

        for (heaps=0; heaps<(int)(parPool[0].max * scale) + 1; heaps++) {
            parPool[0].parity[pair].heap[heaps].parnum = 0;
            parPool[0].parity[pair].heap[heaps].maxalloc = 50;
            parPool[0].parity[pair].heap[heaps].par = (int*) malloc(parPool[0].parity[pair].heap[heaps].maxalloc * sizeof(int));
        }
    }

    for (i=0; i<parnum; i++) {
        pair = (int)((parlist[i].loc[parPool[0].axis] + parPool[0].offset) * scale) % 2;
        heaps = (int) ((parlist[i].loc[parPool[0].axis] + parPool[0].offset) * scale);
        parPool[0].parity[pair].heap[heaps].parnum += 1;

        if (parPool[0].parity[pair].heap[heaps].parnum > parPool[0].parity[pair].heap[heaps].maxalloc) {
            parPool[0].parity[pair].heap[heaps].maxalloc = (int) (parPool[0].parity[pair].heap[heaps].maxalloc * 1.25);
            parPool[0].parity[pair].heap[heaps].par = (int*) realloc(parPool[0].parity[pair].heap[heaps].par, (parPool[0].parity[pair].heap[heaps].maxalloc + 2) * sizeof(int));
        }

        parPool[0].parity[pair].heap[heaps].par[(parPool[0].parity[pair].heap[heaps].parnum - 1)] = parlist[i].id;
    }


    if (profiling == 1) {
        printf("-->copy data time %.12f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    KDTree_create_tree(kdtree, parlistcopy, 0, parnum - 1, 0, -1, 0, 1);

    #pragma omp parallel for
    for (i=0; i<kdtree->thread_index; i++) {
        KDTree_create_tree(kdtree, parlistcopy, kdtree->thread_start[i], kdtree->thread_end[i], kdtree->thread_name[i], kdtree->thread_parent[i], kdtree->thread_depth[i], 0);
    }

    if (profiling == 1) {
        printf("-->create tree time %.12f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    #pragma omp parallel for
    for (i=0; i<parnum; i++) {
        KDTree_rnn_query(kdtree, &parlist[i], parlist[i].loc, parlist[i].size * 2);
    }

    if (profiling == 1) {
        printf("-->neighbours time %.12f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    for (pair=0; pair<2; pair++) {

        for (heaps=0; heaps<(int)(parPool[0].max * scale) + 1; heaps++) {

            #pragma omp parallel for
            for (i=0; i<parPool[0].parity[pair].heap[heaps].parnum; i++) {

                collide(&parlist[parPool[0].parity[pair].heap[heaps].par[i]]);
                solve_link(&parlist[parPool[0].parity[pair].heap[heaps].par[i]]);

                if (parlist[parPool[0].parity[pair].heap[heaps].par[i]].neighboursnum > 1) {
                    parlist[parPool[0].parity[pair].heap[heaps].par[i]].neighboursnum = 0;
                }
            }
        }
    }

    if (profiling == 1) {
        printf("-->collide/solve link time %.12f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    PyObject *exportdata = PyList_New(0);
    PyObject *parvel = PyList_New(0);

    for (i=0; i<psysnum; i++) {
        PyObject *parveltmp = PyList_New(0);

        for (ii=0; ii<psys[i].parnum; ii++) {

            PyObject *vel_x = Py_BuildValue("f", psys[i].particles[ii].vel[0]);
            PyObject *vel_y = Py_BuildValue("f", psys[i].particles[ii].vel[1]);
            PyObject *vel_z = Py_BuildValue("f", psys[i].particles[ii].vel[2]);

            PyList_Append(parveltmp, vel_x);
            PyList_Append(parveltmp, vel_y);
            PyList_Append(parveltmp, vel_z);

        }

        PyList_Append(parvel, parveltmp);
    }

    totallinks += newlinks;
    int pydeadlinks = 0;

    pydeadlinks += deadlinks;
    totaldeadlinks += pydeadlinks;

    PyList_Append(exportdata, parvel);
    PyList_Append(exportdata, Py_BuildValue("i", newlinks));
    PyList_Append(exportdata, Py_BuildValue("i", pydeadlinks));
    PyList_Append(exportdata, Py_BuildValue("i", totallinks));
    PyList_Append(exportdata, Py_BuildValue("i", totaldeadlinks));

    for (pair=0; pair<2; pair++) {

        for (heaps=0; heaps<(int)(parPool[0].max * scale) + 1; heaps++) {
            parPool[0].parity[pair].heap[heaps].parnum = 0;
            free(parPool[0].parity[pair].heap[heaps].par);
        }

        free(parPool[0].parity[pair].heap);
    }

    free(parPool[0].parity);
    free(parPool);


    if (profiling == 1) {
        printf("-->export time %.12f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        printf("-->all process time %.12f sec\n", (double)(clock() - stime2) / CLOCKS_PER_SEC);
        printf("\n\n");
    }

    return exportdata;
}
