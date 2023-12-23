#!/usr/bin/env python

import itertools
import numpy as np
import re
import sys
import timeit


def parse_input(L):
    digs = []
    int_to_direction = {"0": "R", "1": "D", "2": "L", "3": "U"}
    for s in L:
        m = re.match(r"(.) (\d+) \(#(.....)(.)", s)
        (_, _, dist, d) = m.groups()
        digs.append((int_to_direction[d], int(dist, 16), (0, 0, 0)))
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
    j_end -= top
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
        lagoon_outline[top : bottom + 1, left : right + 1] = 1
    return lagoon_outline


def display_lagoon_outline(lagoon_outline):
    for row in lagoon_outline:
        print("".join("#" if i else "." for i in row))


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
    print(np.array(list(dig[1] for dig in digs)))
    print(i_end)
    print(j_end)
    print("shoelace", shoelace(i_end, j_end))
    total_dig_length = sum(dig[1] for dig in digs)
    print("total dig length", total_dig_length)
    print("area", (abs(shoelace(i_end, j_end)) + total_dig_length) // 2 + 1)

    # lagoon_outline = make_lagoon_outline(i_start, j_start, i_end, j_end)
    # display_lagoon_outline(lagoon_outline)
    # print("---")
    # outside = find_outside_of_lagoon(lagoon_outline)
    # display_lagoon_outline(outside)
    # display_lagoon_outline(outside * lagoon_outline)
    # m, n = np.shape(lagoon_outline)
    # print(np.size(lagoon_outline) - np.sum(outside))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
