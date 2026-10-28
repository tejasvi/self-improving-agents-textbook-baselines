import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    N, M, K = int(data[0]), int(data[1]), int(data[2])
    X = []
    Y = []
    p = 3
    for _ in range(M):
        X.append(int(data[p]) % N)
        Y.append(int(data[p + 1]) % N)
        p += 2

    # Coordinate c = (vertex - time) mod N. Cycle moves keep c fixed.
    # Taking extra edge X->Y at time t copies mass from coordinate X - t
    # to coordinate Y - (t+1). Total answer = total mass after K steps.
    F = [0] * N
    F[1 % N] = 1
    total = 1  # mass at time 0 (sum of F)
    for t in range(K):
        if M == 0:
            break
        vals = [F[(x - t) % N] for x in X]
        s = sum(vals)
        if s:
            total = (total + s) % MOD
            t1 = t + 1
            for y, v in zip(Y, vals):
                if v:
                    j = (y - t1) % N
                    F[j] = (F[j] + v) % MOD
    print(total % MOD)


main()
