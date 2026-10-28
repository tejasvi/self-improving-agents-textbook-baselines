import sys


def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    xs = []
    ys = []
    pos = 3
    for _ in range(M):
        xs.append(int(data[pos]) - 1)
        ys.append(int(data[pos + 1]) - 1)
        pos += 2

    # D[s][v] = number of walks of length s ending at v (0-indexed vertices).
    # D[s][v] = D[s-1][v-1] + sum_{extra edges x->v} D[s-1][x].
    # Store G[c] = D[s][(c + s) mod N]; the cycle edges then become free,
    # and only the extra-edge injections write into G.
    G = [0] * N
    G[0] = 1  # D[0][0] = 1
    pairs = list(zip(xs, ys))
    for s in range(1, K + 1):
        sm = s - 1
        if pairs:
            vals = [G[(x - sm) % N] for x, _ in pairs]
            for (_, y), v in zip(pairs, vals):
                if v:
                    idx = (y - s) % N
                    G[idx] = (G[idx] + v) % MOD
    print(sum(G) % MOD)


main()
