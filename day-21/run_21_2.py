#!/usr/bin/env python
import math
import numpy as np
import timeit
import sys


def parse_input(L):
    field = np.zeros((len(L), len(L[0]) - 1), dtype=np.int_)
    for i, s in enumerate(L):
        if (j := s.find("S")) != -1:
            starti = i
            startj = j
            s = s.replace("S", "0")
        field[i, :] = np.array(
            list(s[:-1].replace(".", "0").replace("#", "1")), dtype=np.int_
        )
    return starti, startj, field


def walk(starti, startj, field, n):
    """
    Takes a starting position in a field, walks n steps, and returns an array where
    each value is the first step at which that vield could have been entered and 0 if
    not entered.
    """
    walked = -np.ones(np.shape(field), dtype=np.int_)
    walked[starti, startj] = 0
    open_field = 1 - field[1:-1, 1:-1]
    for k in range(n):
        # neighbors = max(
        #     [
        #         walked[0:-2, 1:-1]
        #         | walked[2:, 1:-1]
        #         | walked[1:-1, 0:-2]
        #         | walked[1:-1, 2:]
        #     ]
        # )
        neighbors = np.max(
            np.array(
                [
                    walked[0:-2, 1:-1],
                    walked[2:, 1:-1],
                    walked[1:-1, 0:-2],
                    walked[1:-1, 2:],
                ]
            ),
            axis=0,
        )

        # Keep data from past iterations and add cells that had been unwalked, are open
        # fields, and have neighbors that were seen previously
        walked[1:-1, 1:-1] = walked[1:-1, 1:-1] + (
            (walked[1:-1, 1:-1] == -1) & open_field & (neighbors >= 0)
        ) * (neighbors + 2)
    return walked


def print_field_and_walked(field, walked, steps_end):
    for i in range(len(field)):
        print(
            "".join(
                "."
                if f
                else ("O" if (w % 2 == steps_end % 2) & (0 <= w <= steps_end) else " ")
                for f, w in zip(field[i, :], walked[i, :])
            )
        )


def embiggen(starti, startj, field, factor):
    repeats = factor * 2 - 1
    nr, nc = np.shape(field)
    starti += (factor - 1) * nr
    startj += (factor - 1) * nc
    big_field = np.tile(field, (repeats, repeats))
    return starti, startj, big_field


def count_shapes(original_width, walked, step):
    """
    Takes the original shape (unembiggened), a walked array, and the step for cycle 2.

    Returns a dict of possible end points for the walk of length step in tiles of
    various shapes.

    A cycle 2 result would have this shape:
     J^L
    JAOBL <OEO> 7CODF
     7VF
    """
    tiles = np.size(walked, 0) // original_width
    w = original_width
    center = (tiles + 1) // 2
    shape_indices = {
        "E": (0, 0),
        "O": (0, 1),
        ">": (0, 2),
        "<": (0, -2),
        "^": (-2, 0),
        "V": (2, 0),
        "A": (-1, -1),
        "B": (-1, 1),
        "C": (1, -1),
        "D": (1, 1),
        "J": (-2, -1),
        "L": (-2, 1),
        "7": (2, -1),
        "F": (2, 1),
    }
    shape_counts = {}

    def count(a, step):
        return np.sum((a % 2 == step % 2) & (a <= step) & (a > -1))

    for shape in shape_indices:
        I, J = shape_indices[shape]
        shape_counts[shape] = count(
            walked[
                (center - 1 + I) * w : (center + I) * w,
                (center - 1 + J) * w : (center + J) * w,
            ],
            step,
        )
    return shape_counts


def predict_steps(shape_counts, cycle):
    """
    Predict number of steps at a given cycle based on how many steps would be taken in
    each shape type.
    """
    number_of_each_shape = {
        "E": (cycle - 1) ** 2,
        "O": cycle**2,
        ">": 1,
        "<": 1,
        "^": 1,
        "V": 1,
        "A": cycle - 1,
        "B": cycle - 1,
        "C": cycle - 1,
        "D": cycle - 1,
        "J": cycle,
        "L": cycle,
        "7": cycle,
        "F": cycle,
    }
    steps = [
        shape_counts[shape] * number_of_each_shape[shape] for shape in shape_counts
    ]
    return sum(steps)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    starti, startj, field = parse_input(L)
    cycles = [0, 1, 2]
    query_steps = [65 + c * 131 for c in cycles]
    steps_end = query_steps[-1]
    factor = (
        math.ceil((steps_end + (np.size(field, 0) + 1) / 2) / np.size(field, 0)) + 1
    )
    starti, startj, field = embiggen(starti, startj, field, factor)
    walked = walk(starti, startj, field, steps_end)
    shape_counts = count_shapes(131, walked, query_steps[2])
    n = 26501365
    big_cycles = (n - 65) // 131
    print(predict_steps(shape_counts, big_cycles))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
