#cython: profile=False
#cython: boundscheck=False
#cython: cdivision=True

# NOTE: order of slow fonction to be optimize/multithreaded:
# kdtreesearching, kdtreecreating, linksolving


print("cmolcore imported with success! v1.12")


cimport cython
from cython.parallel import prange, threadid
from libc.stdlib cimport malloc, free, realloc, calloc, rand, abs
from libc.string cimport memcpy, memset
from libc.stdio cimport printf, fopen, fwrite, fclose, FILE, snprintf
from libc.string cimport strlen, strcat
from time import perf_counter as clock


cdef extern from *:
    int INT_MAX
    float FLT_MAX


cdef extern from "stdlib.h":
    ctypedef void const_void "const void"
    void qsort(
        void *base,
        int nmemb,
        int size,
        int(*compar)(const_void *, const_void *)
    )nogil


#include types
#include data
#include utils
#include memory
#include mol_math
#include kd_tree
#include collide
#include test
#include debug
#include link
#include init
#include simulation
