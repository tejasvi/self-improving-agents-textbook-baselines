import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # f(s) = s / 2^k where k = v2(s); v2(s) = k  <=>  s mod 2^(k+1) == 2^k.
    ordered = 0
    for k in range(0, 26):
        mask = (1 << (k + 1)) - 1
        r = 1 << k
        cnt = {}
        sm = {}
        for a in A:
            x = a & mask
            cnt[x] = cnt.get(x, 0) + 1
            sm[x] = sm.get(x, 0) + a
        T = 0
        for x, sx in sm.items():
            cy = cnt.get((r - x) & mask)
            if cy:
                T += sx * cy
        ordered += (2 * T) >> k

    # diagonal (i == j): f(2*A_i) = f(A_i)
    diag = 0
    for a in A:
        while a % 2 == 0:
            a //= 2
        diag += a
    print((ordered + diag) // 2)


main()
