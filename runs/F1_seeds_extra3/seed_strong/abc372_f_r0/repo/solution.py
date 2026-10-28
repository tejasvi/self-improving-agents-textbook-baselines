import sys

def main():
    data = sys.stdin.read().split()
    MOD = 998244353
    N, M, K = int(data[0]), int(data[1]), int(data[2])
    if M == 0:
        print(1)
        return
    # Shifted frame: f_t[j] = dp_t[(j + t) mod N] (0-indexed vertices).
    # Cycle edge u->u+1 becomes f_t[j] += f_{t-1}[j] (identity copy).
    # Extra edge x->y adds f_{t-1}[(x+1-t) mod N] into f_t[(y-t) mod N].
    # Answer = sum of f_K, with f_0 = e_0 (vertex 1 at index 0).
    srcs = []
    tgts = []
    for i in range(M):
        x = int(data[3 + 2 * i]) - 1
        y = int(data[4 + 2 * i]) - 1
        srcs.append((x + 1) % N)
        tgts.append(y % N)
    # Reads and writes at step t are both shifted by the same r = t mod N,
    # so in-place updates are safe iff no target index equals a source index.
    conflict = bool(set(srcs) & set(tgts))
    pairs = list(zip(srcs, tgts))
    f = [0] * N
    f[0] = 1
    total = 1
    r = 0
    for t in range(1, K + 1):
        r += 1
        if r == N:
            r = 0
        s = 0
        if not conflict:
            for a, b in pairs:
                i = a - r
                if i < 0:
                    i += N
                v = f[i]
                if v:
                    s += v
                    j = b - r
                    if j < 0:
                        j += N
                    f[j] = (f[j] + v) % MOD
        else:
            vals = []
            for a, b in pairs:
                i = a - r
                if i < 0:
                    i += N
                vals.append(f[i])
            for (a, b), v in zip(pairs, vals):
                s += v
                j = b - r
                if j < 0:
                    j += N
                f[j] = (f[j] + v) % MOD
        total = (total + s) % MOD
    print(total % MOD)

main()
