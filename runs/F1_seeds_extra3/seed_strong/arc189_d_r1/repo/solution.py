import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    pre = [0] * (n + 1)
    s = 0
    for i, a in enumerate(A):
        s += a
        pre[i + 1] = s
    # sparse table of range maxima: sp[k][i] = max(A[i .. i+2^k-1])
    sp = [A]
    j = 1
    while (1 << j) <= n:
        prev = sp[-1]
        h = 1 << (j - 1)
        m = n - (1 << j) + 1
        sp.append(list(map(max, prev[:m], prev[h:h + m])))
        j += 1
    LOG = len(sp)
    LIN = 8

    res = []
    for K in range(n):
        l = r = K
        S = A[K]
        while True:
            # nearest x < l with A[x] >= S (or -1)
            x = l - 1
            cnt = 0
            while x >= 0 and A[x] < S and cnt < LIN:
                x -= 1
                cnt += 1
            if x >= 0 and A[x] < S:
                pos = x + 1  # all of [pos, l) ... descend from pos
                for k in range(LOG - 1, -1, -1):
                    st = pos - (1 << k)
                    if st >= 0 and sp[k][st] < S:
                        pos = st
                x = pos - 1
            # nearest y > r with A[y] >= S (or n)
            y = r + 1
            cnt = 0
            while y < n and A[y] < S and cnt < LIN:
                y += 1
                cnt += 1
            if y < n and A[y] < S:
                pos = y
                for k in range(LOG - 1, -1, -1):
                    if pos + (1 << k) <= n and sp[k][pos] < S:
                        pos += 1 << k
                y = pos
            nl = x + 1
            nr = y - 1
            if nl == l and nr == r:
                break
            l, r = nl, nr
            S = pre[r + 1] - pre[l]
        res.append(S)
    sys.stdout.write(" ".join(map(str, res)) + "\n")


main()
