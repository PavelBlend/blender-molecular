#cython: profile=False
#cython: boundscheck=False
#cython: cdivision=True

cimport cython

from libc.stdlib cimport free, calloc
from libc.stdio cimport printf, fopen, fclose, FILE, snprintf
from libc.string cimport strlen, strcat


cdef struct DebugParticleSystem:
    float *link_friction
    float *link_tension
    float *link_stiffness
    float *link_estiffness
    float *link_damping
    float *link_edamping
    float *link_broken
    float *link_ebroken
    float *link_chance


cdef DebugParticleSystem *debug_particle_systems = NULL


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


cdef char* get_file_path(const char *file, const char *directory)nogil:
    cdef char* buff
    buff = <char *> calloc(strlen(directory) + strlen(file), 1)
    strcat(buff, file)
    strcat(buff, directory)
    return buff


cdef void open_debug_files(char *path)nogil:
    global link_friction_file
    global link_tension_file
    global link_stiffness_file
    global link_estiffness_file
    global link_damping_file
    global link_edamping_file
    global link_broken_file
    global link_ebroken_file
    global link_chance_file

    file_path = get_file_path(path, 'link_friction.bin')
    link_friction_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_tension.bin')
    link_tension_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_stiffness.bin')
    link_stiffness_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_estiffness.bin')
    link_estiffness_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_damping.bin')
    link_damping_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_edamping.bin')
    link_edamping_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_broken.bin')
    link_broken_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_ebroken.bin')
    link_ebroken_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_chance.bin')
    link_chance_file = fopen(file_path, 'wb')
    free(file_path)


cdef void close_debug_files()nogil:
    global link_friction_file
    global link_tension_file
    global link_stiffness_file
    global link_estiffness_file
    global link_damping_file
    global link_edamping_file
    global link_broken_file
    global link_ebroken_file
    global link_chance_file
    fclose(link_friction_file)
    fclose(link_tension_file)
    fclose(link_stiffness_file)
    fclose(link_estiffness_file)
    fclose(link_damping_file)
    fclose(link_edamping_file)
    fclose(link_broken_file)
    fclose(link_ebroken_file)
    fclose(link_chance_file)
