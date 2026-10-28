import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    total = 0
    # For each k, pairs (i<=j) with v2(a_i+a_j) == k satisfy sum ≡ 2^k (mod 2^(k+1)).
    # f(s) = s / 2^k for those pairs.
    for k in range(0, 27):
        M = 1 << (k + 1)
        r = 1 << k
        cnt = {}
        sm = {}
        for x in a:
            m = x & (M - 1)
            cnt[m] = cnt.get(m, 0) + 1
            sm[m] = sm.get(m, 0) + x
        TS = 0
        for x, cx in cnt.items():
            y = (r - x) & (M - 1)
            cy = cnt.get(y)
            if cy:
                TS += sm[x] * cy + cx * sm[y]
        # diagonal: i == j, sum 2*a_i with 2*a_i ≡ r (mod M)
        DS = 0
        for x in a:
            if (2 * x) & (M - 1) == r:
                DS += 2 * x
        S = (TS + DS) // 2  # sum of s over unordered pairs i<=j with v2(s)=k
        total += S >> k
    print(total)


main()
