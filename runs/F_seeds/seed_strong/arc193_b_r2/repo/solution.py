import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    s = data[1].strip()
    k = s.count('1')
    # Reduced problem (verified against brute force on random small cases):
    # count z in prod [-1, s_i+1] with 0 <= sum z <= k and, for every proper
    # cyclic arc I, sum_I z in [-1, h(I)+1] where h(I) = #ones in I.
    # NOTE: this is a plain DFS, exponential in N; it is NOT an efficient
    # solution for N up to 1e6.
    bits = [int(c) for c in s]
    arcs_by_end = [[] for _ in range(N)]  # arcs ending (linear) at index j, non-wrapping
    # Build linear prefix constraints for arcs not wrapping past index N-1,
    # and check wrapping arcs at the end.
    arcs = []
    for st in range(N):
        for L in range(1, N):
            idx = [(st + j) % N for j in range(L)]
            arcs.append((st, L, sum(bits[i] for i in idx)))
    # Group arcs by the last index they touch in linear order 0..N-1 (only non-wrapping arcs can be checked early)
    check_at = [[] for _ in range(N)]
    final_arcs = []
    for st, L, h in arcs:
        if st + L - 1 < N:
            check_at[st + L - 1].append((st, h))
        else:
            final_arcs.append((st, L, h))
    z = [0] * N
    prefix = [0] * (N + 1)
    count = 0

    def dfs(i):
        nonlocal count
        if i == N:
            Z = prefix[N]
            if not (0 <= Z <= k):
                return
            for st, L, h in final_arcs:
                idx = [(st + j) % N for j in range(L)]
                t = sum(z[x] for x in idx)
                if not (-1 <= t <= h + 1):
                    return
            count += 1
            return
        for v in range(-1, bits[i] + 2):
            z[i] = v
            prefix[i + 1] = prefix[i] + v
            ok = True
            for st, h in check_at[i]:
                t = prefix[i + 1] - prefix[st]
                if not (-1 <= t <= h + 1):
                    ok = False
                    break
            if ok:
                dfs(i + 1)
        z[i] = 0

    dfs(0)
    print(count % MOD)

main()
