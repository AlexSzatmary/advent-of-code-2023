#!/usr/bin/env python
# from itertools import cycle
import re
import numpy as np
import sys

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
PIPES = ["|NS", "-EW", "LEN", "JWN", "FSE", "7SW"]
INOUT = {"E": "W", "W": "E", "N": "S", "S": "N"}
DIRECTIONS = {}
for pipe in PIPES:
    DIRECTIONS[(pipe[0], INOUT[pipe[1]])] = pipe[2]
    DIRECTIONS[(pipe[0], INOUT[pipe[2]])] = pipe[1]


def find_S(L):
    row = [i for i, s in enumerate(L) if "S" in s][0]
    col = L[row].find("S")
    return row, col


def crawl(L, row, col, d):
    d_start = d
    row_start = row
    col_start = col
    nr = len(L)
    nc = len(L[0])
    loop = np.zeros((nr, nc), dtype=np.int8)
    dist = 0
    loop[row, col] = 1
    while dist < nr * nc:  # generous halting condition
        match d:
            case "E":
                col += 1
                if col > nc:
                    return False
            case "N":
                row -= 1
                if row < 0:
                    return False
            case "W":
                col -= 1
                if col < 0:
                    return False
            case "S":
                row += 1
                if row > nr:
                    return False
        dist += 1
        new_spot = L[row][col]
        loop[row, col] = 1
        if new_spot == "S":
            d_end = INOUT[d]
            for pipe in PIPES:
                if (d_start == pipe[1] and d_end == pipe[2]) or (
                    d_start == pipe[2] and d_end == pipe[1]
                ):
                    new_S = pipe[0]
                    s = L[row_start]
                    L[row_start] = s[:col_start] + new_S + s[col_start + 1 :]
            return loop
        if (new_spot, d) in DIRECTIONS:
            d = DIRECTIONS[(new_spot, d)]
        else:
            return False


def clean(L, loop):
    L_clean = []
    for row, s in enumerate(L):
        L_clean.append(
            "".join([c if loop[row, col] else " " for col, c in enumerate(s)])
        )
    return L_clean


def process(L):
    row, col = find_S(L)
    for d in "ENW":
        loop = crawl(L, row, col, d)
        if loop is not False:
            break
    L_clean = clean(L, loop)
    area = sum([fsm(s) for s in L_clean])
    return area


def count_interior(L_clean):
    return sum(
        [
            sum(
                [
                    len(m.group(1))
                    for m in re.finditer(r"[^J7|]*[J7|]( *)[^J7|]*[J7|] *", s)
                ]
            )
            for s in L_clean
        ]
    )


def fsm(s):
    inside = False
    count = 0
    for c in s:
        match c:
            case " ":
                count += inside
            case "|":
                inside = not inside
            case "L":
                start = "L"
            case "F":
                start = "F"
            case "7":
                if start == "L":
                    inside = not inside
            case "J":
                if start == "F":
                    inside = not inside
            case "-":
                pass
    return count


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    print(process(L))


if __name__ == "__main__":
    sys.exit(main())
