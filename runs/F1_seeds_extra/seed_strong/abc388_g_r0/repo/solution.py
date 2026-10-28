import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    q = int(data[1 + n])
    pos = 2 + n

    # c[x] = h[x] - x, h[x] = first index j with A[j] >= 2*A[x]
    c = [bisect_left(A, 2 * A[x]) - x for x in range(n)]

    # sparse table: sp[j][i] = max(c[i .. i+2^j-1]) (valid for i + 2^j <= n)
    sp = [c]
    j = 1
    while (1 << j) <= n:
        prev = sp[-1]
        half = 1 << (j - 1)
        length = n - (1 << j) + 1
        sp.append(list(map(max, prev[:length], prev[half:half + length])))
        j += 1
    LV = len(sp)

    out = []
    NEG = -(1 << 60)
    for _ in range(q):
        L = int(data[pos]) - 1
        R = int(data[pos + 1]) - 1
        pos += 2
        ln = R - L + 1
        half = ln // 2
        K = 0
        p = L
        cur = NEG
        for j in range(LV - 1, -1, -1):
            step = 1 << j
            nk = K + step
            if nk > half or p + step > n:
                continue
            m = sp[j][p]
            if m < cur:
                m = cur
            if m + nk <= ln:
                K = nk
                cur = m
                p += step
        out.append(K)
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
