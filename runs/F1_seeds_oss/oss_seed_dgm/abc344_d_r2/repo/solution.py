"""solution.py
Solution for the String Bags problem.

We are given a target string T, and N bags each containing a few candidate strings.
For each bag i (in order from 1 to N) we may either:
  * pay 1 yen and pick exactly one string from this bag, appending it to the current string S, or
  * do nothing.
We start with S empty and after all bags have been processed we need S == T.
The goal is to minimise the total money spent (i.e., the number of bags from which we pick a string).
If impossible output -1.

Observation
-----------
The operation order is fixed (bags are considered in increasing index), and each bag can be used at most once.
Thus the final S is a concatenation of a subsequence of the bags, preserving order.
Consequently we need to partition T into k (k ≥ 0) consecutive substrings, each substring being equal to one of the strings in the corresponding chosen bag.
The cost equals k, the number of chosen bags.

Dynamic programming
-------------------
Let L = len(T).  Define dp[i][j] = minimal cost to obtain the prefix T[0:i] after having processed the first j bags (j ranging 0..N).
The answer we need is dp[L][N].
Transition for bag j (1‑based): from state (i, j‑1) we have two possibilities:
  * Skip the bag: dp[i][j] = min(dp[i][j], dp[i][j-1])
  * Pick a string s from bag j (pay 1).  This is allowed only when T[i:i+len(s)] == s.
    Then dp[i+len(s)][j] = min(dp[i+len(s)][j], dp[i][j-1] + 1).
The base case is dp[0][0] = 0 and all other entries are INF.
Complexity: O(N * L * total_strings_per_bag) ≤ 100 * 100 * 10 = 1e5, easily fast.

Implementation details
----------------------
* Input parsing: after reading T and N, each of the following N lines starts with an integer A_i followed by A_i strings.
* We keep the bag strings in a list of lists `bags` (0‑based index for convenience).
* DP table: a 2‑dimensional list of size (L+1) × (N+1).  Using a large value (e.g., 10**9) for INF.
* Finally, if dp[L][N] is INF we output -1, otherwise the value.
"""

import sys

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    T = next(it)
    L = len(T)
    N = int(next(it))
    bags = []
    for _ in range(N):
        Ai = int(next(it))
        strings = [next(it) for _ in range(Ai)]
        bags.append(strings)

    INF = 10 ** 9
    # dp[pos][bag_index] -> minimal cost
    # We'll keep only the previous column to save memory, but full table is also fine.
    dp_prev = [INF] * (L + 1)
    dp_prev[0] = 0  # before processing any bag, empty prefix costs 0

    for idx, bag in enumerate(bags, start=1):
        dp_curr = [INF] * (L + 1)
        for pos in range(L + 1):
            if dp_prev[pos] == INF:
                continue
            # Option 1: skip this bag
            if dp_prev[pos] < dp_curr[pos]:
                dp_curr[pos] = dp_prev[pos]
            # Option 2: pick one string from this bag
            for s in bag:
                nxt = pos + len(s)
                if nxt <= L and T[pos:nxt] == s:
                    cost = dp_prev[pos] + 1
                    if cost < dp_curr[nxt]:
                        dp_curr[nxt] = cost
        dp_prev = dp_curr

    ans = dp_prev[L]
    print(-1 if ans == INF else ans)

if __name__ == "__main__":
    solve()
