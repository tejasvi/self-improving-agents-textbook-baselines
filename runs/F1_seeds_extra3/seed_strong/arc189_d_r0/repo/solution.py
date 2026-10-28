import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    P = [0] * (n + 1)
    s = 0
    for i in range(n):
        s += A[i]
        P[i + 1] = s
    # sparse table: sp[k][i] = max A[i .. i+2^k-1]
    sp = [A]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        h = 1 << (k - 1)
        cur = list(map(max, prev[:len(prev) - h], prev[h:]))
        sp.append(cur)
        k += 1
    LOG = len(sp)

    def left_block(p, S):
        # largest j <= p with A[j] >= S, or -1
        pos = p  # current candidate region is [.., pos], all < S so far
        for kk in range(LOG - 1, -1, -1):
            st = pos - (1 << kk) + 1
            if st >= 0 and sp[kk][st] < S:
                pos = st - 1
        return pos  # -1 if none; else A[pos] >= S

    def right_block(p, S):
        # smallest j >= p with A[j] >= S, or n
        pos = p
        for kk in range(LOG - 1, -1, -1):
            if pos + (1 << kk) <= n and sp[kk][pos] < S:
                pos += 1 << kk
        return pos  # n if none

    out = []
    for K in range(n):
        l = r = K
        S = A[K]
        while True:
            changed = False
            # extend left
            if l > 0 and A[l - 1] < S:
                j = left_block(l - 1, S)
                nl = j + 1
                S += P[l] - P[nl]
                l = nl
                changed = True
            # extend right
            if r < n - 1 and A[r + 1] < S:
                j = right_block(r + 1, S)
                nr = j - 1
                S += P[nr + 1] - P[r + 1]
                r = nr
                changed = True
            if not changed:
                break
        out.append(S)
    sys.stdout.write(" ".join(map(str, out)) + "\n")


main()
