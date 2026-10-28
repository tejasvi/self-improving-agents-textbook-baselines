import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    # Sums are at most 2*10^7 < 2^25, so S[k] == 0 for k >= 25.
    K = 26
    # S[k] = sum of (A_i + A_j) over unordered pairs i <= j with 2^k | (A_i + A_j)
    S = [0] * (K + 1)
    for k in range(K):
        M = 1 << k
        mask = M - 1
        cnt = {}
        sm = {}
        for a in A:
            r = a & mask
            cnt[r] = cnt.get(r, 0) + 1
            sm[r] = sm.get(r, 0) + a
        # ordered-pair total over (i, j) with A_i + A_j ≡ 0 mod 2^k
        T = 0
        for r, c in cnt.items():
            cc = cnt.get((-r) & mask)
            if cc:
                T += sm[r] * cc
        T *= 2
        # diagonal pairs (i, i): contribution 2*A_i when 2*A_i ≡ 0 mod 2^k
        D = 0
        for a in A:
            if (2 * a) & mask == 0:
                D += 2 * a
        S[k] = (T + D) // 2

    ans = 0
    for k in range(K):
        # pairs with 2-adic valuation exactly k have s = (S[k]-S[k+1]) total,
        # each contributing s / 2^k (exact division since 2^k | s)
        ans += (S[k] - S[k + 1]) >> k
    print(ans)


main()
