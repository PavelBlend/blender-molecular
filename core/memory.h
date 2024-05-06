static PyObject* memfree(PyObject *self, PyObject *args) {
    (void)self;  // Unused parameter for Python
    (void)args;  // Unused parameter for Python
    printf("=============> Free Memory Start");
    int i = 0;

    fps = 0;
    substep = 0;
    deltatime = 0;
    cpunum = 0;
    newlinks = 0;
    totallinks = 0;
    totaldeadlinks = 0;
    deadlinks = 0;

    for (i=0; i<parnum; i++) {
        if (parnum >= 1) {

            if (parlist[i].neighboursnum >= 1) {
                free(parlist[i].neighbours);
                parlist[i].neighbours = NULL;
                parlist[i].neighboursnum = 0;
            }

            if (parlist[i].collided_num >= 1) {
                free(parlist[i].collided_with);
                parlist[i].collided_with = NULL;
                parlist[i].collided_num = 0;
            }

            if (parlist[i].links_num >= 1) {
                free(parlist[i].links);
                parlist[i].links = NULL;
                parlist[i].links_num = 0;
                parlist[i].links_activnum = 0;
            }

            if (parlist[i].link_withnum >= 1) {
                free(parlist[i].link_with);
                parlist[i].link_with = NULL;
                parlist[i].link_withnum = 0;
            }

            if (parlist[i].neighboursnum >= 1) {
                free(parlist[i].neighbours);
                parlist[i].neighbours = NULL;
                parlist[i].neighboursnum = 0;
            }
        }
    }

    for (i=0; i<psysnum; i++) {
        if (psysnum >= 1) {
            psys[i].particles = NULL;
        }
    }

    free(par_id_list);

    if (psysnum >= 1) {
        free(psys);
        psys = NULL;
    }

    if (parnum >= 1) {
        free(parlistcopy);
        parlistcopy = NULL;
        free(parlist);
        parlist = NULL;
    }

    parnum = 0;
    psysnum = 0;

    if (kdtree->numnodes >= 1) {
        for (i=0; i<kdtree->numnodes; i++) {
            free(kdtree->nodes[i].particle);
            kdtree->nodes[i].particle = NULL;
            free(kdtree->nodes[i].left_child);
            kdtree->nodes[i].left_child = NULL;
            free(kdtree->nodes[i].right_child);
            kdtree->nodes[i].right_child = NULL;
        }

        free(kdtree->thread_nodes);
        kdtree->thread_nodes = NULL;
        free(kdtree->thread_start);
        kdtree->thread_start = NULL;
        free(kdtree->thread_end);
        kdtree->thread_end = NULL;
        free(kdtree->thread_name);
        kdtree->thread_name = NULL;
        free(kdtree->thread_parent);
        kdtree->thread_parent = NULL;
        free(kdtree->thread_depth);
        kdtree->thread_depth = NULL;
        free(kdtree->nodes);
        kdtree->nodes = NULL;
        free(kdtree->root_node);
        kdtree->root_node = NULL;
    }

    free(kdtree);
    kdtree = NULL;

    return PyLong_FromLong(0);
}

void* safe_malloc(size_t size, const char* var_name) {
    void* ptr = NULL;
    int attempts = 0;
    while (ptr == NULL && attempts < MAX_ATTEMPTS) {
        ptr = malloc(size);
        if (ptr) {
        return ptr;
        } else {
            attempts++;
            fprintf(stderr, "Memory allocation failed for %s after %d attempts\n", var_name, attempts);
            // Handle error here if needed
        }
    }
    fprintf(stderr, "Memory allocation failed for %s after %d attempts\n", var_name, attempts);
    return ptr;
}

int* safe_realloc(int* ptr, size_t size, const char* var_name) {
    int* new_ptr = NULL;
    int attempts = 0;
    while (attempts < MAX_ATTEMPTS) {
        new_ptr = (int*) realloc(ptr, size);

        if (new_ptr) {
            return new_ptr;
        } else {
            attempts++;
            fprintf(stderr, "Memory reallocation failed for %s after %d attempts\n", var_name, attempts);
            // Handle error here if needed
        }
    }

    fprintf(stderr, "Memory reallocation failed for %s after %d attempts\n", var_name, attempts);
    return NULL;
}

Links* safe_realloc_links(Links* ptr, size_t size, const char* var_name) {
    Links* temp = NULL;
    int attempts = 0;
    while (attempts < MAX_ATTEMPTS) {
        temp = (Links*) realloc(ptr, size);
        if (temp) {
            return temp;
        } else {
            attempts++;
            fprintf(stderr, "Memory reallocation failed for %s after %d attempts\n", var_name, attempts);
            // Handle error here if needed
        }
    }

    fprintf(stderr, "Memory reallocation failed for %s after %d attempts\n", var_name, attempts);
    return NULL;
}

// Function to allocate memory using calloc with retry
void* safe_calloc(size_t numElements, size_t elementSize, const char* var_name) {
    void* ptr = NULL;
    int attempts = 0;

    while (attempts < MAX_ATTEMPTS) {
        ptr = calloc(numElements, elementSize);
        if (ptr) {
            // Allocation succeeded
            return ptr;
        } else {
            // Allocation failed; retry
            attempts++;
            fprintf(stderr,"Memory allocation failed for %s after %d attempts\n", var_name, attempts);
        }
    }

    // Allocation still failed after maxAttempts
    fprintf(stderr,"Memory allocation failed for %s after %d attempts\n", var_name, attempts);
    return NULL;
}