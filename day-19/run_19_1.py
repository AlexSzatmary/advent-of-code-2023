#!/usr/bin/env python
import operator
import re
import timeit
import sys


def parse_input(L):
    workflows = {}
    parts = []
    xmas_to_int = {"x": 0, "m": 1, "a": 2, "s": 3}

    def make_condition(op, var, val):
        return lambda xmas: op(xmas[var], val)

    done_parsing_workflows = False
    for s in L:
        if s == "\n":
            done_parsing_workflows = True
        elif not done_parsing_workflows:
            name, rules = re.match(r"(\w+){(.*)}", s).groups()
            workflow = []
            workflows[name] = workflow
            for rule in rules.split(","):
                if m := re.match(r"(\w)([<>])(\d+):(\w+)", rule):
                    var, op, val, next_workflow = m.groups()
                    var = xmas_to_int[var]
                    val = int(val)
                    if op == "<":
                        op = operator.lt
                    else:
                        op = operator.gt
                    condition = make_condition(op, var, val)
                    workflow.append((condition, next_workflow))
                else:
                    workflow.append((lambda xmas: True, rule))
        else:
            parts.append(tuple(map(int, re.findall(r"\d+", s))))
    return workflows, parts


def sort_parts(workflows, parts):
    accepted = []
    for part in parts:
        next_workflow = "in"
        while next_workflow != "A" and next_workflow != "R":
            for condition, next_workflow in workflows[next_workflow]:
                if condition(part):
                    break
        if next_workflow == "A":
            accepted.append(part)
    return accepted


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    workflows, parts = parse_input(L)
    accepted = sort_parts(workflows, parts)
    print(sum(sum(a) for a in accepted))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
