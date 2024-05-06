float randomize_value(float value, float random) {
    if (random == 0 || random == 1) {
        // Handle the case where random is 0 or 1 (e.g., return value, return a default value, etc.)
        return value;
    } else {
        return value * (1.0f + (((float)rand() / RANDOM_MAX) * random) - (random / 2));
    }
}


void quick_sort(SParticle *a, int n, int axis) {
    if (n < 2)
        return;

    SParticle t;
    float p = a[n / 2].loc[axis];
    SParticle *l = a;
    SParticle *r = a + n - 1;

    while (l <= r) {
        if (l[0].loc[axis] < p) {
            l += 1;
            continue;
        }

        if (r[0].loc[axis] > p) {
            r -= 1;
            /*
            we need to check the condition (l <= r) every time
            we change the value of l or r
            */
            continue;
        }

        t = l[0];
        l[0] = r[0];
        /*
        suggested by stephan to remove temp variable t but slower
        l[0], r[0] = r[0], l[0]
        */
        l += 1;
        r[0] = t;
        r -= 1;
    }

    quick_sort(a, (int)(r - a + 1), axis);
    quick_sort(l, (int)(a + n - l), axis);
}


int arraysearch(int element, int *array, int len) {

    for (int i=0; i<len; i++) {
        if (element == array[i]) {
            return i;
        }
    }

    return -1;
}
