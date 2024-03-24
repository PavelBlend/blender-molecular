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

    float friction;
    float collision_damp;
    float link_length;
    float link_stiff;
    float link_stiffrand;
    float link_damp;
    float link_damprand;
    float link_broken;
    float link_brokenrand;
    float link_estiff;
    float link_estiffrand;
    float link_edamp;
    float link_edamprand;
    float link_ebroken;
    float link_ebrokenrand;
    float relink_chance;
    float relink_chancerand;
    float relink_stiff;
    float relink_stiffrand;
    float relink_damp;
    float relink_damprand;
    float relink_broken;
    float relink_brokenrand;
    float relink_estiff;
    float relink_estiffrand;
    float relink_edamp;
    float relink_edamprand;
    float relink_ebroken;
    float relink_ebrokenrand;
    float link_friction;
    float link_frictionrand;

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
