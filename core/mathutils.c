float dot_product(float u[3], float v[3]) {
    return (float)fabs(u[0]*v[0] + u[1]*v[1] + u[2]*v[2]);
}


float square_dist(float point1[3], float point2[3], int k) {
    float sq_dist = 0;

    for (int i=0; i<k; i++) {
        sq_dist += (point1[i] - point2[i]) * (point1[i] - point2[i]);
    }

    return (float)fabs(sq_dist);
}


float average_value(float value_1, float value_2) {
    return (float)fabs((value_1 + value_2) / 2);
}
