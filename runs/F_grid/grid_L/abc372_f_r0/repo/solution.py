import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    N = int(data[0]); M = int(data[1]); K = int(data[2])
    xs = []
    ys = []
    for i in range(M):
        xs.append(int(data[3 + 2 * i]) - 1)
        ys.append(int(data[4 + 2 * i]) - 1)

    # Let c[t][i] = (#walks of length t from vertex 1 ending at X_i).
    # dp_t[x] = [x == t mod N] + sum_{s<t} sum_j c[s][j] * [x == y_j + (t-1-s) mod N]
    # Z[u] maintains sum over contributions; query index for edge i at time t: (t-1-x_i) mod N
    # update for c[t][j]: index (t - y_j) mod N.
    Z = [0] * N
    # precompute per-edge constants
    qa = [(-1 - x) % N for x in xs]
    ua = [(-y) % N for y in ys]
    total = 1
    if M == 0:
        print(1 % MOD)
        return
    for t in range(K):
        tm = t % N
        cs = [0] * M
        s_sum = 0
        for i in range(M):
            idx = (qa[i] + t) % N
            v = Z[idx]
            if xs[i] == tm:
                v += 1
            v %= MOD
            cs[i] = v
            s_sum += v
        total = (total + s_sum) % MOD
        for j in range(M):
            idx = (ua[j] + t) % N
            Z[idx] += cs[j]
    print(total % MOD)

main()
