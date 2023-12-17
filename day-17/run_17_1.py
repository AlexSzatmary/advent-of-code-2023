#!/usr/bin/env python
# from itertools import cycle
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path
import timeit
import sys


def parse_input(L):
    return np.array([[int(c) for c in s[:-1]] for s in L])


def make_1D_index(city):
    m, n = np.shape(city)
    # direction 0 means entered NS (can leave EW). 1 means entered EW (can leave NS).
    return lambda i, j, direction: i + j * n + direction * m * n


def make_graph(city):
    m, n = np.shape(city)
    k = make_1D_index(city)
    # graph = csr_matrix((2 * m * n, 2 * m * n), dtype=city.dtype)
    graph = np.zeros((2 * m * n, 2 * m * n), dtype=city.dtype)

    # We could go in either direction at the start
    graph[k(0, 0, 1), k(0, 0, 0)] = 0
    graph[k(0, 0, 0), k(0, 0, 1)] = 0

    # make north-south connections
    for j in range(n):
        for far in [1, 2, 3]:
            for i in range(0, m - far):
                graph[k(i, j, 1), k(i + far, j, 0)] = np.sum(
                    city[i + 1 : i + far + 1, j]
                )
                graph[k(i + far, j, 1), k(i, j, 0)] = np.sum(city[i : i + far, j])

    # make east-west connections
    for i in range(m):
        for far in [1, 2, 3]:
            for j in range(0, n - far):
                graph[k(i, j, 0), k(i, j + far, 1)] = np.sum(
                    city[i, j + 1 : j + far + 1]
                )
                graph[k(i, j + far, 0), k(i, j, 1)] = np.sum(city[i, j : j + far])

    return csr_matrix(graph)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()

    start = timeit.default_timer()
    city = parse_input(L)

    m, n = np.shape(city)
    k = make_1D_index(city)

    graph = make_graph(city)
    print("Graph made")
    dist_matrix = shortest_path(graph, method="D", indices=k(0, 0, 0))
    print("Shortest path found")

    print(dist_matrix)
    # print(
    #     min(
    #         dist_matrix[k(0, 0, 0), k(m - 1, n - 1, 0)],
    #         dist_matrix[k(0, 0, 0), k(m - 1, n - 1, 1)],
    #     )
    # )
    print(
        min(
            dist_matrix[k(m - 1, n - 1, 0)],
            dist_matrix[k(m - 1, n - 1, 1)],
        )
    )
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
