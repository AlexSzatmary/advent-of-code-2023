#!/usr/bin/env python
import numpy as np
import re
import sys
import timeit
import z3


def parse_input(L):
    xs = np.zeros((len(L), 3), dtype=np.int_)
    vs = np.zeros((len(L), 3), dtype=np.int_)
    for i, s in enumerate(L):
        nums = list(map(int, re.findall(r"[-\d]+", s)))
        xs[i, :] = nums[:3]
        vs[i, :] = nums[3:]
    return xs, vs


# Not used in solution
# I think this is correct but don't know for sure why it doesn't converge with fsolve
def make_objective(xs, vs):
    def objective(vec):
        px0, py0, pz0, vx0, vy0, vz0, t1, t2, t3 = vec
        return np.array([
            px0 + vx0 * t1 - xs[0, 0] - vs[0, 0] * t1,
            py0 + vy0 * t1 - xs[0, 1] - vs[0, 1] * t1,
            pz0 + vz0 * t1 - xs[0, 2] - vs[0, 2] * t1,
            px0 + vx0 * t2 - xs[1, 0] - vs[1, 0] * t2,
            py0 + vy0 * t2 - xs[1, 1] - vs[1, 1] * t2,
            pz0 + vz0 * t2 - xs[1, 2] - vs[1, 2] * t2,
            px0 + vx0 * t3 - xs[2, 0] - vs[2, 0] * t3,
            py0 + vy0 * t3 - xs[2, 1] - vs[2, 1] * t3,
            pz0 + vz0 * t3 - xs[2, 2] - vs[2, 2] * t3,
        ])

    def jac(vec):
        px0, py0, pz0, vx0, vy0, vz0, t1, t2, t3 = vec
        return np.array([
            [1, 0, 0, t1, 0, 0, vx0 - vs[0, 0], 0, 0],
            [0, 1, 0, 0, t1, 0, vx0 - vs[0, 1], 0, 0],
            [0, 0, 1, 0, 0, t1, vx0 - vs[0, 2], 0, 0],
            [1, 0, 0, t2, 0, 0, 0, vx0 - vs[1, 0], 0],
            [0, 1, 0, 0, t2, 0, 0, vy0 - vs[1, 1], 0],
            [0, 0, 1, 0, 0, t2, 0, vz0 - vs[1, 2], 0],
            [1, 0, 0, t3, 0, 0, 0, 0, vx0 - vs[2, 0]],
            [0, 1, 0, 0, t3, 0, 0, 0, vy0 - vs[2, 1]],
            [0, 0, 1, 0, 0, t3, 0, 0, vz0 - vs[2, 2]],
        ])
    return objective, jac


def make_z3_solver(xs, vs):
    px0 = z3.Int("px0")
    py0 = z3.Int("py0")
    pz0 = z3.Int("pz0")
    vx0 = z3.Int("vx0")
    vy0 = z3.Int("vy0")
    vz0 = z3.Int("vz0")
    t1 = z3.Int("t1")
    t2 = z3.Int("t2")
    t3 = z3.Int("t3")
    s = z3.Solver()
    s.add(px0 + vx0 * t1 - xs[0, 0] - vs[0, 0] * t1 == 0)
    s.add(py0 + vy0 * t1 - xs[0, 1] - vs[0, 1] * t1 == 0)
    s.add(pz0 + vz0 * t1 - xs[0, 2] - vs[0, 2] * t1 == 0)
    s.add(px0 + vx0 * t2 - xs[1, 0] - vs[1, 0] * t2 == 0)
    s.add(py0 + vy0 * t2 - xs[1, 1] - vs[1, 1] * t2 == 0)
    s.add(pz0 + vz0 * t2 - xs[1, 2] - vs[1, 2] * t2 == 0)
    s.add(px0 + vx0 * t3 - xs[2, 0] - vs[2, 0] * t3 == 0)
    s.add(py0 + vy0 * t3 - xs[2, 1] - vs[2, 1] * t3 == 0)
    s.add(pz0 + vz0 * t3 - xs[2, 2] - vs[2, 2] * t3 == 0)
    s.check()
    m = s.model()
    return m[px0].as_long() + m[py0].as_long() + m[pz0].as_long()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    xs, vs = parse_input(L)
    print(make_z3_solver(xs, vs))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
