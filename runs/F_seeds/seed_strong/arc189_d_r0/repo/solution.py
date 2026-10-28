import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    # SP[t][i] = max(A[i .. i+2^t-1]), valid for i + 2^t <= n
    SP = [A]
    t = 1
    while (1 << t) <= n:
        prev = SP[-1]
        half = 1 << (t - 1)
        length = n - (1 << t) + 1
        SP.append([a if a > b else b for a, b in zip(prev[:length], prev[half:half + length])])
        t += 1
    LOG = len(SP)

    prefix = [0] * (n + 1)
    s = 0
    for i, a in enumerate(A):
        s += a
        prefix[i + 1] = s

    def ext_left(q, S):
        # absorbed block is [q, r]; return smallest q' with all A[q'..q-1] < S
        t = 0
        while True:
            w = 1 << t
            st = q - w
            if st < 0:
                break
            if SP[t][st] >= S:
                break
            q = st
            t += 1
            if t >= LOG:
                break
        t -= 1
        while t >= 0:
            w = 1 << t
            st = q - w
            if st >= 0 and SP[t][st] < S:
                q = st
            t -= 1
        return q

    def ext_right(r, S):
        # absorbed block ends at r; return largest r' with all A[r+1..r'] < S
        t = 0
        while True:
            w = 1 << t
            st = r + 1
            if st + w > n:
                break
            if SP[t][st] >= S:
                break
            r = st + w - 1
            t += 1
            if t >= LOG:
                break
        t -= 1
        while t >= 0:
            w = 1 << t
            st = r + 1
            if st + w <= n and SP[t][st] < S:
                r = st + w - 1
            t -= 1
        return r

    res = [0] * n
    for K in range(n):
        l = K
        r = K
        S = A[K]
        while True:
            nl = ext_left(l, S)
            nr = ext_right(r, S)
            newS = prefix[nr + 1] - prefix[nl]
            l, r = nl, nr
            if newS == S:
                break
            S = newS
        res[K] = S

    sys.stdout.write(" ".join(map(str, res)) + "\n")


main()
