import sys
from functools import lru_cache

def main():
    data = sys.stdin.read().split()
    A = [int(x) for x in data[:9]]
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    # state: tuple of 9 values: 0 white, 1 red (Takahashi), 2 blue (Aoki)
    # returns True if the player to move (color `me`) wins.
    @lru_cache(maxsize=None)
    def win(state, me):
        other = 3 - me
        opp_turn_color = other
        for i in range(9):
            if state[i] != 0:
                continue
            ns = list(state)
            ns[i] = me
            ok = any(all(ns[k] == me for k in ln) for ln in lines if i in ln)
            if ok:
                return True
            if 0 not in ns:
                # game over by score
                t = sum(A[k] for k in range(9) if ns[k] == 1)
                a = sum(A[k] for k in range(9) if ns[k] == 2)
                # mover wins if his total is higher
                mine = t if me == 1 else a
                theirs = a if me == 1 else t
                if mine > theirs:
                    return True
                continue
            if not win(tuple(ns), opp_turn_color):
                return True
        return False

    # Takahashi (color 1) moves first. Result is determined by win(initial, 1).
    if win((0,) * 9, 1):
        print("Takahashi")
    else:
        print("Aoki")

main()
