# Solution for Maximize XOR problem.
# Given N (up to 2e5) numbers and K, with the guarantee that C(N, K) <= 1e6.
# We need the maximum XOR of any K distinct elements.
# Since the total number of combinations is bounded, we can enumerate all subsets efficiently.
# To speed up the case where all remaining elements must be taken, we pre‑compute suffix XORs.

import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # suffix_xor[i] = A[i] xor A[i+1] xor ... xor A[N-1]
    suffix_xor = [0] * (N + 1)
    for i in range(N - 1, -1, -1):
        suffix_xor[i] = suffix_xor[i + 1] ^ A[i]

    max_xor = 0
    # Stack for manual DFS: (pos, chosen_cnt, current_xor)
    stack = [(0, 0, 0)]
    while stack:
        pos, chosen, cur = stack.pop()
        if chosen == K:
            if cur > max_xor:
                max_xor = cur
            continue
        if pos == N:
            continue
        need = K - chosen
        remain = N - pos
        if remain < need:
            continue
        if remain == need:
            # Must take all remaining elements.
            total = cur ^ suffix_xor[pos]
            if total > max_xor:
                max_xor = total
            continue
        # Branch: skip current element (if possible)
        if remain - 1 >= need:
            stack.append((pos + 1, chosen, cur))
        # Branch: take current element
        stack.append((pos + 1, chosen + 1, cur ^ A[pos]))

    print(max_xor)

if __name__ == "__main__":
    solve()
