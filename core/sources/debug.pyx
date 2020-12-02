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


cdef char* get_file_path(const char *file, const char *directory)nogil:
    cdef char* buff
    buff = <char *> calloc(strlen(directory) + strlen(file), 1)
    strcat(buff, file)
    strcat(buff, directory)
    return buff


cdef void open_debug_files(char *path, int psys_id)nogil:
    #PROFILER_START_NOGIL
    global debug_files

    file_path = get_file_path(path, 'link_friction.bin')
    debug_files[psys_id].link_friction_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_tension.bin')
    debug_files[psys_id].link_tension_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_stiffness.bin')
    debug_files[psys_id].link_stiffness_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_estiffness.bin')
    debug_files[psys_id].link_estiffness_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_damping.bin')
    debug_files[psys_id].link_damping_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_edamping.bin')
    debug_files[psys_id].link_edamping_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_broken.bin')
    debug_files[psys_id].link_broken_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_ebroken.bin')
    debug_files[psys_id].link_ebroken_file = fopen(file_path, 'wb')
    free(file_path)

    file_path = get_file_path(path, 'link_chance.bin')
    debug_files[psys_id].link_chance_file = fopen(file_path, 'wb')
    free(file_path)
    #PROFILER_END_NOGIL


cdef void close_debug_files(int psys_count)nogil:
    #PROFILER_START_NOGIL
    global debug_files
    cdef int psys_id
    for psys_id in xrange(psys_count):
        fclose(debug_files[psys_id].link_friction_file)
        fclose(debug_files[psys_id].link_tension_file)
        fclose(debug_files[psys_id].link_stiffness_file)
        fclose(debug_files[psys_id].link_estiffness_file)
        fclose(debug_files[psys_id].link_damping_file)
        fclose(debug_files[psys_id].link_edamping_file)
        fclose(debug_files[psys_id].link_broken_file)
        fclose(debug_files[psys_id].link_ebroken_file)
        fclose(debug_files[psys_id].link_chance_file)
    #PROFILER_END_NOGIL
