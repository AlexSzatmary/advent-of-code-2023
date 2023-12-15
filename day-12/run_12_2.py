#!/usr/bin/env python
# from itertools import cycle
import re
import sys


def parse_input(L):
    rows = []
    for s in L:
        row, groups = s.split(" ")
        row = row * 5
        groups = ",".join(groups for i in range(5))
        rows.append((row, list(map(int, groups.split(",")))))
    return rows


def pattern_from_groups(groups):
    return (
        r"^([.?]*?)"
        + r"[.?]+".join(r"[#?]{" + str(i) + "}" for i in groups)
        + r"[^#]*$"
    )


def count_arrangements(row, groups):
    # breakpoint()
    if not groups:
        return 1
    m = re.match(pattern_from_groups(groups), row)
    if m:
        start = len(m.group(1))
        dig = count_arrangements(row[start + groups[0] + 1 :], groups[1:])
        if row[start].startswith("?"):
            scan = count_arrangements(row[len(m.group(1)) + 1 :], groups)
        else:
            scan = 0
        return dig + scan
    else:
        return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    rows = parse_input(L)
    print([count_arrangements(row, groups) for row, groups in rows])
    print(sum(count_arrangements(row, groups) for row, groups in rows))


if __name__ == "__main__":
    sys.exit(main())
