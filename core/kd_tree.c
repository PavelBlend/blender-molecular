void KDTree_rnn_search(KDTree *kdtree, Particle *par, Node node, float point[3], float dist, float sqdist, int k, int depth) {

    int axis = 0;
    float realsqdist = 0;

    if (node.index == -1) {
        return;
    }

    SParticle tparticle = node.particle[0];

    axis = kdtree->axis[depth];

    if ((fabs(point[axis] - tparticle.loc[axis])) <= dist) {
        realsqdist = square_dist(point, tparticle.loc, 3);

        if (realsqdist <= sqdist) {

            par->neighboursnum++;
            if (par->neighboursnum >= par->neighboursmax) {
                par->neighboursmax = par->neighboursmax * 2;
                par->neighbours = (int*) realloc(par->neighbours, par->neighboursmax * sizeof(int));
            }
            par->neighbours[par->neighboursnum-1] = node.particle[0].id;
        }

        KDTree_rnn_search(kdtree, &par[0], node.left_child[0], point, dist, sqdist, 3, depth + 1);
        KDTree_rnn_search(kdtree, &par[0], node.right_child[0], point, dist, sqdist, 3, depth + 1);
    }

    else {
        if (point[axis] <= tparticle.loc[axis]) {
            KDTree_rnn_search(kdtree, &par[0], node.left_child[0], point, dist, sqdist, 3, depth + 1);
        }

        if (point[axis] >= tparticle.loc[axis]) {
            KDTree_rnn_search(kdtree, &par[0], node.right_child[0], point, dist, sqdist, 3, depth + 1);
        }
    }

}


int KDTree_rnn_query(KDTree *kdtree, Particle *par, float point[3], float dist) {
    float sqdist = 0;
    par->neighboursnum = 0;
    par->neighbours[0] = -1;

    if (kdtree->root_node[0].index != kdtree->nodes[0].index) {
        par->neighbours[0] = -1;
        par->neighboursnum = 0;
        return -1;

    } else {
        sqdist = dist * dist;
        KDTree_rnn_search(kdtree, &par[0], kdtree->root_node[0], point, dist, sqdist, 3, 0);
    }

    return 0;
}


Node KDTree_create_tree(KDTree *kdtree, SParticle *kdparlist, int start, int end, int name, int parent, int depth, int initiate) {
    int index = 0;
    int len = end - start + 1;

    if (len <= 0) {
        return kdtree->nodes[kdtree->numnodes];
    }

    int axis;
    axis = kdtree->axis[depth];
    quick_sort(kdparlist + start, len, axis);

    int median = (start + end) / 2;

    if (depth == 0) {
        kdtree->thread_index = 0;
        index = 0;
    } else {
        index = parent * 2 + name;
    }

    if (index > kdtree->numnodes) {
        return kdtree->nodes[kdtree->numnodes];
    }

    kdtree->nodes[index].name = name;
    kdtree->nodes[index].parent = parent;

    if (len >= 1 && depth == 0) {
        kdtree->root_node[0] = kdtree->nodes[0];
    }

    kdtree->nodes[index].particle[0] = kdparlist[median];

    if (parnum > 127) {
        if (depth == 4 && initiate == 1) {
            kdtree->thread_nodes[kdtree->thread_index] = index;
            kdtree->thread_start[kdtree->thread_index] = start;
            kdtree->thread_end[kdtree->thread_index] = end;
            kdtree->thread_name[kdtree->thread_index] = name;
            kdtree->thread_parent[kdtree->thread_index] = parent;
            kdtree->thread_depth[kdtree->thread_index] = depth;
            kdtree->thread_index += 1;
            return kdtree->nodes[index];
        }
    }

    kdtree->nodes[index].left_child[0] = KDTree_create_tree(kdtree, kdparlist, start, median - 1, 1, index, depth + 1, initiate);
    kdtree->nodes[index].right_child[0] = KDTree_create_tree(kdtree, kdparlist, median + 1, end, 2, index, depth + 1, initiate);

    return kdtree->nodes[index];

}


void KDTree_create_nodes(KDTree *kdtree, int parnum) {
    int i = 2;

    while (i < parnum) {
        i *= 2;
    }

    kdtree->numnodes = i;
    kdtree->nodes = (Node*) malloc((kdtree->numnodes + 1) * sizeof(Node));
    kdtree->root_node = (Node*) malloc(sizeof(Node));

    for (int i=0; i<=kdtree->numnodes; i++) {
        kdtree->nodes[i].index = i;
        kdtree->nodes[i].name = -1;
        kdtree->nodes[i].parent = -1;

        kdtree->nodes[i].particle = (SParticle*) malloc(sizeof(SParticle));

        kdtree->nodes[i].left_child = (Node*) malloc(sizeof(Node));
        kdtree->nodes[i].right_child = (Node*) malloc(sizeof(Node));
        kdtree->nodes[i].left_child[0].index = -1;
        kdtree->nodes[i].right_child[0].index = -1;
    }

    kdtree->nodes[kdtree->numnodes].index = -1;

    kdtree->thread_nodes = (int*) malloc(128 * sizeof(int));
    kdtree->thread_start = (int*) malloc(128 * sizeof(int));
    kdtree->thread_end = (int*) malloc(128 * sizeof(int));
    kdtree->thread_name = (int*) malloc(128 * sizeof(int));
    kdtree->thread_parent = (int*) malloc(128 * sizeof(int));
    kdtree->thread_depth = (int*) malloc(128 * sizeof(int));

    for (int i=0; i<64; i++) {
        kdtree->axis[i] = i % 3;
    }

    return;
}
