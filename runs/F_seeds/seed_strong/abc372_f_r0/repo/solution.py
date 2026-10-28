import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N, M, K = int(data[0]), int(data[1]), int(data[2])
    X = []
    Y = []
    pos = 3
    for _ in range(M):
        X.append(int(data[pos]))
        Y.append(int(data[pos + 1]))
        pos += 2
    if M == 0:
        print(1)
        return
    # E[k]: sum of a_s[i] over s <= t-1 with (s - Y_i) mod N == k.
    # a_t[j] = [X_j == t (mod N)] + E[(t-1-X_j) mod N].
    E = [0] * N
    ins = [(-y) % N for y in Y]
    Xm = [x % N for x in X]
    pairs = list(zip(ins, range(M)))
    prev = [0] * M
    total = 1
    for t in range(1, K + 1):
        s = t - 1
        if t >= 2:
            # insert a_{t-1} contributions keyed by (s - Y_i) mod N
            for off, i in pairs:
                p = prev[i]
                if p:
                    k = (s + off) % N
                    E[k] = (E[k] + p) % MOD
        t1 = s % N
        tm = t % N
        cur = [0] * M
        ssum = 0
        for j in range(M):
            v = E[(t1 - Xm[j]) % N]
            if Xm[j] == tm:
                v += 1
            v %= MOD
            cur[j] = v
            ssum += v
        total = (total + ssum) % MOD
        prev = cur
    print(total % MOD)

main()
