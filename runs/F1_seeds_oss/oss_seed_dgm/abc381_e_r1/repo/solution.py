"""Solution for 11/22 Subsequence problem.
We need to answer Q queries on a string S consisting of characters '1', '2', '/'.
For each query [L, R] (1-indexed, inclusive) we consider the substring T = S[L-1:R].
We need the maximum length of a subsequence of T that forms an 11/22 string.
An 11/22 string has the form: k times '1', then '/', then k times '2', for some k >= 0.
Thus length = 2*k + 1 (always odd). The case k = 0 corresponds to just '/'.

Observation:
For any position i where S[i] == '/', we can take up to
    left_ones = number of '1's in T that appear before i,
    right_twos = number of '2's in T that appear after i.
The largest k achievable using this '/' is min(left_ones, right_twos).
Hence the answer for the query is:
    max_{i : S[i]=='/'} ( 2 * min(left_ones(i), right_twos(i)) + 1 ),
or 0 if there is no '/' in the range.

Let prefix arrays be 1-indexed:
    pre1[i] = # of '1' in S[1..i]
    pre2[i] = # of '2' in S[1..i]
Then for a query (L,R) and a slash at position i (L <= i <= R):
    left_ones(i)  = pre1[i-1] - pre1[L-1]
    right_twos(i) = pre2[R] - pre2[i]
Note that left_ones is non‑decreasing as i moves right, while right_twos is non‑increasing.
Therefore the function f(i) = min(left_ones(i), right_twos(i)) is unimodal, and its maximum is attained at the point where the two monotone values cross.
We can locate the crossing by binary searching among the positions of '/'.
For each query we:
  1. Find the slice of slash positions that lie inside [L,R] using bisect.
  2. If the slice is empty → answer 0.
  3. Binary search for the first index where left_ones >= right_twos.
  4. Evaluate f at that index and (optionally) the previous index; also consider the boundaries because the optimal may lie at the ends when there is no crossing.
All operations are O(log N) per query.
"""

import sys
import bisect

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    S = next(it).strip()
    # 1-indexed prefix counts
    pre1 = [0] * (N + 1)
    pre2 = [0] * (N + 1)
    slash_pos = []  # list of indices (1-indexed) where S[i-1] == '/'
    for i, ch in enumerate(S, start=1):
        pre1[i] = pre1[i-1] + (1 if ch == '1' else 0)
        pre2[i] = pre2[i-1] + (1 if ch == '2' else 0)
        if ch == '/':
            slash_pos.append(i)

    out_lines = []
    for _ in range(Q):
        L = int(next(it))
        R = int(next(it))
        # Find relevant slash indices
        left_idx = bisect.bisect_left(slash_pos, L)
        right_idx = bisect.bisect_right(slash_pos, R) - 1
        if left_idx > right_idx:
            out_lines.append('0')
            continue
        # Helper to compute min value for a slash at position i
        def min_k(pos: int) -> int:
            left_ones = pre1[pos-1] - pre1[L-1]
            right_twos = pre2[R] - pre2[pos]
            return left_ones if left_ones < right_twos else right_twos

        # Binary search for first position where left_ones >= right_twos
        lo = left_idx
        hi = right_idx
        while lo < hi:
            mid = (lo + hi) // 2
            pos = slash_pos[mid]
            left_ones = pre1[pos-1] - pre1[L-1]
            right_twos = pre2[R] - pre2[pos]
            if left_ones >= right_twos:
                hi = mid
            else:
                lo = mid + 1
        # lo is the first index where left_ones >= right_twos, may be at boundaries
        best_k = 0
        # evaluate at lo
        best_k = max(best_k, min_k(slash_pos[lo]))
        # evaluate at previous if exists
        if lo - 1 >= left_idx:
            best_k = max(best_k, min_k(slash_pos[lo-1]))
        # also evaluate at boundaries in case monotone never crosses
        best_k = max(best_k, min_k(slash_pos[left_idx]))
        best_k = max(best_k, min_k(slash_pos[right_idx]))
        # length is 2*best_k + 1
        out_lines.append(str(2 * best_k + 1))

    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
