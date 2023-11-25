typedef struct SParticle SParticle;
typedef struct ParSys ParSys;
typedef struct Node Node;
typedef struct KDTree KDTree;
typedef struct Links Links;
typedef struct Particle Particle;
typedef struct Pool Pool;
typedef struct Parity Parity;
typedef struct Heap Heap;



struct SParticle {
    int id;
    float loc[3];
};


struct Node {
    int index;
    int parent;

    float loc[3];

    char name;

    SParticle *particle;
    Node *left_child;
    Node *right_child;
};


struct KDTree {
    char axis[64];

    int numnodes;
    int thread_index;

    int *thread_nodes;
    int *thread_start;
    int *thread_end;
    int *thread_name;
    int *thread_parent;
    int *thread_depth;

    Node *root_node;
    Node *nodes;
};


struct Links {
    int start;
    int end;
    int exponent;
    int eexponent;

    float lenght;
    float stiffness;
    float damping;
    float broken;
    float estiffness;
    float edamping;
    float ebroken;
    float friction;
};


struct Particle {
    int id;
    int neighboursnum;
    int neighboursmax;
    int links_num;
    int links_activnum;
    int link_withnum;
    int collided_num;

    int *collided_with;
    int *link_with;
    int *neighbours;

    float loc[3];
    float vel[3];
    float size;
    float mass;

    ParSys *sys;
    Links *links;

    char state;
};


struct ParSys {
    int id;
    int parnum;
    int selfcollision_active;
    int othercollision_active;
    int collision_group;
    int links_active;
    int link_max;
    int relink_group;
    int relink_max;
    int link_group;
    int other_link_active;
    int use_link_tension_tex;
    int use_link_friction_tex;
    int use_link_stiff_tex;
    int use_link_estiff_tex;
    int use_link_damp_tex;
    int use_link_edamp_tex;
    int use_link_broken_tex;
    int use_link_ebroken_tex;
    int use_relink_tension_tex;
    int use_relink_friction_tex;
    int use_relink_stiff_tex;
    int use_relink_estiff_tex;
    int use_relink_damp_tex;
    int use_relink_edamp_tex;
    int use_relink_broken_tex;
    int use_relink_ebroken_tex;
    int use_relink_chance_tex;

    float friction;
    float collision_damp;
    float link_length;
    float link_tension;
    float link_tensionrand;
    float link_stiff;
    float link_stiffrand;
    float link_stiffexp;
    float link_damp;
    float link_damprand;
    float link_broken;
    float link_brokenrand;
    float link_estiff;
    float link_estiffrand;
    float link_estiffexp;
    float link_edamp;
    float link_edamprand;
    float link_ebroken;
    float link_ebrokenrand;
    float relink_chance;
    float relink_chancerand;
    float relink_tension;
    float relink_tensionrand;
    float relink_stiff;
    float relink_stiffexp;
    float relink_stiffrand;
    float relink_damp;
    float relink_damprand;
    float relink_broken;
    float relink_brokenrand;
    float relink_estiff;
    float relink_estiffexp;
    float relink_estiffrand;
    float relink_edamp;
    float relink_edamprand;
    float relink_ebroken;
    float relink_ebrokenrand;
    float link_friction;
    float link_frictionrand;

    float *link_tension_tex;
    float *link_friction_tex;
    float *link_stiff_tex;
    float *link_estiff_tex;
    float *link_damp_tex;
    float *link_edamp_tex;
    float *link_broken_tex;
    float *link_ebroken_tex;
    float *relink_tension_tex;
    float *relink_friction_tex;
    float *relink_stiff_tex;
    float *relink_estiff_tex;
    float *relink_damp_tex;
    float *relink_edamp_tex;
    float *relink_broken_tex;
    float *relink_ebroken_tex;
    float *relink_chance_tex;

    Particle *particles;
};


struct Pool {
    float offset;
    float max;
    char axis;
    Parity *parity;
};


struct Parity {
    Heap *heap;
};


struct Heap {
    int parnum;
    int maxalloc;
    int *par;
};
