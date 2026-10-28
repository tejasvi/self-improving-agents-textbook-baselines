import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    N = int(data[0]); M = int(data[1]); K = int(data[2])
    X = []
    Y = []
    p = 3
    for _ in range(M):
        X.append(int(data[p]) - 1)
        Y.append(int(data[p + 1]) - 1)
        p += 2
    # Rotating frame: g_t[i] = f_t[(i + t) mod N]; cycle edges become identity.
    g = [0] * N
    g[0] = 1
    if M == 0:
        print(1 % MOD)
        return
    for t in range(K):
        vals = [g[(x - t) % N] for x in X]
        for y, v in zip(Y, vals):
            if v:
                j = (y - t - 1) % N
                g[j] = (g[j] + v) % MOD
    print(sum(g) % MOD)

main()
