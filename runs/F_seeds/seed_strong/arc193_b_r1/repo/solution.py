import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()

    # Relation R (2x2 boolean) for an allowed symbol set A subset of {0,1,2}.
    # State 0: last non-1 symbol was 0 (next non-1 must be 2).
    # State 1: last non-1 symbol was 2 (next non-1 must be 0).
    def relation(A):
        r = [[0, 0], [0, 0]]
        if 1 in A:
            r[0][0] = 1
            r[1][1] = 1
        if 2 in A:
            r[0][1] = 1
        if 0 in A:
            r[1][0] = 1
        return r

    # Product masks: bit (a*2+c) set iff M[a][c] true.
    def to_mask(M):
        m = 0
        for a in range(2):
            for c in range(2):
                if M[a][c]:
                    m |= 1 << (a * 2 + c)
        return m

    def mul_mask(m, r):
        # (M * R)[a][c] = OR_b M[a][b] & R[b][c]
        out = 0
        for a in range(2):
            for c in range(2):
                v = 0
                for b in range(2):
                    if (m >> (a * 2 + b)) & 1 and r[b][c]:
                        v = 1
                if v:
                    out |= 1 << (a * 2 + c)
        return out

    # Transition count matrices over 16 masks for a position of type t
    # (t = s_i). t=0: x in {0,1,2}, A={x}. t=1: x in {0..3}, A={x-1,x}∩{0,1,2}.
    def trans(t):
        T = [[0] * 16 for _ in range(16)]
        if t == 0:
            xs = [({0}), ({1}), ({2})]
        else:
            xs = []
            for x in range(4):
                A = {v for v in (x - 1, x) if 0 <= v <= 2}
                xs.append(A)
        rels = [relation(A) for A in xs]
        for m in range(16):
            for r in rels:
                T[m][mul_mask(m, r)] += 1
        return T

    T = [trans(0), trans(1)]

    def matmul(A, B, mod=None):
        R = [[0] * 16 for _ in range(16)]
        for i in range(16):
            Ai = A[i]
            Ri = R[i]
            for k in range(16):
                a = Ai[k]
                if a:
                    Bk = B[k]
                    for j in range(16):
                        if Bk[j]:
                            Ri[j] += a * Bk[j]
            if mod is not None:
                for j in range(16):
                    Ri[j] %= mod
        return R

    ident = [[1 if i == j else 0 for j in range(16)] for i in range(16)]

    CH = 8
    # Precompute chunk matrices for all patterns of length CH (MSB = first char).
    chunk_mats = [None] * (1 << CH)
    for p in range(1 << CH):
        M = ident
        for j in range(CH):
            bit = (p >> (CH - 1 - j)) & 1
            M = matmul(M, T[bit])
        chunk_mats[p] = M

    # Start: product = identity relation.
    start_mask = to_mask([[1, 0], [0, 1]])
    vec = [0] * 16
    vec[start_mask] = 1

    def vecmul(v, M):
        out = [0] * 16
        for i in range(16):
            vi = v[i]
            if vi:
                Mi = M[i]
                for j in range(16):
                    if Mi[j]:
                        out[j] += vi * Mi[j]
        return [x % MOD for x in out]

    full = n // CH
    pos = 0
    for _ in range(full):
        p = int(s[pos:pos + CH], 2)
        pos += CH
        # chunk matrix entries are small (<= 4^CH), vector entries < MOD: no overflow.
        vec = vecmul(vec, chunk_mats[p])

    rem = n - pos
    for i in range(pos, n):
        vec = vecmul(vec, T[int(s[i])])

    ans = 0
    for m in range(16):
        if vec[m] and ((m >> 0) & 1 or (m >> 3) & 1):
            ans += vec[m]
    print(ans % MOD)


main()
