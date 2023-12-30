#!/usr/bin/env python
import numpy as np
import re
import timeit
import sys


def parse_input(L):
    blocks = np.zeros((len(L), 6), dtype=np.int_)
    for i, s in enumerate(L):
        blocks[i] = re.findall(r"\d+", s)
        # nice code for orienting but seems unnecessary
        for j in range(3):
            if blocks[i, j] > blocks[i, j + 3]:
                blocks[i, j], blocks[i, j + 3] = blocks[i, j + 3], blocks[i, j]
    blocks = blocks[blocks[:, 2].argsort()]
    return blocks


def drop_blocks(blocks):
    floor_size = (
        max(np.max(blocks[:, 0]), np.max(blocks[:, 3])) + 1,
        max(np.max(blocks[:, 1]), np.max(blocks[:, 4])) + 1,
    )
    top_heights = np.zeros(floor_size, dtype=np.int_)
    top_indices = -np.ones(floor_size, dtype=np.int_)
    do_not_disintegrate = np.zeros(np.size(blocks, 0), dtype=np.int_)
    for i, block in enumerate(blocks):
        x0, y0, z0, x1, y1, z1 = block
        # breakpoint()
        height = np.max(top_heights[x0 : x1 + 1, y0 : y1 + 1])
        blocks_below = np.unique(
            top_indices[x0 : x1 + 1, y0 : y1 + 1][
                top_heights[x0 : x1 + 1, y0 : y1 + 1] == height
            ]
        )
        if np.size(blocks_below) == 1 and blocks_below != -1:
            print(i, blocks_below)
            do_not_disintegrate[blocks_below] = 1
        top_indices[x0 : x1 + 1, y0 : y1 + 1] = i
        top_heights[x0 : x1 + 1, y0 : y1 + 1] = height + z1 + 1 - z0
    print(top_indices)
    print(top_heights)
    print(do_not_disintegrate)
    return np.size(blocks, 0) - np.sum(do_not_disintegrate)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    blocks = parse_input(L)
    print(drop_blocks(blocks))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
