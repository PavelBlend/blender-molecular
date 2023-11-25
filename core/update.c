void update(PyObject *mol_data) {
    int i;
    int ii;
    int par_state;

    for (i=0; i<psysnum; i++) {
        PyObject* psys_props = PyList_GetItem(mol_data, i);

        PyObject* location = PyList_GetItem(psys_props, 0);
        PyObject* velocity = PyList_GetItem(psys_props, 1);
        PyObject* state = PyList_GetItem(psys_props, 2);

        for (ii=0; ii<psys[i].parnum; ii++) {

            psys[i].particles[ii].loc[0] = (float)PyFloat_AsDouble(PyList_GetItem(location, ii*3));
            psys[i].particles[ii].loc[1] = (float)PyFloat_AsDouble(PyList_GetItem(location, ii*3 + 1));
            psys[i].particles[ii].loc[2] = (float)PyFloat_AsDouble(PyList_GetItem(location, ii*3 + 2));

            psys[i].particles[ii].vel[0] = (float)PyFloat_AsDouble(PyList_GetItem(velocity, ii*3));
            psys[i].particles[ii].vel[1] = (float)PyFloat_AsDouble(PyList_GetItem(velocity, ii*3 + 1));
            psys[i].particles[ii].vel[2] = (float)PyFloat_AsDouble(PyList_GetItem(velocity, ii*3 + 2));

            par_state = PyLong_AsLong(PyList_GetItem(state, ii));

            if (psys[i].particles[ii].state == 0 && par_state == 0) {
                psys[i].particles[ii].state = par_state + 1;

                if (psys[i].links_active == 1) {
                    KDTree_rnn_query(kdtree, &psys[i].particles[ii], psys[i].particles[ii].loc, psys[i].particles[ii].sys->link_length);
                    create_link(psys[i].particles[ii].id, psys[i].link_max, 0, -1);
                    psys[i].particles[ii].neighboursnum = 0;
                }

            } else if (psys[i].particles[ii].state == 1 && par_state == 0) {
                psys[i].particles[ii].state = 1;

            } else {
                psys[i].particles[ii].state = par_state;
            }

            psys[i].particles[ii].collided_with = (int*) realloc(psys[i].particles[ii].collided_with, sizeof(int));
            psys[i].particles[ii].collided_num = 0;
        }
    }
}
