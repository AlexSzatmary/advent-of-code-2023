#!/usr/bin/env python
# from itertools import cycle
import numpy as np
import timeit
import sys


def parse_input(L):
    return [s[:-1] for s in L]


def trace_rays(grid):
    rays = [(0, 0, "E")]
    n_r = len(grid)
    n_c = len(grid[0])
    # records of which spaces have been left in which directions
    left_E = np.zeros((n_r, n_c), dtype=np.bool_)
    left_N = np.zeros((n_r, n_c), dtype=np.bool_)
    left_W = np.zeros((n_r, n_c), dtype=np.bool_)
    left_S = np.zeros((n_r, n_c), dtype=np.bool_)
    left_arrays = {"E": left_E, "N": left_N, "W": left_W, "S": left_S}
    while rays:
        (i, j, d) = rays.pop()  # (row, column, direction)
        while True:
            # find next d; if a splitter, record direction not taken
            match grid[i][j]:
                case "|":
                    if d == "E" or d == "W":
                        rays.append((i, j, "S"))
                        d = "N"
                    # else keep going
                case "-":
                    if d == "N" or d == "S":
                        rays.append((i, j, "W"))
                        d = "E"
                    # else keep going
                case "/":
                    match d:
                        case "N": d = "E"
                        case "E": d = "N"
                        case "W": d = "S"
                        case "S": d = "W"
                case "\\":
                    match d:
                        case "N": d = "W"
                        case "E": d = "S"
                        case "W": d = "N"
                        case "S": d = "E"

                case ".":
                    pass

            # check whether this d has been taken yet; if so, break, else, record
            a = left_arrays[d]
            if a[i, j]:
                break
            else:
                a[i, j] = True

            # find new coordinate, check bounds and break if needed, else advance
            match d:
                case "E":
                    if j >= n_c - 1:
                        break
                    else:
                        j += 1
                case "N":
                    if i <= 0:
                        break
                    else:
                        i -= 1
                case "W":
                    if j <= 0:
                        break
                    else:
                        j -= 1
                case "S":
                    if i >= n_r - 1:
                        break
                    else:
                        i += 1

    return left_E, left_N, left_W, left_S


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    grid = parse_input(L)
    left_E, left_N, left_W, left_S = trace_rays(grid)
    energized = left_E | left_N | left_W | left_S
    print(np.sum(energized))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
