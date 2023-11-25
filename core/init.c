static PyObject* init(PyObject *self, PyObject *args) {

    PyObject* importdata;

    int parse_result = PyArg_ParseTuple(args, "O", &importdata);
    if (!parse_result) {
        printf("error %d", 0);
        return NULL;
    }

    int is_list = PyList_Check(importdata);
    if (!is_list) {
        printf("error %d", 1);
        return NULL;
    }

    PyObject* settings = PyList_GetItem(importdata, 0);
    is_list = PyList_Check(settings);
    if (!is_list) {
        printf("error %d", 2);
        return NULL;
    }

    int i = 0;
    int ii = 0;
    int jj = 0;
    int index = 0;
    int profiling = 0;

    newlinks = 0;
    totallinks = 0;
    totaldeadlinks = 0;

    fps = (float)PyFloat_AsDouble(PyList_GetItem(settings, 0));
    substep = PyLong_AsLongLong(PyList_GetItem(settings, 1));
    psysnum = PyLong_AsLongLong(PyList_GetItem(settings, 2));
    parnum = PyLong_AsLongLong(PyList_GetItem(settings, 3));
    cpunum = PyLong_AsLongLong(PyList_GetItem(settings, 4));

    deltatime = fps * (float)(substep + 1);
    deadlinks = (int*) malloc(cpunum * sizeof(int));

    psys = (ParSys*) malloc(psysnum * sizeof(ParSys));
    parlist = (Particle*) malloc(parnum * sizeof(Particle));
    par_id_list = (int*) malloc(parnum * sizeof(int));
    parlistcopy = (SParticle*) malloc(parnum * sizeof(SParticle));

    for (i=0; i<psysnum; i++) {

        PyObject* psys_props = PyList_GetItem(importdata, i+1);

        psys[i].id = i;
        psys[i].parnum = PyLong_AsLongLong(PyList_GetItem(psys_props, 0));
        psys[i].particles = (Particle*) malloc(psys[i].parnum * sizeof(Particle));
        psys[i].particles = &parlist[jj];

        PyObject* tex_props = PyList_GetItem(psys_props, 6);
        index = 48;

        // link tension
        psys[i].use_link_tension_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_link_tension_tex) {
            psys[i].link_tension_tex = (float*) malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].link_tension_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // link stiffness
        psys[i].use_link_stiff_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_link_stiff_tex) {
            psys[i].link_stiff_tex = (float*) malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values_2 = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].link_stiff_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values_2, ii));
            }
        }
        index += 2;

        // link expansion stiffness
        psys[i].use_link_estiff_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_link_estiff_tex) {
            psys[i].link_estiff_tex = (float*) malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].link_estiff_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // link damping
        psys[i].use_link_damp_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_link_damp_tex) {
            psys[i].link_damp_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].link_damp_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // link expansion damping
        psys[i].use_link_edamp_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_link_edamp_tex) {
            psys[i].link_edamp_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].link_edamp_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // link broken
        psys[i].use_link_broken_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_link_broken_tex) {
            psys[i].link_broken_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].link_broken_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // link expansion broken
        psys[i].use_link_ebroken_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_link_ebroken_tex) {
            psys[i].link_ebroken_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].link_ebroken_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // relink tension
        psys[i].use_relink_tension_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_relink_tension_tex) {
            psys[i].relink_tension_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].relink_tension_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // relink stiffness
        psys[i].use_relink_stiff_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_relink_stiff_tex) {
            psys[i].relink_stiff_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].relink_stiff_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // relink expansion stiffness
        psys[i].use_relink_estiff_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_relink_estiff_tex) {
            psys[i].relink_estiff_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].relink_estiff_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // relink damping
        psys[i].use_relink_damp_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_relink_damp_tex) {
            psys[i].relink_damp_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].relink_damp_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // relink expansion damping
        psys[i].use_relink_edamp_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_relink_edamp_tex) {
            psys[i].relink_edamp_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].relink_edamp_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // relink broken
        psys[i].use_relink_broken_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_relink_broken_tex) {
            psys[i].relink_broken_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].relink_broken_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // relink expansion broken
        psys[i].use_relink_ebroken_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_relink_ebroken_tex) {
            psys[i].relink_ebroken_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].relink_ebroken_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // link friction
        psys[i].use_link_friction_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_link_friction_tex) {
            psys[i].link_friction_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].link_friction_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // relink friction
        psys[i].use_relink_friction_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_relink_friction_tex) {
            psys[i].relink_friction_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].relink_friction_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        // relink tension
        psys[i].use_relink_chance_tex = PyLong_AsLongLong(PyList_GetItem(tex_props, index+1));
        if (psys[i].use_relink_chance_tex) {
            psys[i].relink_chance_tex = (float*)malloc(psys[i].parnum * sizeof(float));
            PyObject* tex_values = PyList_GetItem(tex_props, index);
            for (ii=0; ii<psys[i].parnum; ii++) {
                psys[i].relink_chance_tex[ii] = (float)PyFloat_AsDouble(PyList_GetItem(tex_values, ii));
            }
        }
        index += 2;

        psys[i].selfcollision_active    =       PyLong_AsLongLong(PyList_GetItem(tex_props,  0));
        psys[i].othercollision_active   =       PyLong_AsLongLong(PyList_GetItem(tex_props,  1));
        psys[i].collision_group         =       PyLong_AsLongLong(PyList_GetItem(tex_props,  2));
        psys[i].friction                = (float)PyFloat_AsDouble(PyList_GetItem(tex_props,  3));
        psys[i].collision_damp          = (float)PyFloat_AsDouble(PyList_GetItem(tex_props,  4));
        psys[i].links_active            =       PyLong_AsLongLong(PyList_GetItem(tex_props,  5));
        psys[i].link_length             = (float)PyFloat_AsDouble(PyList_GetItem(tex_props,  6));
        psys[i].link_max                =       PyLong_AsLongLong(PyList_GetItem(tex_props,  7));
        psys[i].link_tension            = (float)PyFloat_AsDouble(PyList_GetItem(tex_props,  8));
        psys[i].link_tensionrand        = (float)PyFloat_AsDouble(PyList_GetItem(tex_props,  9));
        psys[i].link_stiff              = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 10)) * 0.5;
        psys[i].link_stiffrand          = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 11));
        psys[i].link_stiffexp           = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 12));
        psys[i].link_damp               = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 13));
        psys[i].link_damprand           = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 14));
        psys[i].link_broken             = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 15));
        psys[i].link_brokenrand         = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 16));
        psys[i].link_estiff             = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 17)) * 0.5;
        psys[i].link_estiffrand         = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 18));
        psys[i].link_estiffexp          = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 19));
        psys[i].link_edamp              = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 20));
        psys[i].link_edamprand          = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 21));
        psys[i].link_ebroken            = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 22));
        psys[i].link_ebrokenrand        = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 23));
        psys[i].relink_group            =       PyLong_AsLongLong(PyList_GetItem(tex_props, 24));
        psys[i].relink_chance           = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 25));
        psys[i].relink_chancerand       = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 26));
        psys[i].relink_max              =       PyLong_AsLongLong(PyList_GetItem(tex_props, 27));
        psys[i].relink_tension          = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 28));
        psys[i].relink_tensionrand      = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 29));
        psys[i].relink_stiff            = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 30)) * 0.5;
        psys[i].relink_stiffexp         = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 31));
        psys[i].relink_stiffrand        = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 32));
        psys[i].relink_damp             = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 33));
        psys[i].relink_damprand         = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 34));
        psys[i].relink_broken           = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 35));
        psys[i].relink_brokenrand       = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 36));
        psys[i].relink_estiff           = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 37)) * 0.5;
        psys[i].relink_estiffexp        = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 38));
        psys[i].relink_estiffrand       = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 39));
        psys[i].relink_edamp            = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 40));
        psys[i].relink_edamprand        = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 41));
        psys[i].relink_ebroken          = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 42));
        psys[i].relink_ebrokenrand      = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 43));
        psys[i].link_friction           = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 44));
        psys[i].link_group              =       PyLong_AsLongLong(PyList_GetItem(tex_props, 45));
        psys[i].other_link_active       =       PyLong_AsLongLong(PyList_GetItem(tex_props, 46));
        psys[i].link_frictionrand       = (float)PyFloat_AsDouble(PyList_GetItem(tex_props, 47));

        PyObject* location = PyList_GetItem(psys_props, 1);
        PyObject* velocity = PyList_GetItem(psys_props, 2);
        PyObject* size = PyList_GetItem(psys_props, 3);
        PyObject* mass = PyList_GetItem(psys_props, 4);
        PyObject* state = PyList_GetItem(psys_props, 5);

        for (ii=0; ii<psys[i].parnum; ii++) {
            parlist[jj].id = jj;
            par_id_list[jj] = ii;

            parlist[jj].loc[0] = (float)PyFloat_AsDouble(PyList_GetItem(location, ii*3));
            parlist[jj].loc[1] = (float)PyFloat_AsDouble(PyList_GetItem(location, ii*3 + 1));
            parlist[jj].loc[2] = (float)PyFloat_AsDouble(PyList_GetItem(location, ii*3 + 2));
            //printf("loc = %.3f, %.3f, %.3f \n", parlist[jj].loc[0], parlist[jj].loc[1], parlist[jj].loc[2]);

            parlist[jj].vel[0] = (float)PyFloat_AsDouble(PyList_GetItem(velocity, ii*3));
            parlist[jj].vel[1] = (float)PyFloat_AsDouble(PyList_GetItem(velocity, ii*3 + 1));
            parlist[jj].vel[2] = (float)PyFloat_AsDouble(PyList_GetItem(velocity, ii*3 + 2));
            //printf("vel = %.3f, %.3f, %.3f \n", parlist[jj].vel[0], parlist[jj].vel[1], parlist[jj].vel[2]);

            parlist[jj].size  = (float) PyFloat_AsDouble(PyList_GetItem(size,  ii));
            parlist[jj].mass  = (float) PyFloat_AsDouble(PyList_GetItem(mass,  ii));
            parlist[jj].state = (char)  PyLong_AsLong   (PyList_GetItem(state, ii));
            //printf("size mass state = %.3f, %.3f, %d \n\n", parlist[jj].size, parlist[jj].mass, parlist[jj].state);

            parlist[jj].sys = &psys[i];
            parlist[jj].collided_with = (int*) malloc(sizeof(int));
            parlist[jj].collided_num = 0;
            parlist[jj].links = (Links*) malloc(sizeof(Links));
            parlist[jj].links_num = 0;
            parlist[jj].links_activnum = 0;
            parlist[jj].link_with = (int*) malloc(sizeof(int));
            parlist[jj].link_withnum = 0;
            parlist[jj].neighboursmax = 10;
            parlist[jj].neighbours = (int*) malloc(parlist[jj].neighboursmax * sizeof(int));
            parlist[jj].neighboursnum = 0;
            jj += 1;
        }
    }

    jj = 0;
    kdtree = (KDTree*) malloc(sizeof(KDTree));
    KDTree_create_nodes(kdtree, parnum);

    for (i=0; i<parnum; i++) {
        parlistcopy[i].id = parlist[i].id;
        parlistcopy[i].loc[0] = parlist[i].loc[0];
        parlistcopy[i].loc[1] = parlist[i].loc[1];
        parlistcopy[i].loc[2] = parlist[i].loc[2];
    }

    KDTree_create_tree(kdtree, parlistcopy, 0, parnum - 1, 0, -1, 0, 1);

    for (i=0; i<kdtree->thread_index; i++) {
        KDTree_create_tree(
            kdtree,
            parlistcopy,
            kdtree->thread_start[i],
            kdtree->thread_end[i],
            kdtree->thread_name[i],
            kdtree->thread_parent[i],
            kdtree->thread_depth[i],
            0
        );
    }

    for (i=0; i<parnum; i++) {
        if (parlist[i].sys->links_active == 1) {
            KDTree_rnn_query(kdtree, &parlist[i], parlist[i].loc, parlist[i].sys->link_length);
        }
    }

    for (i=0; i<parnum; i++) {
        create_link(parlist[i].id, parlist[i].sys->link_max, 1, -1);

        if (parlist[i].neighboursnum > 1) {
            parlist[i].neighboursnum = 0;
        }

    }

    totallinks += newlinks;

    return PyLong_FromLong(parnum);
}
