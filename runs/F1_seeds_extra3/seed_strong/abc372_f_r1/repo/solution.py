import sys

def main():
    data = sys.stdin.buffer.read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    MOD = 998244353
    if m == 0:
        # Only the cycle edges: exactly one walk.
        print(1)
        return
    # Shifted frame (0-indexed): a[(v - t) mod n] = ways to be at vertex v after t steps.
    # Cycle moves leave a unchanged. Extra edge x->y at step t: a[(y - t - 1)] += a[(x - t)].
    S = [int(data[3 + 2 * i]) - 1 for i in range(m)]
    D = [(int(data[4 + 2 * i]) - 2) % n for i in range(m)]
    a = [0] * n
    a[0] = 1
    for _ in range(k):
        vals = [a[s] for s in S]
        for d, v in zip(D, vals):
            a[d] = (a[d] + v) % MOD
        S = [s - 1 if s else n - 1 for s in S]
        D = [d - 1 if d else n - 1 for d in D]
    print(sum(a) % MOD)

main()
