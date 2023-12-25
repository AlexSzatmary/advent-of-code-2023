#!/usr/bin/env python
from collections import deque
import re
import sys
import timeit


class Module:
    def __init__(self, name, destinations) -> None:
        self.name = name
        self.destinations = destinations

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} {self.name} -> "
            f"{', '.join(self.destinations)}>"
        )

    def process(self, source, high):
        return []


class FlipFlop(Module):
    def __init__(self, name, destinations) -> None:
        super().__init__(name, destinations)
        self.on = False

    def process(self, source, high):
        if high:
            return []
        else:
            self.on = not self.on
            return [(self.name, self.on, d) for d in self.destinations]


class Conjunction(Module):
    def __init__(self, name, destinations) -> None:
        super().__init__(name, destinations)
        self.inputs = {}

    def process(self, source, high):
        self.inputs[source] = high
        out = not all(self.inputs.values())
        return [(self.name, out, d) for d in self.destinations]


class Broadcast(Module):
    def process(self, source, high):
        return [(self.name, high, d) for d in self.destinations]


def dispatch(modules):
    n_high = 0
    n_low = 0
    pulses = deque([("button", False, "broadcaster")])

    while pulses:
        # print(pulses.popleft())
        (source, high, destination) = pulses.popleft()
        print(f"{source} -{'high' if high else 'low'}-> {destination}")
        if high:
            n_high += 1
        else:
            n_low += 1
        pulses.extend(modules[destination].process(source, high))

    return n_low, n_high


module_symbols = {"%": FlipFlop, "&": Conjunction, "": Broadcast}


def parse_input(L):
    graph = {}
    modules = {}

    for s in L:
        (module_type, module_name, destinations) = re.match(
            r"^([%&]?)(\w+) -> (.*)", s[:-1]
        ).groups()
        graph[module_name] = destinations.split(", ")
        modules[module_name] = module_symbols[module_type](
            module_name, destinations.split(", ")
        )

    # add nodes that are outputs but are unlisted
    existing_destination_lists = list(graph.values())
    for destination_list in existing_destination_lists:
        for destination in destination_list:
            if destination not in modules:
                modules[destination] = Module(destination, [])
                graph[destination] = []

    for module_name, module in modules.items():
        for destination in module.destinations:
            if isinstance(modules[destination], Conjunction):
                modules[destination].inputs[module_name] = False
    return modules


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    modules = parse_input(L)
    print(modules)
    total_low = 0
    total_high = 0
    for k in range(1000):
        n_low, n_high = dispatch(modules)
        total_low += n_low
        total_high += n_high
    print("total_low * total_high  = ", total_low * total_high)
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
