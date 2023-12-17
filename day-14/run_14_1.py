#!/usr/bin/env python
import numpy as np
import timeit
import sys


def parse_input(L):
    squares = []
    circles = []
    for s in L:
        squares.append([1 if c == "#" else 0 for c in s[:-1]])
        circles.append([1 if c == "O" else 0 for c in s[:-1]])
    return np.array(squares), np.array(circles)


def find_moment(squares, circles):
    m = np.size(squares, 0)
    moment = 0
    for j in range(np.size(squares, 1)):
        locs = [-1] + list(np.nonzero(squares[:, j])[0]) + [m]
        for i in range(len(locs) - 1):
            n_circles = np.sum(circles[max(locs[i], 0) : locs[i + 1], j])
            moment += n_circles * (m - locs[i] - 1) - n_circles * (n_circles - 1) // 2
    return moment


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    squares, circles = parse_input(L)
    print(find_moment(squares, circles))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
