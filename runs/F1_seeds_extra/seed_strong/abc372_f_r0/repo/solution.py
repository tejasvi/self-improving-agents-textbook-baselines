import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    N, M, K = int(data[0]), int(data[1]), int(data[2])
    X = []
    Y = []
    for i in range(M):
        X.append(int(data[3 + 2 * i]))
        Y.append(int(data[4 + 2 * i]))
    if M == 0:
        print(1)
        return
    # Runs: a walker at vertex v at time t belongs to a run with key (v - t) mod N.
    # acc[k] = total weight of runs with key k started so far.
    acc = [0] * N
    acc[1 % N] = 1
    total = 1
    # Per-step: L_j = acc[(X_j - s) mod N]; then acc[(Y_j - s - 1) mod N] += L_j
    pairs = list(zip(X, Y))
    for s in range(K):
        Ls = [acc[(x - s) % N] for x in X]
        for j in range(M):
            L = Ls[j]
            if L:
                k = (Y[j] - s - 1) % N
                acc[k] = (acc[k] + L) % MOD
                total += L
        total %= MOD
    print(total % MOD)

main()
