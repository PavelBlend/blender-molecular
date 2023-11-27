#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <math.h>
#include <time.h>
#include <limits.h>
#include <stdlib.h>

#include "omp.h"

#include "types.c"
#include "global.c"
#include "utils.c"
#include "mathutils.c"
#include "memory.c"
#include "kd_tree.c"
#include "link.c"
#include "collide.c"
#include "init.c"
#include "update.c"
#include "sim.c"
#include "python_api.c"
