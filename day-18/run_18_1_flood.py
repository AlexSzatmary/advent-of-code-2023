#!/usr/bin/env python

# In this version, I kept a lot of dead code because I had tried a solution with flood
# fill that didn't work out; then, when I checked Reddit, it seemed that that solution
# would scale poorly in part 2; I'd like to fix the flood fill solution later.

import itertools
import numpy as np
import re
import sys
import timeit


def parse_input(L):
    digs = []
    for s in L:
        m = re.match(r"(.) (\d+) \(#(..)(..)(..)", s)
        (d, dist, r, g, b) = m.groups()
        digs.append((d, int(dist), (r, g, b)))
    return digs


def make_digs_absolute(digs):
    i_start = np.zeros(len(digs), dtype=np.int_)
    j_start = np.zeros(len(digs), dtype=np.int_)
    i_end = np.zeros(len(digs), dtype=np.int_)
    j_end = np.zeros(len(digs), dtype=np.int_)
    colors = []
    i = 0
    j = 0
    for k, (d, dist, color) in enumerate(digs):
        match d:
            case "R":
                i_start[k] = i
                j_start[k] = j + 1
                i_end[k] = i
                j_end[k] = j + dist
            case "U":
                i_start[k] = i - 1
                j_start[k] = j
                i_end[k] = i - dist
                j_end[k] = j
            case "L":
                i_start[k] = i
                j_start[k] = j - 1
                i_end[k] = i
                j_end[k] = j - dist
            case "D":
                i_start[k] = i + 1
                j_start[k] = j
                i_end[k] = i + dist
                j_end[k] = j
        i = i_end[k]
        j = j_end[k]
        colors.append(color)
    i_start[0] = j_start[0] = 0

    # register
    top = min(np.min(i_start), np.min(i_end))
    left = min(np.min(j_start), np.min(j_end))
    i_start -= top
    j_start -= left
    i_end -= top
    j_end -= left
    return i_start, j_start, i_end, j_end, colors


def make_lagoon_outline(i_start, j_start, i_end, j_end):
    m = max(np.max(i_start), np.max(i_end)) + 1
    n = max(np.max(j_start), np.max(j_end)) + 1
    lagoon_outline = np.zeros((m, n), dtype=np.int_)
    for k in range(np.size(i_start)):
        left = min(j_start[k], j_end[k])
        right = max(j_start[k], j_end[k])
        top = min(i_start[k], i_end[k])
        bottom = max(i_start[k], i_end[k])
        # print(left, right, top, bottom)
        lagoon_outline[top : bottom + 1, left : right + 1] = 1
    return lagoon_outline


def display_lagoon_outline(lagoon_outline):
    for row in lagoon_outline:
        print("".join("#" if i else "." for i in row))


def display_lagoon_outline_and_outside(lagoon_outline, outside):
    m, n = np.shape(lagoon_outline)
    for i in range(m):
        s = ""
        for j in range(n):
            if lagoon_outline[i, j] and outside[i, j]:
                s += "X"
            elif lagoon_outline[i, j]:
                s += "*"
            elif outside[i, j]:
                s += "."
            else:
                s += " "
        print(s)


def find_outside_of_lagoon(lagoon_outline):
    m, n = np.shape(lagoon_outline)
    outside = np.zeros((m, n), dtype=np.int_)
    edges = [
        (i, j)
        for i, j in itertools.chain(
            ((i, 0) for i in range(m)),
            ((i, n - 1) for i in range(m)),
            ((0, j) for j in range(n)),
            ((m - 1, j) for j in range(n)),
        )
        if not lagoon_outline[i, j]
    ]
    while edges:
        i, j = edges.pop()
        if not lagoon_outline[i, j] and not outside[i, j]:
            outside[i, j] = 1
            for di, dj in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
                if 0 <= i + di < m and 0 <= j + dj < n:
                    if (
                        not lagoon_outline[i + di, j + dj]
                        and not outside[i + di, j + dj]
                    ):
                        edges.append((i + di, j + dj))
    return outside


def shoelace(i_end, j_end):
    """Gives twice shoelace-calculated area because that is an integer"""
    return (
        np.sum(i_end[0:-1] * j_end[1:] - i_end[1:] * j_end[0:-1])
        + i_end[-1] * j_end[0]
        - i_end[0] * j_end[-1]
    )


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    digs = parse_input(L)
    i_start, j_start, i_end, j_end, colors = make_digs_absolute(digs)

    lagoon_outline = make_lagoon_outline(i_start, j_start, i_end, j_end)
    outside = find_outside_of_lagoon(lagoon_outline)
    display_lagoon_outline_and_outside(lagoon_outline, outside)
    print("area", np.size(lagoon_outline) - np.sum(outside))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
