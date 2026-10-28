import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    # S_k = sum of (a_i + a_j) over pairs i <= j with 2^k | (a_i + a_j)
    # s = a_i + a_j < 2 * 10^7 < 2^25, so k up to 25 suffices.
    K = 26
    S = [0] * (K + 1)
    for k in range(K + 1):
        M = 1 << k
        mask = M - 1
        cnt = {}
        sm = {}
        for x in a:
            r = x & mask
            cnt[r] = cnt.get(r, 0) + 1
            sm[r] = sm.get(r, 0) + x
        # ordered pairs (i, j) including i == j, sum of a_i + a_j
        T = 0
        for r, c in cnt.items():
            r2 = (-r) & mask
            c2 = cnt.get(r2)
            if c2:
                T += sm[r] * c2 + c * sm[r2]
        # diagonal i == j: s = 2*a_i, valid when 2*a_i divisible by M
        D = 0
        for x in a:
            if (2 * x) & mask == 0:
                D += 2 * x
        # unordered pairs with i <= j: (T + D) / 2
        S[k] = (T + D) // 2

    ans = 0
    for k in range(K):
        ans += (S[k] - S[k + 1]) >> k
    print(ans)


main()
