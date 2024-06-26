static PyObject* init(PyObject *self, PyObject *args) {

    PyObject* importdata;

    int parse_result = PyArg_ParseTuple(args, "O", &importdata);
    if (!parse_result) {
        printf("Error while parsing init function parameters!\n");
        return NULL;
    }

    int is_list = PyList_Check(importdata);
    if (!is_list) {
        printf("Function parameter is not a list!\n");
        return NULL;
    }

    PyObject* sim_settings = PyList_GetItem(importdata, 0);
    is_list = PyList_Check(sim_settings);
    if (!is_list) {
        printf("First element of the importdata is not a list!\n");
        return NULL;
    }

    int i = 0;
    int ii = 0;
    int jj = 0;

    newlinks = 0;
    totallinks = 0;
    totaldeadlinks = 0;

    fps = (float)PyFloat_AsDouble(PyList_GetItem(sim_settings, 0));
    substep = (int)PyLong_AsLongLong(PyList_GetItem(sim_settings, 1));
    psysnum = (int)PyLong_AsLongLong(PyList_GetItem(sim_settings, 2));
    parnum = (int)PyLong_AsLongLong(PyList_GetItem(sim_settings, 3));
    cpunum = (int)PyLong_AsLongLong(PyList_GetItem(sim_settings, 4));

    omp_set_num_threads(cpunum);
    omp_set_max_active_levels(1);

    deltatime = fps * (float)(substep);

    psys = (ParSys*)safe_malloc(psysnum * sizeof(ParSys), "psys");
    parlist = (Particle*)safe_malloc(parnum * sizeof(Particle), "parlist");
    parlistcopy = (SParticle*)safe_malloc(parnum * sizeof(SParticle), "parlistcopy");
    par_id_list = (int*)safe_malloc(parnum * sizeof(int), "par_id_list");


    for (i=0; i<psysnum; i++) {

        PyObject* psys_props = PyList_GetItem(importdata, i+1);

        psys[i].id = i;
        psys[i].parnum = (int)PyLong_AsLongLong(PyList_GetItem(psys_props, 0));
        psys[i].particles = (Particle*)safe_malloc(psys[i].parnum * sizeof(Particle), "psys[i].particles");
        psys[i].particles = &parlist[jj];

        PyObject* psys_settings = PyList_GetItem(psys_props, 6);

        psys[i].selfcollision_active    = (int)PyLong_AsLongLong(PyList_GetItem(psys_settings,  0));
        psys[i].othercollision_active   = (int)PyLong_AsLongLong(PyList_GetItem(psys_settings,  1));
        psys[i].collision_group         = (int)PyLong_AsLongLong(PyList_GetItem(psys_settings,  2));
        psys[i].friction                = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings,  3));
        psys[i].collision_damp          = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings,  4));

        psys[i].links_active            = (int)PyLong_AsLongLong(PyList_GetItem(psys_settings,  5));
        psys[i].other_link_active       = (int)PyLong_AsLongLong(PyList_GetItem(psys_settings,  6));
        psys[i].link_group              = (int)PyLong_AsLongLong(PyList_GetItem(psys_settings,  7));
        psys[i].link_friction           = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings,  8));
        psys[i].link_frictionrand       = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings,  9));
        psys[i].link_max                = (int)PyLong_AsLongLong(PyList_GetItem(psys_settings, 10));
        psys[i].link_length             = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 11));

        psys[i].link_stiff              = (float)(PyFloat_AsDouble(PyList_GetItem(psys_settings, 12)) * 0.5);
        psys[i].link_stiffrand          = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 13));
        psys[i].link_estiff             = (float)(PyFloat_AsDouble(PyList_GetItem(psys_settings, 14)) * 0.5);
        psys[i].link_estiffrand         = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 15));

        psys[i].link_damp               = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 16));
        psys[i].link_damprand           = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 17));
        psys[i].link_edamp              = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 18));
        psys[i].link_edamprand          = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 19));


        psys[i].link_broken             = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 20));
        psys[i].link_brokenrand         = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 21));
        psys[i].link_ebroken            = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 22));
        psys[i].link_ebrokenrand        = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 23));

        psys[i].relink_group            = (int)PyLong_AsLongLong(PyList_GetItem(psys_settings, 24));
        psys[i].relink_chance           = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 25));
        psys[i].relink_chancerand       = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 26));
        psys[i].relink_max              = (int)PyLong_AsLongLong(PyList_GetItem(psys_settings, 27));

        psys[i].relink_stiff            = (float)(PyFloat_AsDouble(PyList_GetItem(psys_settings, 28)) * 0.5);
        psys[i].relink_stiffrand        = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 29));
        psys[i].relink_estiff           = (float)(PyFloat_AsDouble(PyList_GetItem(psys_settings, 30)) * 0.5);
        psys[i].relink_estiffrand       = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 31));

        psys[i].relink_damp             = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 32));
        psys[i].relink_damprand         = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 33));
        psys[i].relink_edamp            = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 34));
        psys[i].relink_edamprand        = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 35));

        psys[i].relink_broken           = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 36));
        psys[i].relink_brokenrand       = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 37));
        psys[i].relink_ebroken          = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 38));
        psys[i].relink_ebrokenrand      = (float)PyFloat_AsDouble(PyList_GetItem(psys_settings, 39));

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

            parlist[jj].vel[0] = (float)PyFloat_AsDouble(PyList_GetItem(velocity, ii*3));
            parlist[jj].vel[1] = (float)PyFloat_AsDouble(PyList_GetItem(velocity, ii*3 + 1));
            parlist[jj].vel[2] = (float)PyFloat_AsDouble(PyList_GetItem(velocity, ii*3 + 2));

            parlist[jj].size  = (float) PyFloat_AsDouble(PyList_GetItem(size,  ii));
            parlist[jj].mass  = (float) PyFloat_AsDouble(PyList_GetItem(mass,  ii));
            parlist[jj].state = (char)  PyLong_AsLong   (PyList_GetItem(state, ii));

            parlist[jj].sys = &psys[i];

            parlist[jj].collided_with = (int*)safe_malloc(sizeof(int), "parlist[jj].collided_with");
            parlist[jj].collided_num = 0;

            parlist[jj].links_capacity = INITIAL_CAPACITY;
            parlist[jj].links = (Links*)safe_malloc(parlist[jj].links_capacity * sizeof(Links), "parlist[jj].links");
            parlist[jj].links_num = 0;

            parlist[jj].links_activnum = 0;

            parlist[jj].link_with_capacity = INITIAL_WITH_CAPACITY;
            parlist[jj].link_with = (int*)safe_malloc(parlist[jj].link_with_capacity * sizeof(int), "parlist[jj].link_with");
            parlist[jj].link_withnum = 0;

            parlist[jj].neighboursmax = 10;

            parlist[jj].neighbours = (int*)safe_malloc(parlist[jj].neighboursmax * sizeof(int), "parlist[jj].neighbours");
            parlist[jj].neighboursnum = 0;

            jj += 1;
        }
    }

    jj = 0;

    kdtree = (KDTree*)safe_malloc(sizeof(KDTree), "kdtree");
    KDTree_create_nodes(kdtree, parnum);

    #pragma omp parallel
    {
        int i;
        #pragma omp for schedule(dynamic, 10)
        for (i=0; i<parnum; i++) {
            parlistcopy[i].id = parlist[i].id;
            memcpy(parlistcopy[i].loc, parlist[i].loc, sizeof(parlist[i].loc));
        }
    }

    KDTree_create_tree(kdtree, parlistcopy, 0, parnum - 1, 0, -1, 0, 1);

    #pragma omp parallel
    {
        int i;
        #pragma omp for schedule(dynamic, 10)
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
    }

    #pragma omp parallel
    {
        int i;
        #pragma omp for schedule(dynamic, 10)
        for (i=0; i<parnum; i++) {
            if (parlist[i].sys->links_active == 1) {
                KDTree_rnn_query(kdtree, &parlist[i], parlist[i].loc, parlist[i].sys->link_length);
            }
        }
    }

    for (i=0; i<parnum; i++) {
        create_link(parlist[i].id, parlist[i].sys->link_max, -1);

        if (parlist[i].neighboursnum > 1) {
            parlist[i].neighboursnum = 0;
        }

    }

    totallinks += newlinks;

    return PyLong_FromLong(parnum);
}
