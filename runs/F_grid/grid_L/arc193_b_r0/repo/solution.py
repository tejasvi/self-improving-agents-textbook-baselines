import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    s = data[1][:N]

    # A 2x2 boolean matrix is encoded as 4 bits: bit (2*a + b) = entry [a][b].
    def to_mat(p):
        return [[(p >> (2 * a + b)) & 1 for b in range(2)] for a in range(2)]

    def to_bits(m):
        r = 0
        for a in range(2):
            for b in range(2):
                if m[a][b]:
                    r |= 1 << (2 * a + b)
        return r

    def mul(p, q):
        P = to_mat(p)
        Q = to_mat(q)
        R = [[0, 0], [0, 0]]
        for a in range(2):
            for b in range(2):
                R[a][b] = 1 if (P[a][0] & Q[0][b]) or (P[a][1] & Q[1][b]) else 0
        return to_bits(R)

    # trans[sv][p] = list of (newp, count): for each d in 0..3 that is allowed
    # with s-bit sv, the boolean product P * M_d is accumulated.
    trans = [[[0] * 16 for _ in range(16)] for _ in range(2)]
    for sv in range(2):
        for d in range(4):
            M = [[0, 0], [0, 0]]
            for tp in range(2):
                for tc in range(2):
                    # c_i = t_{i-1} + 1 - t_i ; need d - c_i in [0, sv]
                    v = d - (tp + 1 - tc)
                    M[tp][tc] = 1 if 0 <= v <= sv else 0
            mb = to_bits(M)
            for p in range(16):
                trans[sv][p][mul(p, mb)] += 1

    tr = [[[(q, trans[sv][p][q]) for q in range(16) if trans[sv][p][q]]
           for p in range(16)] for sv in range(2)]

    ident = to_bits([[1, 0], [0, 1]])
    v = [0] * 16
    v[ident] = 1
    for ch in s:
        t = tr[1 if ch == '1' else 0]
        nv = [0] * 16
        for p in range(16):
            x = v[p]
            if x:
                for q, c in t[p]:
                    nv[q] += x * c
        v = [x % MOD for x in nv]

    ans = 0
    for p in range(16):
        # accept if trace nonzero: bit 0 = [0][0], bit 3 = [1][1]
        if (p & 1) or ((p >> 3) & 1):
            ans += v[p]
    print(ans % MOD)


main()
