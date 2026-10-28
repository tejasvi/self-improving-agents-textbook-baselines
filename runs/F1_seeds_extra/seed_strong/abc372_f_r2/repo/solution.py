import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N, M, K = int(data[0]), int(data[1]), int(data[2])
    if M == 0:
        print(1)
        return
    X = [int(data[3 + 2 * i]) % N for i in range(M)]
    Y = [int(data[4 + 2 * i]) % N for i in range(M)]
    # Key = (pos - t) mod N is invariant under cycle edges.
    # Special edge X->Y used at time t: key (X - t) -> key (Y - t - 1).
    w = [0] * N
    w[1 % N] = 1
    rng = range(M)
    tm = 0  # t mod N
    for t in range(K):
        # snapshot the transfers from the state at time t
        cs = [w[(X[e] - tm) % N] % MOD for e in rng]
        for e in rng:
            c = cs[e]
            if c:
                w[(Y[e] - tm - 1) % N] += c
        tm += 1
        if tm == N:
            tm = 0
    print(sum(w) % MOD)

main()
