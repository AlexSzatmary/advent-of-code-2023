#!/usr/bin/env python
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
    nr = len(L)
    nc = len(L[0])
    dist = 0
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
        if new_spot == "S":
            return dist
        if (new_spot, d) in DIRECTIONS:
            d = DIRECTIONS[(new_spot, d)]
        else:
            return False


def predict(row):
    row = list(reversed(row))
    tableau = []
    tableau.append([row[i + 1] - row[i] for i in range(len(row) - 1)])
    while not all(x == 0 for x in tableau[-1]):
        r = tableau[-1]
        tableau.append([r[i + 1] - r[i] for i in range(len(r) - 1)])
    lower_end = 0
    for r in reversed(tableau):
        lower_end += r[-1]
    return row[-1] + lower_end


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    row, col = find_S(L)
    for d in "ENW":
        distance = crawl(L, row, col, d)
        if distance > 0:
            break
    print(distance // 2)


if __name__ == "__main__":
    sys.exit(main())
