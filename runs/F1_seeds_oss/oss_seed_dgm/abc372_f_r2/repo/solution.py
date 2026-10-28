# Write your solution here. Read from stdin, write to stdout.

import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(map(int, data))
    N = next(it)
    M = next(it)
    K = next(it)
    extra = [(next(it), next(it)) for _ in range(M)]

    # dp values for vertices 1..N stored in arr with a rotating offset
    arr = [0] * N
    arr[0] = 1  # start at vertex 1
    offset = 0  # logical shift applied to map arr index -> vertex number

    for _ in range(K):
        # process all extra edges for this step
        new_offset = (offset + 1) % N
        for x, y in extra:
            # source index in current arr
            src_idx = (x - 1 - offset) % N
            val = arr[src_idx]
            if val:
                dst_idx = (y - 1 - new_offset) % N
                arr[dst_idx] = (arr[dst_idx] + val) % MOD
        offset = new_offset

    # after K steps, total ways = sum over all vertices
    ans = sum(arr) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
