#!/usr/bin/env python
import numpy as np
import re
import sys
import timeit


def parse_input(L):
    xs = np.zeros((len(L), 3), dtype=np.int_)
    vs = np.zeros((len(L), 3), dtype=np.int_)
    for i, s in enumerate(L):
        nums = list(map(int, re.findall(r"[-\d]+", s)))
        xs[i, :] = nums[:3]
        vs[i, :] = nums[3:]
    return xs, vs


def check_collisions(xs, vs, test_min, test_max):
    intersections = 0
    n = np.size(xs, 0)
    # xi + vxi * ti = xj + vxj * tj
    # yi + vyi * ti = yj + vyj * tj
    # so
    # vxi * ti - vxj * tj = xj - xi
    # vyi * ti - vyj * tj = yj - yi
    # multiply x equation by vyi, multiply y equation by vxi, then subtract scaled x
    # from y equation:
    # (-vyj * vxi - vyi * (-vxj)) * tj = vxi * (yj - yi) - vyi * (xj - xi)
    # tj = (vxi * (yj - yi) - vyi * (xj - xi)) / (-vyj * vxi + vyi * vxj)
    for i in range(n - 1):
        for j in range(i + 1, n):
            xi, yi = xs[i, :2]
            xj, yj = xs[j, :2]
            vxi, vyi = vs[i, :2]
            vxj, vyj = vs[j, :2]
            denominator = vyi * vxj - vxi * vyj
            if denominator:
                tj = (vxi * (yj - yi) - vyi * (xj - xi)) / denominator
                ti = (xj - xi + vxj * tj) / vxi
                # simple back-substitution, does not work if vxi = 0
                if ti > 0 and tj > 0:
                    if (
                        test_min <= xi + vxi * ti <= test_max
                        and test_min <= yi + vyi * ti <= test_max
                    ):
                        intersections += 1
            else:
                pass
            # Parallel trajectories. Probably no intersection unless the vectors are
            # inline, and the problem statement is not clear on how to handle that.
    return intersections


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    xs, vs = parse_input(L)
    # test_min = 7
    # test_max = 27
    test_min = 200000000000000
    test_max = 400000000000000
    print(check_collisions(xs, vs, test_min, test_max))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
