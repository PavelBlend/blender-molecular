static PyObject* simulate(PyObject *self, PyObject *args) {

    // parse import data
    PyObject* importdata;

    int parse_result = PyArg_ParseTuple(args, "O", &importdata);
    if (!parse_result) {
        printf("importdata parse error\n");
        return NULL;
    }

    // min particles coordinate
    float min_x = +INT_MAX;
    float min_y = +INT_MAX;
    float min_z = +INT_MAX;

    // max particles coordinate
    float max_x = -INT_MAX;
    float max_y = -INT_MAX;
    float max_z = -INT_MAX;

    // max particle link length
    float link_max_size = -INT_MAX;

    clock_t stime2;
    clock_t stime;

    Pool *parPool = (Pool*) malloc(sizeof(Pool));

    parPool->parity = (Parity*) malloc(2 * sizeof(Parity));
    parPool->axis = -1;
    parPool->offset = 0.0;
    parPool->max = 0.0;

    newlinks = 0;
    deadlinks = 0;

    printf("-->start simulate\n");
    stime2 = clock();
    stime = clock();

    // update import data
    update(importdata);

    printf("-->update time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
    stime = clock();

    int par_index = 0;

    #pragma omp parallel for
    for (par_index=0; par_index<parnum; par_index++) {

        parlistcopy[par_index].id = parlist[par_index].id;

        parlistcopy[par_index].loc[0] = parlist[par_index].loc[0];
        parlistcopy[par_index].loc[1] = parlist[par_index].loc[1];
        parlistcopy[par_index].loc[2] = parlist[par_index].loc[2];

        // search min/max coordinates

        if (parlist[par_index].loc[0] < min_x) {
            min_x = parlist[par_index].loc[0];
        }

        if (parlist[par_index].loc[0] > max_x) {
            max_x = parlist[par_index].loc[0];
        }

        if (parlist[par_index].loc[1] < min_y) {
            min_y = parlist[par_index].loc[1];
        }

        if (parlist[par_index].loc[1] > max_y) {
            max_y = parlist[par_index].loc[1];
        }

        if (parlist[par_index].loc[2] < min_z) {
            min_z = parlist[par_index].loc[2];
        }

        if (parlist[par_index].loc[2] > max_z) {
            max_z = parlist[par_index].loc[2];
        }

        if (parlist[par_index].sys->links_active == 1 && parlist[par_index].links_num > 0) {
            for (int link_index=0; link_index<parlist[par_index].links_num; link_index++) {
                if (parlist[par_index].links[link_index].lenght > link_max_size) {
                    link_max_size = parlist[par_index].links[link_index].lenght;
                }
            }
        }

        if (parlist[par_index].size * 2 > link_max_size) {
            link_max_size = parlist[par_index].size * 2;
        }
    }

    if ((max_x - min_x) >= (max_y - min_y) && (max_x - min_x) >= (max_z - min_z)) {
        parPool->axis = 0;
        parPool->offset = 0 - min_x;
        parPool->max = max_x + parPool->offset;
    }

    if ((max_y - min_y) > (max_x - min_x) && (max_y - min_y) > (max_z - min_z)) {
        parPool->axis = 1;
        parPool->offset = 0 - min_y;
        parPool->max = max_y + parPool->offset;
    }

    if ((max_z - min_z) > (max_y - min_y) && (max_z - min_z) > (max_x - min_x)) {
        parPool->axis = 2;
        parPool->offset = 0 - min_z;
        parPool->max = max_z + parPool->offset;
    }

    if (parPool->max / 10 > link_max_size) {
        link_max_size = parPool->max / 10;
    }

    int pair;
    int heaps;
    float scale = 1 / (link_max_size * 2.1);

    for (pair=0; pair<2; pair++) {

        parPool->parity[pair].heap = (Heap*) malloc(((int)(parPool->max * scale) + 1) * sizeof(Heap));

        for (heaps=0; heaps<(int)(parPool->max * scale) + 1; heaps++) {
            parPool->parity[pair].heap[heaps].parnum = 0;
            parPool->parity[pair].heap[heaps].maxalloc = 50;
            parPool->parity[pair].heap[heaps].par = (int*) malloc(parPool->parity[pair].heap[heaps].maxalloc * sizeof(int));
        }
    }

    for (par_index=0; par_index<parnum; par_index++) {
        pair = (int)((parlist[par_index].loc[parPool->axis] + parPool->offset) * scale) % 2;
        heaps = (int) ((parlist[par_index].loc[parPool->axis] + parPool->offset) * scale);
        parPool->parity[pair].heap[heaps].parnum += 1;

        if (parPool->parity[pair].heap[heaps].parnum > parPool->parity[pair].heap[heaps].maxalloc) {
            parPool->parity[pair].heap[heaps].maxalloc = (int) (parPool->parity[pair].heap[heaps].maxalloc * 1.25);
            parPool->parity[pair].heap[heaps].par = (int*) realloc(parPool->parity[pair].heap[heaps].par, (parPool->parity[pair].heap[heaps].maxalloc + 2) * sizeof(int));
        }

        parPool->parity[pair].heap[heaps].par[(parPool->parity[pair].heap[heaps].parnum - 1)] = parlist[par_index].id;
    }

    printf("-->copy data time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
    stime = clock();

    // kd-tree

    KDTree_create_tree(kdtree, parlistcopy, 0, parnum - 1, 0, -1, 0, 1);

    int i = 0;

    #pragma omp parallel for schedule(dynamic, 10)
    for (i=0; i<kdtree->thread_index; i++) {
        KDTree_create_tree(kdtree, parlistcopy, kdtree->thread_start[i], kdtree->thread_end[i], kdtree->thread_name[i], kdtree->thread_parent[i], kdtree->thread_depth[i], 0);
    }

    printf("-->create tree time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
    stime = clock();

    #pragma omp parallel for schedule(dynamic, 10)
    for (par_index=0; par_index<parnum; par_index++) {
        KDTree_rnn_query(kdtree, &parlist[par_index], parlist[par_index].loc, parlist[par_index].size * 2);
    }

    printf("-->neighbours time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
    stime = clock();

    // simulation

    for (pair=0; pair<2; pair++) {

        for (heaps=0; heaps<(int)(parPool->max * scale) + 1; heaps++) {

            for (par_index=0; par_index<parPool->parity[pair].heap[heaps].parnum; par_index++) {

                collide(&parlist[parPool->parity[pair].heap[heaps].par[par_index]]);
                solve_link(&parlist[parPool->parity[pair].heap[heaps].par[par_index]]);

                if (parlist[parPool->parity[pair].heap[heaps].par[par_index]].neighboursnum > 1) {
                    parlist[parPool->parity[pair].heap[heaps].par[par_index]].neighboursnum = 0;
                }
            }
        }
    }

    printf("-->collide/solve link time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
    stime = clock();

    // export

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

    printf("-->export time %.3f sec\n", (double)(clock() - stime) / CLOCKS_PER_SEC);
    printf("-->all process time %.3f sec\n", (double)(clock() - stime2) / CLOCKS_PER_SEC);
    printf("\n");

    return exportdata;
}
