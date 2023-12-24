#!/usr/bin/env python
import numpy as np
import re
import timeit
import sys


def parse_input(L):
    workflows = {}
    xmas_to_int = {"x": 0, "m": 1, "a": 2, "s": 3}

    for s in L:
        if s == "\n":
            break
        else:
            name, rules = re.match(r"(\w+){(.*)}", s).groups()
            workflow = []
            workflows[name] = workflow
            for rule in rules.split(","):
                if m := re.match(r"(\w)([<>])(\d+):(\w+)", rule):
                    var, op, val, next_workflow = m.groups()
                    var = xmas_to_int[var]
                    val = int(val)
                    workflow.append(((op, var, val), next_workflow))
                else:
                    workflow.append(("else", rule))
    return workflows


def count_part_combos(workflows, this_workflow, xmas):
    if this_workflow == "A":
        return np.prod(xmas[1, :] - xmas[0, :] + np.array([1, 1, 1, 1], dtype=np.int_))
    elif this_workflow == "R":
        return 0
    else:
        count = 0
        for rule, next_workflow in workflows[this_workflow]:
            if rule == "else":
                count += count_part_combos(workflows, next_workflow, xmas)
            else:
                op, var, val = rule
                if op == "<" and xmas[0, var] < val:
                    next_xmas = xmas.copy()
                    next_xmas[1, var] = min(next_xmas[1, var], val - 1)
                    count += count_part_combos(workflows, next_workflow, next_xmas)
                    xmas[0, var] = val
                elif op == ">" and xmas[1, var] > val:
                    next_xmas = xmas.copy()
                    next_xmas[0, var] = max(next_xmas[0, var], val + 1)
                    count += count_part_combos(workflows, next_workflow, next_xmas)
                    xmas[1, var] = val
                if xmas[0, var] > xmas[1, var]:
                    break
        return count


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    workflows = parse_input(L)
    xmas = np.array([[1, 1, 1, 1], [4000, 4000, 4000, 4000]], dtype=np.int_)
    print(count_part_combos(workflows, "in", xmas))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
