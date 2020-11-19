cimport cython

from libc.stdio cimport FILE


# debug files
cdef FILE *link_friction_file
cdef FILE *link_tension_file
cdef FILE *link_stiffness_file
cdef FILE *link_estiffness_file
cdef FILE *link_damping_file
cdef FILE *link_edamping_file
cdef FILE *link_broken_file
cdef FILE *link_ebroken_file
cdef FILE *link_chance_file

cdef void open_debug_files(char *path)nogil
cdef void close_debug_files()nogil
