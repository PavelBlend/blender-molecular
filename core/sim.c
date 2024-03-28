static PyObject* simulate(PyObject *self, PyObject *args) {

    PyObject* importdata;

    int parse_result = PyArg_ParseTuple(args, "O", &importdata);
    if (!parse_result) {
        printf("importdata parse error\n");
        return NULL;
    }

    int profiling = 1;

    float minX = +INT_MAX;
    float minY = +INT_MAX;
    float minZ = +INT_MAX;

    float maxX = -INT_MAX;
    float maxY = -INT_MAX;
    float maxZ = -INT_MAX;

    float maxSize = -INT_MAX;

    clock_t stime2;
    clock_t stime;

    Pool *parPool = (Pool*) malloc(sizeof(Pool));

    parPool->parity = (Parity*) malloc(2 * sizeof(Parity));
    parPool->axis = -1;
    parPool->offset = 0.0;
    parPool->max = 0.0;

    newlinks = 0;
    deadlinks = 0;

    if (profiling == 1) {
        printf("-->start simulate\n");
        stime2 = clock();
        stime = clock();
    }

    update(importdata);

    if (profiling == 1) {
        printf("-->update time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    int par_index = 0;

    #pragma omp parallel for
    for (par_index=0; par_index<parnum; par_index++) {

        parlistcopy[par_index].id = parlist[par_index].id;

        parlistcopy[par_index].loc[0] = parlist[par_index].loc[0];
        parlistcopy[par_index].loc[1] = parlist[par_index].loc[1];
        parlistcopy[par_index].loc[2] = parlist[par_index].loc[2];

        // search min/max coordinates

        if (parlist[par_index].loc[0] < minX) {
            minX = parlist[par_index].loc[0];
        }

        if (parlist[par_index].loc[0] > maxX) {
            maxX = parlist[par_index].loc[0];
        }

        if (parlist[par_index].loc[1] < minY) {
            minY = parlist[par_index].loc[1];
        }

        if (parlist[par_index].loc[1] > maxY) {
            maxY = parlist[par_index].loc[1];
        }

        if (parlist[par_index].loc[2] < minZ) {
            minZ = parlist[par_index].loc[2];
        }

        if (parlist[par_index].loc[2] > maxZ) {
            maxZ = parlist[par_index].loc[2];
        }

        if (parlist[par_index].sys->links_active == 1 && parlist[par_index].links_num > 0) {
            for (int link_index=0; link_index<parlist[par_index].links_num; link_index++) {
                if (parlist[par_index].links[link_index].lenght > maxSize) {
                    maxSize = parlist[par_index].links[link_index].lenght;
                }
            }
        }

        if (parlist[par_index].size * 2 > maxSize) {
            maxSize = parlist[par_index].size * 2;
        }
    }

    if ((maxX - minX) >= (maxY - minY) && (maxX - minX) >= (maxZ - minZ)) {
        parPool->axis = 0;
        parPool->offset = 0 - minX;
        parPool->max = maxX + parPool->offset;
    }

    if ((maxY - minY) > (maxX - minX) && (maxY - minY) > (maxZ - minZ)) {
        parPool->axis = 1;
        parPool->offset = 0 - minY;
        parPool->max = maxY + parPool->offset;
    }

    if ((maxZ - minZ) > (maxY - minY) && (maxZ - minZ) > (maxX - minX)) {
        parPool->axis = 2;
        parPool->offset = 0 - minZ;
        parPool->max = maxZ + parPool->offset;
    }

    if (parPool->max / 10 > maxSize) {
        maxSize = parPool->max / 10;
    }

    int pair;
    int heaps;
    float scale = 1 / (maxSize*2.1);

    for (pair=0; pair<2; pair++) {

        parPool->parity[pair].heap = (Heap*) malloc(((int)(parPool->max * scale) + 1) * sizeof(Heap));

        for (heaps=0; heaps<(int)(parPool->max * scale) + 1; heaps++) {
            parPool->parity[pair].heap[heaps].parnum = 0;
            parPool->parity[pair].heap[heaps].maxalloc = 50;
            parPool->parity[pair].heap[heaps].par = (int*) malloc(parPool->parity[pair].heap[heaps].maxalloc * sizeof(int));
        }
    }

    for (int par_index=0; par_index<parnum; par_index++) {
        pair = (int)((parlist[par_index].loc[parPool->axis] + parPool->offset) * scale) % 2;
        heaps = (int) ((parlist[par_index].loc[parPool->axis] + parPool->offset) * scale);
        parPool->parity[pair].heap[heaps].parnum += 1;

        if (parPool->parity[pair].heap[heaps].parnum > parPool->parity[pair].heap[heaps].maxalloc) {
            parPool->parity[pair].heap[heaps].maxalloc = (int) (parPool->parity[pair].heap[heaps].maxalloc * 1.25);
            parPool->parity[pair].heap[heaps].par = (int*) realloc(parPool->parity[pair].heap[heaps].par, (parPool->parity[pair].heap[heaps].maxalloc + 2) * sizeof(int));
        }

        parPool->parity[pair].heap[heaps].par[(parPool->parity[pair].heap[heaps].parnum - 1)] = parlist[par_index].id;
    }

    if (profiling == 1) {
        printf("-->copy data time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    KDTree_create_tree(kdtree, parlistcopy, 0, parnum - 1, 0, -1, 0, 1);

    int i = 0;

    #pragma omp parallel for schedule(dynamic, 10)
    for (i=0; i<kdtree->thread_index; i++) {
        KDTree_create_tree(kdtree, parlistcopy, kdtree->thread_start[i], kdtree->thread_end[i], kdtree->thread_name[i], kdtree->thread_parent[i], kdtree->thread_depth[i], 0);
    }

    if (profiling == 1) {
        printf("-->create tree time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    #pragma omp parallel for schedule(dynamic, 10)
    for (par_index=0; par_index<parnum; par_index++) {
        KDTree_rnn_query(kdtree, &parlist[par_index], parlist[par_index].loc, parlist[par_index].size * 2);
    }

    if (profiling == 1) {
        printf("-->neighbours time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    for (pair=0; pair<2; pair++) {

        for (heaps=0; heaps<(int)(parPool->max * scale) + 1; heaps++) {

            for (int par_index=0; par_index<parPool->parity[pair].heap[heaps].parnum; par_index++) {

                collide(&parlist[parPool->parity[pair].heap[heaps].par[par_index]]);
                solve_link(&parlist[parPool->parity[pair].heap[heaps].par[par_index]]);

                if (parlist[parPool->parity[pair].heap[heaps].par[par_index]].neighboursnum > 1) {
                    parlist[parPool->parity[pair].heap[heaps].par[par_index]].neighboursnum = 0;
                }
            }
        }
    }

    if (profiling == 1) {
        printf("-->collide/solve link time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        stime = clock();
    }

    PyObject *exportdata = PyList_New(0);
    PyObject *parvel = PyList_New(0);

    for (int par_sys_index=0; par_sys_index<psysnum; par_sys_index++) {
        PyObject *parveltmp = PyList_New(psys[par_sys_index].parnum * 3);

        for (int par_index=0; par_index<psys[par_sys_index].parnum; par_index++) {

            PyList_SetItem(parveltmp, par_index*3,     Py_BuildValue("f", psys[par_sys_index].particles[par_index].vel[0]));
            PyList_SetItem(parveltmp, par_index*3 + 1, Py_BuildValue("f", psys[par_sys_index].particles[par_index].vel[1]));
            PyList_SetItem(parveltmp, par_index*3 + 2, Py_BuildValue("f", psys[par_sys_index].particles[par_index].vel[2]));

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

        for (heaps=0; heaps<(int)(parPool->max * scale) + 1; heaps++) {
            parPool->parity[pair].heap[heaps].parnum = 0;
            free(parPool->parity[pair].heap[heaps].par);
        }

        free(parPool->parity[pair].heap);
    }

    free(parPool->parity);
    free(parPool);

    if (profiling == 1) {
        printf("-->export time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
        printf("-->all process time %.3f sec\n", (double)(clock() - stime2) / CLOCKS_PER_SEC);
        printf("\n");
    }

    return exportdata;
}
