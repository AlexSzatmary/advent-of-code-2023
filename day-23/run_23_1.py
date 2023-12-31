#!/usr/bin/env python
import numpy as np
import timeit
import sys

DIRECTION = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def parse_input(L):
    forest = np.zeros((len(L) + 2, len(L[0]) - 1), dtype=np.int_)
    for i, s in enumerate(L, start=1):
        for j, c in enumerate(s[:-1]):
            # print(i, j)
            match c:
                case "#":
                    forest[i, j] = 0
                case ".":
                    forest[i, j] = 1
                case ">":
                    forest[i, j] = 10
                case "^":
                    forest[i, j] = 11
                case "<":
                    forest[i, j] = 12
                case "v":
                    forest[i, j] = 13
    return forest


def wander(forest, i, j, d, graph):
    n_steps = 0
    while True:
        for k in range(1, -2, -1):
            # breakpoint()
            if (np.array([i + 2, j + 2]) == np.shape(forest)).all():
                return [i, j, d, n_steps]  # the end
            d_new = (d + k) % 4
            di, dj = DIRECTION[d_new]
            next_space = forest[i + di, j + dj]
            if next_space:
                if next_space == 1:
                    i += di
                    j += dj
                    d = d_new
                    n_steps += 1
                    break
                elif next_space - 10 == (d_new + 2) % 4:  # cannot go uphill
                    continue
                else:  # we found a node
                    i += 2 * di
                    j += 2 * dj
                    d = d_new
                    n_steps += 2
                    process_node(forest, i, j, graph)
                    return [i, j, d, n_steps]
            else:
                continue
        else:
            return "infinity"


def process_node(forest, i, j, graph):
    if (i, j) in graph:
        return None  # already visited
    graph[(i, j)] = []
    for k in range(4):
        d_new = k
        di, dj = DIRECTION[d_new]
        next_space = forest[i + di, j + dj]
        if next_space:
            if next_space == 1:
                new_path = wander(forest, i + di, j + dj, d_new, graph)
                if new_path != "infinity":
                    new_path[-1] += 1
                    graph[(i, j)].append(new_path)
            elif next_space - 10 == (d_new + 2) % 4:  # cannot go uphill
                continue
            else:  # going downhill
                new_path = wander(forest, i + 2 * di, j + 2 * dj, d_new, graph)
                if new_path != "infinity":
                    new_path[-1] += 2
                    graph[(i, j)].append(new_path)
    return None  # none because graph is the real output


def longest_path(forest, i, j, graph, costs):
    if (np.array([i + 2, j + 2]) == np.shape(forest)).all():
        costs[i, j] = 0
    else:
        costs[i, j] = 0
        for node in graph[i, j]:
            i2, j2, _, cost = node
            if (i2, j2) not in costs:
                longest_path(forest, i2, j2, graph, costs)
            costs[i, j] = max(costs[i, j], costs[i2, j2] + cost)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    forest = parse_input(L)
    graph = {}
    process_node(forest, 1, 1, graph)
    costs = {}
    longest_path(forest, 1, 1, graph, costs)
    print(costs[1, 1])
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
