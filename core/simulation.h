#ifndef SIMULATE_H
#define SIMULATE_H
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <math.h>
#include <time.h>
#include <limits.h>
#include <stdlib.h>

#include "omp.h"

#include "types.h"
#include "global.h"
#include "utils.h"
#include "mathutils.h"
#include "memory.h"
#include "kd_tree.h"
// #include "octree.c"
// #include "kdtree.h"
#include "link.h"
#include "collide.h"
#include "init.h"
#include "update.h"

static PyObject* simulate(PyObject *self, PyObject *args);
#endif 
#include "python_api.h"
