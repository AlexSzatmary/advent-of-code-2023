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
    fallen_blocks = blocks
    floor_size = (
        max(np.max(blocks[:, 0]), np.max(blocks[:, 3])) + 1,
        max(np.max(blocks[:, 1]), np.max(blocks[:, 4])) + 1,
    )
    top_heights = np.zeros(floor_size, dtype=np.int_)
    top_indices = -np.ones(floor_size, dtype=np.int_)
    do_not_disintegrate = np.zeros(np.size(blocks, 0), dtype=np.int_)
    blocks_below = []
    for i, block in enumerate(blocks):
        x0, y0, z0, x1, y1, z1 = block
        # breakpoint()
        height = np.max(top_heights[x0 : x1 + 1, y0 : y1 + 1])
        blocks_below.append(
            np.unique(
                top_indices[x0 : x1 + 1, y0 : y1 + 1][
                    top_heights[x0 : x1 + 1, y0 : y1 + 1] == height
                ]
            )
        )
        if np.size(blocks_below[-1]) == 1 and blocks_below[-1] != -1:
            do_not_disintegrate[blocks_below[-1]] = 1
        top_indices[x0 : x1 + 1, y0 : y1 + 1] = i
        top_heights[x0 : x1 + 1, y0 : y1 + 1] = height + z1 + 1 - z0
        fallen_blocks[i, 5] = height + z1 - z0
        # z1 had been the bottom of the top cube; coordinate 5 is now the top of the top
        # cube
        fallen_blocks[i, 2] = height
    return fallen_blocks, blocks_below


def count_chain_reaction_fall(fallen_blocks, blocks_below):
    return sum(
        count_chain_reaction_fall_helper(fallen_blocks, blocks_below, j)
        for j in range(np.size(fallen_blocks, 0))
    )


def count_chain_reaction_fall_helper(fallen_blocks, blocks_below, j):
    shaky = -np.ones(np.size(fallen_blocks, 0), dtype=np.int_)
    # -1 is not yet checked (should never be seen, I think), 0 is safe, 1 is will fall.
    shaky[0:j] = 0  # blocks at or below the level of this block cannot be shaken
    shaky[j] = 1
    # the algorithm below relies on this being set here; the problem statement does not
    # include j in its own count so that's accounted for in the return.
    for k in range(j+1, np.size(fallen_blocks, 0)):
        # if j == 5:
        #     print(k, shaky, blocks_below[k], shaky[blocks_below[j]])
        if fallen_blocks[k, 2] <= fallen_blocks[j, 5]:
            shaky[k] = 0
        else:
            if all(shaky[blocks_below[k]]):
                shaky[k] = 1
            else:
                shaky[k] = 0
    return np.sum(shaky) - 1  # -1 so we don't count j in its own count


def main(argv=None):
    if argv is None:
        argv = sys.argv
    with open(argv[1], "r") as hin:
        L = hin.readlines()
    start = timeit.default_timer()
    blocks = parse_input(L)
    fallen_blocks, blocks_below = drop_blocks(blocks)
    print(count_chain_reaction_fall(fallen_blocks, blocks_below))
    stop = timeit.default_timer()
    print("Time:", stop - start)


if __name__ == "__main__":
    sys.exit(main())
