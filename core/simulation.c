#include "simulation.h"

static PyObject* simulate(PyObject *self, PyObject *args) {

    // parse import data
    PyObject* importdata;

    int parse_result = PyArg_ParseTuple(args, "O", &importdata);
    if (!parse_result) {
        printf("importdata parse error\n");
        return NULL;
    }

    // min particles coordinate
    float MX = (float)(INT_MAX);
    float min_x = +MX;
    float min_y = +MX;
    float min_z = +MX;

    // max particles coordinate
    float max_x = -MX;
    float max_y = -MX;
    float max_z = -MX;

    // max particle link length
    float link_max_size = -MX;

    Pool *parPool;
    Parity *parity;

    newlinks = 0;
    deadlinks = 0;

    float scale;
    float double_size;
    float potential_link_max_size;
    float range_x;
    float range_y;
    float range_z;
    int par_index;

    update(importdata);

    for (int step=0; step<substep; step++) {
            printf("test 1\n");

            parPool = (Pool*)safe_malloc(sizeof(Pool), "parPool");
            parity = (Parity*)safe_malloc(2 * sizeof(Parity), "parity");

            parPool->parity = parity;

            parPool->axis = -1;
            parPool->offset = 0.0;
            parPool->max = 0.0;

            for (par_index=0; par_index<parnum; par_index++) {
                parlistcopy[par_index].id = parlist[par_index].id;

                memcpy(parlistcopy[par_index].loc, parlist[par_index].loc, sizeof(parlist[par_index].loc));

                // search min/max coordinates
                if (parlist[par_index].loc[0] < min_x) min_x = parlist[par_index].loc[0];
                if (parlist[par_index].loc[0] > max_x) max_x = parlist[par_index].loc[0];
                if (parlist[par_index].loc[1] < min_y) min_y = parlist[par_index].loc[1];
                if (parlist[par_index].loc[1] > max_y) max_y = parlist[par_index].loc[1];
                if (parlist[par_index].loc[2] < min_z) min_z = parlist[par_index].loc[2];
                if (parlist[par_index].loc[2] > max_z) max_z = parlist[par_index].loc[2];

                if (parlist[par_index].sys->links_active == 1 && parlist[par_index].links_num > 0) {
                    for (int link_index=0; link_index<parlist[par_index].links_num; link_index++) {
                        if (parlist[par_index].links[link_index].lenght > link_max_size) {
                            link_max_size = parlist[par_index].links[link_index].lenght;
                        }
                    }
                }

                double_size = parlist[par_index].size * 2;
                if (double_size > link_max_size) link_max_size = double_size;

            }
        printf("test 3\n");

        range_x = max_x - min_x;
        range_y = max_y - min_y;
        range_z = max_z - min_z;

        if (range_x >= range_y && range_x >= range_z) {
            parPool->axis = 0;
            parPool->offset = 0 - min_x;
            parPool->max = max_x + parPool->offset;
        }

        if (range_y > range_x && range_y > range_z) {
            parPool->axis = 1;
            parPool->offset = 0 - min_y;
            parPool->max = max_y + parPool->offset;
        }

        if (range_z > range_x && range_z > range_y) {
            parPool->axis = 2;
            parPool->offset = 0 - min_z;
            parPool->max = max_z + parPool->offset;
        }

        potential_link_max_size = parPool->max / 10;
        if (potential_link_max_size > link_max_size) link_max_size = potential_link_max_size;

        scale = (float)(1 / (link_max_size * 2.1));

        printf("test 4\n");

        for (int pair=0; pair<2; pair++) {
            parPool->parity[pair].heap = (Heap*)safe_malloc(((int)(parPool->max * scale) + 1) * sizeof(Heap), "parPool->parity[pair].heap");

            for (int heaps=0; heaps<(int)(parPool->max * scale) + 1; heaps++) {
                parPool->parity[pair].heap[heaps].parnum = 0;
                parPool->parity[pair].heap[heaps].maxalloc = 50;
                parPool->parity[pair].heap[heaps].par = (int*)safe_malloc(parPool->parity[pair].heap[heaps].maxalloc * sizeof(int), "parPool->parity[pair].heap[heaps].par");
            }
        }

        printf("test 5\n");

        for (int par_index=0; par_index<parnum; par_index++) {
            int axis = (int)parPool->axis;
            int local_offset = (int)((parlist[par_index].loc[axis] + parPool->offset) * scale);
            int pair  = (int) (local_offset % 2);
            int heaps = (int) local_offset;
            parPool->parity[pair].heap[heaps].parnum += 1;

            int local_maxalloc = parPool->parity[pair].heap[heaps].maxalloc;
            if (parPool->parity[pair].heap[heaps].parnum > local_maxalloc) {
                parPool->parity[pair].heap[heaps].maxalloc = local_maxalloc = (int) (local_maxalloc * 1.25);
                
                parPool->parity[pair].heap[heaps].par = safe_realloc(parPool->parity[pair].heap[heaps].par, (local_maxalloc + 2) * sizeof(int),"heap[heaps].par");
            }

            parPool->parity[pair].heap[heaps].par[(parPool->parity[pair].heap[heaps].parnum - 1)] = parlist[par_index].id;
        }

        printf("test 6\n");

        KDTree_create_tree(kdtree, parlistcopy, 0, parnum - 1, 0, -1, 0, 1);

            int i;
            for (i=0; i<kdtree->thread_index; i++) {
                KDTree_create_tree(kdtree, parlistcopy, kdtree->thread_start[i], kdtree->thread_end[i], kdtree->thread_name[i], kdtree->thread_parent[i], kdtree->thread_depth[i], 0);
            }

            for (par_index=0; par_index<parnum; par_index++) {
                KDTree_rnn_query(kdtree, &parlist[par_index], parlist[par_index].loc, parlist[par_index].size * 2);
            }

            for (int pair=0; pair<2; pair++) {
                int heaps;
                for (heaps=0; heaps<(int)(parPool->max * scale) + 1; heaps++) {
                    int par_index;

                    for (par_index=0; par_index<parPool->parity[pair].heap[heaps].parnum; par_index++) {

                        collide(&parlist[parPool->parity[pair].heap[heaps].par[par_index]]);
                        solve_link(&parlist[parPool->parity[pair].heap[heaps].par[par_index]]);

                        if (parlist[parPool->parity[pair].heap[heaps].par[par_index]].neighboursnum > 1) {
                            parlist[parPool->parity[pair].heap[heaps].par[par_index]].neighboursnum = 0;
                        }
                    }
                }
            }

        // update particles position
        int par_id;
        float gravity_z = -9.81;
        float dt = 1.0 / (substep * fps);
        for (par_id=0; par_id<parnum; par_id++) {
            parlist[par_id].loc[0] += dt * parlist[par_id].vel[0];
            parlist[par_id].loc[1] += dt * parlist[par_id].vel[1];
            // added gravity
            //parlist[par_id].vel[2] += gravity_z;
            parlist[par_id].loc[2] += dt * parlist[par_id].vel[2] + (0.5 * (-9.81) * dt * dt);
        }

        printf("test 7\n");

        // free memory
        for (int pair=0; pair<2; pair++) {

            for (int heaps=0; heaps<(int)(parPool->max * scale) + 1; heaps++) {
                parPool->parity[pair].heap[heaps].parnum = 0;
                free(parPool->parity[pair].heap[heaps].par);
            }

            free(parPool->parity[pair].heap);
        }

        free(parPool->parity);
        free(parPool);
        printf("test 2\n");
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

    return exportdata;
}
