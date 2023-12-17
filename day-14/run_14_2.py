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
    return np.array(squares, dtype=np.bool_), np.array(circles, dtype=np.bool_)


def drop_and_find_moment(squares, circles):
    m = np.size(squares, 0)
    moment = 0
    new_circles = np.zeros(np.shape(circles), dtype=np.bool_)
    for j in range(np.size(squares, 1)):
        locs = [-1] + list(np.nonzero(squares[:, j])[0]) + [m]
        for i in range(len(locs) - 1):
            n_circles = np.sum(circles[max(locs[i], 0) : locs[i + 1], j])
            moment += n_circles * (m - locs[i] - 1) - n_circles * (n_circles - 1) // 2
            new_circles[locs[i] + 1: locs[i] + 1 + n_circles, j] = 1
    return new_circles, moment


def drop(squares, circles):
    m = np.size(squares, 0)
    new_circles = np.zeros(np.shape(circles), dtype=np.bool_)
    for j in range(np.size(squares, 1)):
        locs = [-1] + list(np.nonzero(squares[:, j])[0]) + [m]
        for i in range(len(locs) - 1):
            n_circles = np.sum(circles[max(locs[i], 0) : locs[i + 1], j])
            new_circles[locs[i] + 1: locs[i] + 1 + n_circles, j] = 1
    return new_circles


def find_moment(circles):
    m = np.size(circles, 0)
    return np.sum(np.sum(circles, 1) * np.arange(m, 0, -1))


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    squares, circles = parse_input(L)
    L_squares = [np.rot90(squares, k=k) for k in [0, 3, 2, 1]]
    new_circles = circles
    d = {}
    for j in range(1000):
        for i in range(4):
            new_circles = drop(L_squares[i], new_circles)
            new_circles = np.rot90(new_circles, k=3)
        moment = find_moment(new_circles)
        h = hash(tuple(list(new_circles.flatten())))
        if h in d:
            offset = d[h][0]
            period = j - offset
            break
        else:
            d[h] = (j, moment)
    phase = (1_000_000_000 - 1 - offset) % period
    target_j = phase + offset
    for (j, moment) in d.values():
        if j == target_j:
            print(moment)
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
