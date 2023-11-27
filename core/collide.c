void collide(Particle *par) {
    int i = 0;
    int check = 0;

    int *neighbours = NULL;

    float stiff = 0;
    float target = 0;
    float sqtarget = 0;
    float lenghtx = 0;
    float lenghty = 0;
    float lenghtz = 0;
    float sqlenght = 0;
    float lenght = 0;
    float invlenght = 0;
    float factor = 0;
    float ratio1 = 0;
    float ratio2 = 0;
    float factor1 = 0;
    float factor2 = 0;
    float friction1 = 0;
    float friction2 = 0;
    float damping1 = 0;
    float damping2 = 0;
    float force1 = 0;
    float force2 = 0;
    float mathtmp = 0;

    float col_normal1[3] = {0, 0, 0};
    float col_normal2[3] = {0, 0, 0};
    float ypar_vel[3] = {0, 0, 0};
    float xpar_vel[3] = {0, 0, 0};
    float yi_vel[3] = {0, 0, 0};
    float xi_vel[3] = {0, 0, 0};

    Particle *par2 = NULL;

    if (par->state >= 2) {
        return;
    }

    if (!par->sys->selfcollision_active && !par->sys->othercollision_active) {
        return;
    }

    neighbours = par->neighbours;

    for (i=0; i<par->neighboursnum; i++) {

        check = 0;

        if (parlist[i].id == -1) {
            check += 1;
        }

        par2 = &parlist[neighbours[i]];

        if (par->id == par2->id) {
            check += 10;
        }

        if (arraysearch(par2->id, par->collided_with, par->collided_num) == -1) {

            if (par2->sys->id != par->sys->id) {
                if (!par2->sys->othercollision_active || !par->sys->othercollision_active) {
                    check += 100;
                }
            }

            if (par2->sys->collision_group != par->sys->collision_group) {
                check += 1000;
            }

            if (par2->sys->id == par->sys->id && !par->sys->selfcollision_active) {
                check += 10000;
            }

            stiff = deltatime;
            target = (par->size + par2->size) * 0.999;
            sqtarget = target * target;

            if (check == 0 && par2->state <= 1 && arraysearch(par2->id, par->link_with, par->link_withnum) == -1 && arraysearch(par->id, par2->link_with, par2->link_withnum) == -1) {

                lenghtx = par->loc[0] - par2->loc[0];
                lenghty = par->loc[1] - par2->loc[1];
                lenghtz = par->loc[2] - par2->loc[2];

                sqlenght = square_dist(par->loc, par2->loc, 3);

                if (sqlenght != 0 && sqlenght < sqtarget) {
                    lenght = pow(sqlenght, 0.5);
                    invlenght = 1 / lenght;
                    factor = (lenght - target) * invlenght;
                    ratio1 = par2->mass / (par->mass + par2->mass);
                    ratio2 = 1 - ratio1;

                    mathtmp = factor * stiff;

                    force1 = ratio1 * mathtmp;
                    force2 = ratio2 * mathtmp;

                    par->vel[0] -= lenghtx * force1;
                    par->vel[1] -= lenghty * force1;
                    par->vel[2] -= lenghtz * force1;

                    par2->vel[0] += lenghtx * force2;
                    par2->vel[1] += lenghty * force2;
                    par2->vel[2] += lenghtz * force2;

                    col_normal1[0] = (par2->loc[0] - par->loc[0]) * invlenght;
                    col_normal1[1] = (par2->loc[1] - par->loc[1]) * invlenght;
                    col_normal1[2] = (par2->loc[2] - par->loc[2]) * invlenght;

                    col_normal2[0] = col_normal1[0] * -1;
                    col_normal2[1] = col_normal1[1] * -1;
                    col_normal2[2] = col_normal1[2] * -1;

                    factor1 = dot_product(par->vel, col_normal1);

                    ypar_vel[0] = factor1 * col_normal1[0];
                    ypar_vel[1] = factor1 * col_normal1[1];
                    ypar_vel[2] = factor1 * col_normal1[2];

                    xpar_vel[0] = par->vel[0] - ypar_vel[0];
                    xpar_vel[1] = par->vel[1] - ypar_vel[1];
                    xpar_vel[2] = par->vel[2] - ypar_vel[2];

                    factor2 = dot_product(par2->vel, col_normal2);

                    yi_vel[0] = factor2 * col_normal2[0];
                    yi_vel[1] = factor2 * col_normal2[1];
                    yi_vel[2] = factor2 * col_normal2[2];

                    xi_vel[0] = par2->vel[0] - yi_vel[0];
                    xi_vel[1] = par2->vel[1] - yi_vel[1];
                    xi_vel[2] = par2->vel[2] - yi_vel[2];

                    friction1 = 1 - ((par->sys->friction + par2->sys->friction) * 0.5) * ratio1;
                    friction2 = 1 - ((par->sys->friction + par2->sys->friction) * 0.5) * ratio2;

                    damping1 = 1 - ((par->sys->collision_damp + par2->sys->collision_damp) * 0.5) * ratio1;
                    damping2 = 1 - ((par->sys->collision_damp + par2->sys->collision_damp) * 0.5) * ratio2;

                    par->vel[0] = ((ypar_vel[0] * damping1) + (yi_vel[0] * (1 - damping1))) + ((xpar_vel[0] * friction1) + (xi_vel[0] * (1 - friction1)));
                    par->vel[1] = ((ypar_vel[1] * damping1) + (yi_vel[1] * (1 - damping1))) + ((xpar_vel[1] * friction1) + (xi_vel[1] * (1 - friction1)));
                    par->vel[2] = ((ypar_vel[2] * damping1) + (yi_vel[2] * (1 - damping1))) + ((xpar_vel[2] * friction1) + (xi_vel[2] * (1 - friction1)));

                    par2->vel[0] = ((yi_vel[0] * damping2) + (ypar_vel[0] * (1 - damping2))) + ((xi_vel[0] * friction2) + ( xpar_vel[0] * (1 - friction2)));
                    par2->vel[1] = ((yi_vel[1] * damping2) + (ypar_vel[1] * (1 - damping2))) + ((xi_vel[1] * friction2) + ( xpar_vel[1] * (1 - friction2)));
                    par2->vel[2] = ((yi_vel[2] * damping2) + (ypar_vel[2] * (1 - damping2))) + ((xi_vel[2] * friction2) + ( xpar_vel[2] * (1 - friction2)));

                    par2->collided_with[par2->collided_num] = par->id;
                    par2->collided_num += 1;
                    par2->collided_with = (int*) realloc(par2->collided_with, (par2->collided_num + 1) * sizeof(int));

                    if (((par->sys->relink_chance + par2->sys->relink_chance) / 2) > 0) {
                        create_link(par->id, par->sys->link_max * 2, 0, par2->id);
                    }
                }
            }
        }
    }
}
