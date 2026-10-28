import sys
from functools import lru_cache

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def main():
    data = sys.stdin.read().split()
    A = [int(x) for x in data[:9]]

    def has_line(board, color):
        for a, b, c in LINES:
            if board[a] == board[b] == board[c] == color:
                return True
        return False

    # board cell: 0 = white, 1 = red (Takahashi), 2 = blue (Aoki)
    # Returns the winner ('T' or 'A') under optimal play from this state.
    @lru_cache(maxsize=None)
    def solve(board, turn_red):
        color = 1 if turn_red else 2
        winner_if_line = 'T' if turn_red else 'A'
        loser = 'A' if turn_red else 'T'
        for i in range(9):
            if board[i] != 0:
                continue
            nb = list(board)
            nb[i] = color
            nb = tuple(nb)
            if has_line(nb, color):
                res = winner_if_line
            elif 0 not in nb:
                ts = sum(A[k] for k in range(9) if nb[k] == 1)
                as_ = sum(A[k] for k in range(9) if nb[k] == 2)
                res = 'T' if ts > as_ else 'A'
            else:
                res = solve(nb, not turn_red)
            if res == winner_if_line:
                return winner_if_line
        return loser

    w = solve(tuple([0] * 9), True)
    print("Takahashi" if w == "T" else "Aoki")


main()
