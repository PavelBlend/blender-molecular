cdef struct Links:
    float lenght
    int start
    int end
    float stiffness
    int exponent
    float damping
    float broken
    float estiffness
    int eexponent
    float edamping
    float ebroken
    float friction


cdef struct KDTree:
    int numnodes
    # int num_result
    # int *result
    Node *root_node
    Node *nodes
    char axis[64]
    int thread_index
    int *thread_nodes
    int *thread_start
    int *thread_end
    int *thread_name
    int *thread_parent
    int *thread_depth


cdef struct Node:
    int index
    char name
    int parent
    float loc[3] 
    SParticle *particle
    Node *left_child
    Node *right_child


cdef struct ParSys:
    int id
    int parnum
    Particle *particles
    int selfcollision_active
    int othercollision_active
    int collision_group
    float friction
    float collision_damp
    int links_active
    float link_length
    int link_max
    float link_tension
    float link_tensionrand
    float link_stiff
    float link_stiffrand
    float link_stiffexp
    float link_damp
    float link_damprand
    float link_broken
    float link_brokenrand
    float link_estiff
    float link_estiffrand
    float link_estiffexp
    float link_edamp
    float link_edamprand
    float link_ebroken
    float link_ebrokenrand
    int relink_group
    float relink_chance
    float relink_chancerand
    int relink_max
    float relink_tension
    float relink_tensionrand
    float relink_stiff
    float relink_stiffexp
    float relink_stiffrand
    float relink_damp
    float relink_damprand
    float relink_broken
    float relink_brokenrand
    float relink_estiff
    float relink_estiffexp
    float relink_estiffrand
    float relink_edamp
    float relink_edamprand
    float relink_ebroken
    float relink_ebrokenrand
    float link_friction
    int link_group
    int other_link_active

    # textures params

    # link tension
    int use_link_tension_tex
    float *link_tension_tex
    # link friction
    int use_link_friction_tex
    float *link_friction_tex
    # link stiffness
    int use_link_stiff_tex
    float *link_stiff_tex
    int use_link_estiff_tex
    float *link_estiff_tex
    # link damping
    int use_link_damp_tex
    float *link_damp_tex
    int use_link_edamp_tex
    float *link_edamp_tex
    # link broken
    int use_link_broken_tex
    float *link_broken_tex
    int use_link_ebroken_tex
    float *link_ebroken_tex

    # relink tension
    int use_relink_tension_tex
    float *relink_tension_tex
    # relink friction
    int use_relink_friction_tex
    float *relink_friction_tex
    # relink stiffness
    int use_relink_stiff_tex
    float *relink_stiff_tex
    int use_relink_estiff_tex
    float *relink_estiff_tex
    # relink damping
    int use_relink_damp_tex
    float *relink_damp_tex
    int use_relink_edamp_tex
    float *relink_edamp_tex
    # relink broken
    int use_relink_broken_tex
    float *relink_broken_tex
    int use_relink_ebroken_tex
    float *relink_ebroken_tex
    # relink chance
    int use_relink_chance_tex
    float *relink_chance_tex


cdef struct SParticle:
    int id
    float loc[3]


cdef struct Particle:
    int id
    float loc[3]
    float vel[3]
    float size
    float mass
    char state
    ParSys *sys
    int *collided_with
    int collided_num
    Links *links
    int links_num
    int links_activnum
    int *link_with
    int link_withnum
    int *neighbours
    int neighboursnum
    int neighboursmax


cdef struct Pool:
    char axis
    float offset
    float max
    Parity *parity


cdef struct Parity:
    Heap *heap


cdef struct Heap:
    int *par
    int parnum
    int maxalloc
