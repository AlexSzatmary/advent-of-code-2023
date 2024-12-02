#!/usr/bin/env python
from collections import Counter
import re
import sys
import timeit
import typing
from typing_extensions import Never

type Graph = dict[str, Counter[str]]
type Node = str
type Cabal = list[set[Node]]


def parse_input(L: list[str]) -> Graph:
    graph = {}
    for s in L:
        (node, *edges) = re.findall(r"\w+", s)
        graph[node] = Counter(edges)
    return graph


def make_undirected(graph: Graph) -> Graph:
    edges_to_add = []
    for node in graph:
        for edge in graph[node]:
            if edge not in graph:
                edges_to_add.append(edge)
    for node in edges_to_add:
        graph[node] = Counter()
    for node in graph:
        for edge in graph[node]:
            if node not in graph[edge]:
                graph[edge][node] += 1
    return graph


def merge_highly_connected(graph: Graph, cabals: Cabal) -> tuple[Graph, Cabal]:
    most_connected = 0
    best_pals = ("", "")
    a = list(graph.keys())[0]  # pick the 0th node and merge with its closest neighbor
    for b in graph[a]:
        k = (
            sum(min(graph[a][c], graph[b][c]) for c in graph[a] if c in graph[b])
            + graph[a][b]
        )
        if k > most_connected:
            best_pals = (a, b)
            most_connected = k

    (a, b) = best_pals
    for c in graph[b]:
        if c != a:
            graph[c][a] += graph[c].pop(b)
    graph[a] += graph[b]
    graph[a].pop(a)
    graph[a].pop(b)
    graph.pop(b)

    for i in range(len(cabals)):
        if b in cabals[i]:
            cabal_b = cabals.pop(i)
            break
    for cabal in cabals:
        if a in cabal:
            cabal.update(cabal_b)
            break

    return graph, cabals


def run_merge_highly_connected(graph: Graph) -> int:
    cabals = [set([node]) for node in graph]
    while len(cabals) > 2:
        graph, cabals = merge_highly_connected(graph, cabals)
        for node in graph:
            if graph[node].total() == 3:
                for cabal in cabals:
                    if node in cabal:
                        return len(cabal) * (sum(len(c) for c in cabals) - len(cabal))
                break
    assert False, "This should not execute"


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if argv[0] == "python":
        argv = argv[1:]
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    graph = make_undirected(parse_input(L))

    if len(argv) == 3 and argv[2] == "dot":
        print("graph {")
        for node, edges in graph.items():
            print(f"{node} -- {{{' '.join(map(str, edges))}}}")
        print("}")
        sys.exit()

    print(run_merge_highly_connected(graph))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
