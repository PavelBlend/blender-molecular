// Thread-local storage for the random number state
// __declspec(thread) unsigned int rand_state;

void create_link(int par_id, int max_link, int parothers_id) {

    int ii = 0;
    int neighboursnum = 0;
    int create_links;

    int *neighbours = NULL;

    float link_friction_1 = 0.0;
    float link_friction_2 = 0.0;
    // float link_tension_1 = 0.0;
    // float link_tension_2 = 0.0;
    float link_stiff_1 = 0.0;
    float link_stiff_2 = 0.0;
    float link_estiff_1 = 0.0;
    float link_estiff_2 = 0.0;
    float link_damp_1 = 0.0;
    float link_damp_2 = 0.0;
    float link_edamp_1 = 0.0;
    float link_edamp_2 = 0.0;
    float link_broken_1 = 0.0;
    float link_broken_2 = 0.0;
    float link_ebroken_1 = 0.0;
    float link_ebroken_2 = 0.0;
    float relink_chance_1 = 0.0;
    float relink_chance_2 = 0.0;
    float relink_random = 0.0;
    float relink_stiff_1 = 0.0;
    float relink_stiff_2 = 0.0;
    float relink_estiff_1 = 0.0;
    float relink_estiff_2 = 0.0;
    float relink_damp_1 = 0.0;
    float relink_damp_2 = 0.0;
    float relink_edamp_1 = 0.0;
    float relink_edamp_2 = 0.0;
    float relink_broken_1 = 0.0;
    float relink_broken_2 = 0.0;
    float relink_ebroken_1 = 0.0;
    float relink_ebroken_2 = 0.0;

    Particle *par = NULL;
    Particle *par2 = NULL;
    Particle *fakepar = NULL;
    Links *link = (Links*) safe_malloc(sizeof(Links), "link");
    fakepar = (Particle*) safe_malloc(sizeof(Particle), "fakepar");

    par = &parlist[par_id];

    if (par->state >= 2) {
        return;
    }

    if (par->links_activnum >= max_link) {
        return;
    }

    if (par->sys->links_active == 0) {
        return;
    }

    if (parothers_id == -1) {
        neighbours = par->neighbours;
        neighboursnum = par->neighboursnum;

    } else {
        neighbours = (int*)safe_malloc(sizeof(int), "neighbours");
        neighbours[0] = parothers_id;
        neighboursnum = 1;
    }

    link->start = par->id;

    link_friction_1 = randomize_value(par->sys->link_friction, par->sys->link_frictionrand);
    link_stiff_1 = randomize_value(par->sys->link_stiff, par->sys->link_stiffrand);
    link_estiff_1 = randomize_value(par->sys->link_estiff, par->sys->link_estiffrand);
    link_damp_1 = randomize_value(par->sys->link_damp, par->sys->link_damprand);
    link_edamp_1 = randomize_value(par->sys->link_edamp, par->sys->link_edamprand);
    link_broken_1 = randomize_value(par->sys->link_broken, par->sys->link_brokenrand);
    link_ebroken_1 = randomize_value(par->sys->link_ebroken, par->sys->link_ebrokenrand);
    relink_chance_1 = randomize_value(par->sys->relink_chance, par->sys->relink_chancerand);
    relink_stiff_1 = randomize_value(par->sys->relink_stiff, par->sys->relink_stiffrand);
    relink_estiff_1 = randomize_value(par->sys->relink_estiff, par->sys->relink_estiffrand);
    relink_damp_1 = randomize_value(par->sys->relink_damp, par->sys->relink_damprand);
    relink_edamp_1 = randomize_value(par->sys->relink_edamp, par->sys->relink_edamprand);
    relink_broken_1 = randomize_value(par->sys->relink_broken, par->sys->relink_brokenrand);
    relink_ebroken_1 = randomize_value(par->sys->relink_ebroken, par->sys->relink_ebrokenrand);

    for (ii=0; ii<neighboursnum; ii++) {
        if (par->links_activnum >= max_link) {
            break;
        }

        if (parothers_id == -1) {
            par2 = &parlist[neighbours[ii]];
        } else {
            par2 = &parlist[neighbours[0]];
        }

        if (par->id != par2->id) {

            if (arraysearch(par->id,par2->link_with, par2->link_withnum) == -1 && par2->state <= 1 && par->state <= 1) {

                link->end = par2->id;

                link_friction_2 = randomize_value(par2->sys->link_friction, par2->sys->link_frictionrand);

                link->friction = average_value(link_friction_1, link_friction_2);

                if (parothers_id == -1 && par->sys->link_group == par2->sys->link_group) {

                    if (par->sys->id != par2->sys->id) {

                        if (par->sys->other_link_active && par2->sys->other_link_active) {
                            create_links = 1;
                        } else {
                            create_links = 0;
                        }

                    } else {
                        create_links = 1;
                    }

                    if (create_links == 1) {
                        link->lenght = (float)sqrt(square_dist(par->loc, par2->loc, 3));
                        link->stiffness = average_value(link_stiff_1, link_stiff_2);
                        link_estiff_2 = randomize_value(par2->sys->link_estiff, par2->sys->link_estiffrand);
                        link->estiffness = average_value(link_estiff_1, link_estiff_2);
                        link->exponent = (int)1.0;
                        link->eexponent = (int)1.0;
                        link_damp_2 = randomize_value(par2->sys->link_damp, par2->sys->link_damprand);
                        link->damping = average_value(link_damp_1, link_damp_2);
                        link_edamp_2 = randomize_value(par2->sys->link_edamp, par2->sys->link_edamprand);
                        link->edamping = average_value(link_edamp_1, link_edamp_2);
                        link_broken_2 = randomize_value(par2->sys->link_broken, par2->sys->link_brokenrand);
                        link->broken = average_value(link_broken_1, link_broken_2);
                        link_ebroken_2 = randomize_value(par2->sys->link_ebroken, par2->sys->link_ebrokenrand);
                        link->ebroken = average_value(link_ebroken_1, link_ebroken_2);

                        par->links[par->links_num] = link[0];
                        par->links_num += 1;
                        par->links_activnum += 1;
                        if (par->links_num >= par->links_capacity) {
                            par->links_capacity *= 2;  // Double the capacity
                            par->links = (Links*) safe_realloc_links(par->links, par->links_capacity * sizeof(Links), "par->links");
                        }

                        par->link_with[par->link_withnum] = par2->id;
                        par->link_withnum += 1;

                        if (par->link_withnum >= par->link_with_capacity) {
                            par->link_with_capacity *= 2;  // Double the capacity
                            par->link_with = (int*) safe_realloc(par->link_with, par->link_with_capacity * sizeof(int), "par->link_with");
                        }

                        par2->link_with[par2->link_withnum] = par->id;
                        par2->link_withnum += 1;

                        if (par2->link_withnum >= par2->link_with_capacity) {
                            par2->link_with_capacity *= 2;  // Double the capacity
                            par2->link_with = (int*) safe_realloc(par2->link_with, par2->link_with_capacity * sizeof(int), "par2->link_with");
                        }

                        newlinks += 1;
                    }
                }

                if (parothers_id != -1 && par->sys->relink_group == par2->sys->relink_group) {
                    relink_chance_2 = randomize_value(par2->sys->relink_chance, par2->sys->relink_chancerand);
                    relink_random = rand() / RANDOM_MAX;

                    if (relink_random <= average_value(relink_chance_1, relink_chance_2)) {
                        link->lenght = (float)sqrt(square_dist(par->loc, par2->loc, 3));
                        relink_stiff_2 = randomize_value(par2->sys->relink_stiff, par2->sys->relink_stiffrand);
                        relink_estiff_2 = randomize_value(par2->sys->relink_estiff, par2->sys->relink_estiffrand);
                        link->stiffness = average_value(relink_stiff_1, relink_stiff_2);
                        link->estiffness = average_value(relink_estiff_1, relink_estiff_2);
                        link->exponent = (int)1.0;
                        link->eexponent = (int)1.0;
                        relink_damp_2 = randomize_value(par2->sys->relink_damp, par2->sys->relink_damprand);
                        relink_edamp_2 = randomize_value(par2->sys->relink_edamp, par2->sys->relink_edamprand);
                        link->damping = average_value(relink_damp_1, relink_damp_2);
                        link->edamping = average_value(relink_edamp_1, relink_edamp_2);
                        relink_broken_2 = randomize_value(par2->sys->relink_broken, par2->sys->relink_brokenrand);
                        relink_ebroken_2 = randomize_value(par2->sys->relink_ebroken, par2->sys->relink_ebrokenrand);
                        link->broken = average_value(relink_broken_1, relink_broken_2);
                        link->ebroken = average_value(relink_ebroken_1, relink_ebroken_2);

                        par->links[par->links_num] = link[0];
                        par->links_num += 1;
                        par->links_activnum += 1;
                        if (par->links_num >= par->links_capacity) {
                            par->links_capacity *= 2;  // Double the capacity
                            par->links = (Links*) safe_realloc_links(par->links, par->links_capacity * sizeof(Links), "par->links");
                        }

                        par->link_with[par->link_withnum] = par2->id;
                        par->link_withnum += 1;

                        if (par->link_withnum >= par->link_with_capacity) {
                            par->link_with_capacity *= 2;  // Double the capacity
                            par->link_with = (int*) safe_realloc(par->link_with, par->link_with_capacity * sizeof(int),"par->link_with");
                        }

                        par2->link_with[par2->link_withnum] = par->id;
                        par2->link_withnum += 1;

                        if (par2->link_withnum >= par2->link_with_capacity) {
                            par2->link_with_capacity *= 2;  // Double the capacity
                            par2->link_with = (int*) safe_realloc(par2->link_with, par2->link_with_capacity * sizeof(int),"par2->link_with");
                        }

                        newlinks += 1;
                    }
                }
            }
        }
    }

    free(link);
    free(fakepar);

    if (parothers_id != -1) {
        free(neighbours);
    }

    return;
}


void solve_link(Particle *par) {
    int i = 0;
    int parsearch = 0;
    int par2search = 0;

    float stiff = 0;
    float damping = 0;
    float exp = 0;
    float Vx = 0;
    float Vy = 0;
    float Vz = 0;
    float V = 0;
    float ForceSpring = 0;
    float ForceDamper = 0;
    float ForceX = 0;
    float ForceY = 0;
    float ForceZ = 0;
    float ratio1 = 0;
    float ratio2 = 0;
    float factor1 = 0;
    float factor2 = 0;
    float friction1 = 0;
    float friction2 = 0;

    float Force1[3] = {0, 0, 0};
    float Force2[3] = {0, 0, 0};
    float normal1[3] = {0, 0, 0};
    float normal2[3] = {0, 0, 0};
    float ypar1_vel[3] = {0, 0, 0};
    float xpar1_vel[3] = {0, 0, 0};
    float ypar2_vel[3] = {0, 0, 0};
    float xpar2_vel[3] = {0, 0, 0};

    Particle *par1 = NULL;
    Particle *par2 = NULL;

    if (par->state >= 2) {
        return;
    }

    for (i=0; i<par->links_num; i++) {
        if (par->links[i].start != -1) {

            par1 = &parlist[par->links[i].start];
            par2 = &parlist[par->links[i].end];
            
            float Loc1[3] = {0, 0, 0}, Loc2[3] = {0, 0, 0}, V1[3] = {0, 0, 0}, V2[3] = {0, 0, 0};
            float LengthX = 0, LengthY = 0, LengthZ = 0, Length = 0;

            memcpy(Loc1, par1->loc, sizeof(Loc1));
            memcpy(Loc2, par2->loc, sizeof(Loc2));
            memcpy(V1, par1->vel, sizeof(V1));
            memcpy(V2, par2->vel, sizeof(V2));

            LengthX = Loc2[0] - Loc1[0];
            LengthY = Loc2[1] - Loc1[1];
            LengthZ = Loc2[2] - Loc1[2];
            Length = (float)sqrt(pow(LengthX, 2) + pow(LengthY, 2) + pow(LengthZ, 2));

            if (par->links[i].lenght != Length && Length != 0) {
                
                if (par->links[i].lenght > Length) {
                    stiff = par->links[i].stiffness * deltatime;
                    damping = par->links[i].damping;
                    exp = (float)par->links[i].exponent;
                } else if (par->links[i].lenght < Length) {
                    stiff = par->links[i].estiffness * deltatime;
                    damping = par->links[i].edamping;
                    exp = (float)par->links[i].eexponent;
                }

                Vx = V2[0] - V1[0];
                Vy = V2[1] - V1[1];
                Vz = V2[2] - V1[2];
                V = (Vx * LengthX + Vy * LengthY + Vz * LengthZ) / Length;
                ForceSpring = (float)pow((Length - par->links[i].lenght), exp) * stiff;
                ForceDamper = damping * V;
                float sum_force = ForceSpring + ForceDamper;
                float LengthRatioX = LengthX / Length;
                float LengthRatioY = LengthY / Length;
                float LengthRatioZ = LengthZ / Length;
                ForceX = (sum_force) * LengthRatioX;
                ForceY = (sum_force) * LengthRatioY;
                ForceZ = (sum_force) * LengthRatioZ;
                Force1[0] = ForceX;
                Force1[1] = ForceY;
                Force1[2] = ForceZ;
                Force2[0] = -ForceX;
                Force2[1] = -ForceY;
                Force2[2] = -ForceZ;
                float sum_mass = par1->mass + par2->mass;
                ratio1 = (par2->mass/(sum_mass));
                ratio2 = (par1->mass/(sum_mass));

                if (par1->state == 3) {    /* dead particle, correct velocity ratio of alive partner */
                    ratio1 = 0;
                    ratio2 = 1;
                } else if (par2->state == 3) {
                    ratio1 = 1;
                    ratio2 = 0;
                }

                for (int i = 0; i < 3; i++) {
                    par1->vel[i] += Force1[i] * ratio1;
                    par2->vel[i] += Force2[i] * ratio2;
                }

                normal1[0] = LengthRatioX;
                normal1[1] = LengthRatioY;
                normal1[2] = LengthRatioZ;
                normal2[0] = -LengthRatioX;
                normal2[1] = -LengthRatioY;
                normal2[2] = -LengthRatioZ;

                factor1 = dot_product(par1->vel, normal1);
                factor2 = dot_product(par2->vel, normal2);

                friction1 = 1 - ((par->links[i].friction) * ratio1);
                friction2 = 1 - ((par->links[i].friction) * ratio2);

                for (int i = 0; i < 3; i++) {
                    ypar1_vel[i] = factor1 * normal1[i];
                    xpar1_vel[i] = par1->vel[i] - ypar1_vel[i];
                    ypar2_vel[i] = factor2 * normal2[i];
                    xpar2_vel[i] = par2->vel[i] - ypar2_vel[i];

                    par1->vel[i] = ypar1_vel[i] + ((xpar1_vel[i] * friction1) + (xpar2_vel[i] * (1 - friction1)));
                    par2->vel[i] = ypar2_vel[i] + ((xpar2_vel[i] * friction2) + (xpar1_vel[i] * (1 - friction2)));
                }


                if (Length > (par->links[i].lenght * (1 + par->links[i].ebroken)) || Length < (par->links[i].lenght  * (1 - par->links[i].broken))) {

                    par->links[i].start = -1;
                    par->links_activnum -= 1;
                    deadlinks += 1;

                    parsearch = arraysearch(par2->id, par->link_with, par->link_withnum);

                    if (parsearch != -1) {
                        par->link_with[parsearch] = -1;
                    }

                    par2search = arraysearch(par->id, par2->link_with, par2->link_withnum);

                    if (par2search != -1) {
                        par2->link_with[par2search] = -1;
                    }
                }
            }
        }
    }
}
