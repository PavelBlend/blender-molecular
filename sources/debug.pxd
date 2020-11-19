cimport cython

from libc.stdio cimport FILE


# debug files
cdef struct DebugFiles:
    FILE *link_friction_file
    FILE *link_tension_file
    FILE *link_stiffness_file
    FILE *link_estiffness_file
    FILE *link_damping_file
    FILE *link_edamping_file
    FILE *link_broken_file
    FILE *link_ebroken_file
    FILE *link_chance_file


cdef DebugFiles *debug_files
cdef void open_debug_files(char *path, int psys_id)nogil
cdef void close_debug_files(int psys_id)nogil
