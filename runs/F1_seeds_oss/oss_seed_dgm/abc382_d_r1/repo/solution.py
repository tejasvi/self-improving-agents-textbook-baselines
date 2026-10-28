"""Solution for Keep Distance problem.

Given integers N and M, we need to enumerate all integer sequences A_1..A_N such that:
  * 1 <= A_i
  * A_{i} - A_{i-1} >= 10 for i >= 2
  * A_N <= M
The sequences must be printed in lexicographical order, together with the total count.

Constraints are small (N <= 12, M is at most 10*N), which means the search space is tiny – the difference between the minimal possible last element
    min_last = 1 + 10*(N-1) = 10*N - 9
and the maximal allowed M is at most 9. Therefore a simple depth‑first search with pruning suffices.

The DFS chooses the current element A_i within the feasible range:
    lo = max(1, prev + 10)               # minimal value respecting the distance constraint
    hi = M - 10 * (remaining - 1)        # maximal value that still leaves room for the rest
Iterating from lo to hi in increasing order naturally yields lexicographical order.
"""

import sys
from typing import List


def generate_sequences(N: int, M: int) -> List[List[int]]:
    """Return all valid sequences in lexicographical order.

    The function uses backtracking. Because the total number of sequences is tiny
    (at most a few thousand for the given limits), we can store them all in memory.
    """
    res: List[List[int]] = []
    cur: List[int] = []

    def dfs(pos: int, prev: int) -> None:
        """Depth‑first search.

        pos  – current index (0‑based). When pos == N we have a complete sequence.
        prev – value of A_{pos-1} (or 0 for the first element).
        """
        if pos == N:
            res.append(cur.copy())
            return

        remaining = N - pos  # positions left including current
        # Minimal possible value for this position.
        if pos == 0:
            lo = 1
        else:
            lo = prev + 10
        # Maximal possible value: we need at least +10 for each of the remaining-1 steps.
        hi = M - 10 * (remaining - 1)
        if lo > hi:
            return
        for val in range(lo, hi + 1):
            cur.append(val)
            dfs(pos + 1, val)
            cur.pop()

    dfs(0, 0)
    return res


def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N, M = map(int, data)
    sequences = generate_sequences(N, M)
    out_lines = [str(len(sequences))]
    for seq in sequences:
        out_lines.append(' '.join(map(str, seq)))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
