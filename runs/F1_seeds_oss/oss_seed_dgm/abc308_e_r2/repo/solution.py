# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    S = list(next(it).strip())
    # Precompute total counts of X positions for each value
    suffix_counts = [0, 0, 0]
    for a, ch in zip(A, S):
        if ch == 'X':
            suffix_counts[a] += 1
    # Prefix counts for M positions
    pref_counts = [0, 0, 0]
    # Precompute mex table for all triples of values 0..2
    mex_table = [[[0]*3 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                present = {i, j, k}
                m = 0
                while m in present:
                    m += 1
                mex_table[i][j][k] = m
    ans = 0
    for idx in range(N):
        ch = S[idx]
        a = A[idx]
        # Remove current position from suffix if it is an X, because suffix should contain only positions > idx
        if ch == 'X':
            suffix_counts[a] -= 1
        if ch == 'E':
            aj = a
            # iterate over possible values for i (M) and k (X)
            for vi in range(3):
                pref = pref_counts[vi]
                if pref == 0:
                    continue
                for vk in range(3):
                    suf = suffix_counts[vk]
                    if suf == 0:
                        continue
                    m = mex_table[vi][aj][vk]
                    if m:
                        ans += pref * suf * m
        if ch == 'M':
            pref_counts[a] += 1
    print(ans)

if __name__ == "__main__":
    solve()
