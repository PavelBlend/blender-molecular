int substep = 0;
int parnum = 0;
int psysnum = 0;
int cpunum = 0;
int newlinks = 0;
int totallinks = 0;
int totaldeadlinks = 0;
int deadlinks = 0;

float fps = 0;
float deltatime = 0;
float RANDOM_MAX = 32767.0f;

int INITIAL_CAPACITY = 2;
int INITIAL_WITH_CAPACITY = 2;

int MAX_ATTEMPTS = 4;

int *par_id_list = NULL;

Particle *parlist = NULL;
SParticle *parlistcopy = NULL;
ParSys *psys = NULL;
KDTree *kdtree = NULL;
Octree  *octree = NULL;