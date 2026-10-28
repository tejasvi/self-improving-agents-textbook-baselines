import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N, M, K = int(data[0]), int(data[1]), int(data[2])
    # g[u] with u = (v - t) mod N. Cycle edges are identity in these coordinates.
    # Extra edge X->Y at step t (t -> t+1): g[(Y-t-1) mod N] += g[(X-t) mod N] (old values).
    g = [0] * N
    g[1 % N] = 1  # t = 0, v = 1
    src = [int(data[3 + 2 * i]) % N for i in range(M)]   # X_j - t, at t = 0
    dst = [(int(data[4 + 2 * i]) - 1) % N for i in range(M)]  # Y_j - t - 1, at t = 0
    pairs = list(zip(src, dst))
    for _ in range(K):
        if pairs:
            reads = [g[a] for a, _ in pairs]
            for (a, b), r in zip(pairs, reads):
                if r:
                    g[b] = (g[b] + r) % MOD
            # both pointers move by -1 per step
            pairs = [((a - 1) % N, (b - 1) % N) for a, b in pairs]
    print(sum(g) % MOD)

main()
