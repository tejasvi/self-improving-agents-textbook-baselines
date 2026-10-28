import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    mx = 2 * max(A)

    def G(k):
        # Sum over unordered pairs i<=j with 2^k | (A_i + A_j) of (A_i + A_j).
        M = 1 << k
        mask = M - 1
        C = {}
        S = {}
        for a in A:
            r = a & mask
            C[r] = C.get(r, 0) + 1
            S[r] = S.get(r, 0) + a
        # ordered pairs (including i=j): sum over r of S_r * C_{-r} * 2
        ordered = 0
        for r, s in S.items():
            t = (-r) & mask
            c = C.get(t)
            if c:
                ordered += s * c
        ordered *= 2
        # diagonal i=j terms: 2*A_i where 2*A_i ≡ 0 mod 2^k
        diag = 0
        for a in A:
            if (2 * a) & mask == 0:
                diag += 2 * a
        return (ordered + diag) // 2

    K = 0
    while (1 << K) <= mx:
        K += 1
    Gs = [G(k) for k in range(K + 1)] + [0]
    ans = 0
    for k in range(K + 1):
        ans += (Gs[k] - Gs[k + 1]) >> k
    print(ans)


main()
