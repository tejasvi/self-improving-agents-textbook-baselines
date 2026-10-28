import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    maxs = 2 * max(A)
    # T[k] = sum over pairs i<=j with 2^k | (A_i+A_j) of (A_i+A_j)
    LIM = maxs.bit_length() + 1
    T = [0] * (LIM + 1)
    for k in range(LIM):
        m = 1 << k
        mask = m - 1
        cnt = {}
        sm = {}
        for a in A:
            r = a & mask
            if r in cnt:
                cnt[r] += 1
                sm[r] += a
            else:
                cnt[r] = 1
                sm[r] = a
        # ordered pairs (i, j), including i == j
        ordered = 0
        for r, c in cnt.items():
            p = (-r) & mask
            cp = cnt.get(p)
            if cp:
                ordered += sm[r] * cp + c * sm[p]
        # diagonal: i == j, pair sum 2*A_i, need 2*A_i divisible by m
        half = m >> 1 if m > 1 else 1
        if m == 1:
            diag = 2 * sum(A)
        else:
            diag = 0
            for a in A:
                if a % half == 0:
                    diag += 2 * a
        T[k] = (ordered + diag) // 2
    ans = 0
    for k in range(LIM):
        group = T[k] - T[k + 1]
        ans += group >> k
    print(ans)


main()
