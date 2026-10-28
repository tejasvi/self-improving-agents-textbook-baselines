import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 2)
    for i in range(n):
        A[i + 1] = int(data[1 + i])
    INF = float('inf')
    BIG = 1 << 62
    A[0] = BIG
    A[n + 1] = BIG
    P = [0] * (n + 1)
    s = 0
    for i in range(1, n + 1):
        s += A[i]
        P[i] = s

    # prev strictly greater chain (left), sentinel 0
    pg = [0] * (n + 2)
    st = [0]
    for i in range(1, n + 1):
        a = A[i]
        while A[st[-1]] <= a and st[-1] != 0:
            st.pop()
        pg[i] = st[-1]
        st.append(i)
    # next strictly greater chain (right), sentinel n+1
    ng = [n + 1] * (n + 2)
    st = [n + 1]
    for i in range(n, 0, -1):
        a = A[i]
        while A[st[-1]] <= a and st[-1] != n + 1:
            st.pop()
        ng[i] = st[-1]
        st.append(i)
    ng[0] = n + 1
    pg[0] = 0
    pg[n + 1] = 0
    ng[n + 1] = n + 1

    LOG = 1
    while (1 << LOG) <= n + 2:
        LOG += 1
    upL = [pg]
    upR = [ng]
    for k in range(1, LOG):
        pl = upL[-1]
        pr = upR[-1]
        upL.append(list(map(pl.__getitem__, pl)))
        upR.append(list(map(pr.__getitem__, pr)))

    def leftq(l, S):
        # largest j < l with A[j] >= S (sentinel 0 has BIG)
        x = l - 1
        if A[x] >= S:
            return x
        for k in range(LOG - 1, -1, -1):
            y = upL[k][x]
            if A[y] < S:
                x = y
        return upL[0][x]

    def rightq(r, S):
        x = r + 1
        if A[x] >= S:
            return x
        for k in range(LOG - 1, -1, -1):
            y = upR[k][x]
            if A[y] < S:
                x = y
        return upR[0][x]

    res = []
    for K in range(1, n + 1):
        l = r = K
        S = A[K]
        while True:
            changed = False
            j = leftq(l, S)
            if j != l - 1:
                l = j + 1
                S = P[r] - P[l - 1]
                changed = True
            j = rightq(r, S)
            if j != r + 1:
                r = j - 1
                S = P[r] - P[l - 1]
                changed = True
            if not changed:
                break
        res.append(S)
    sys.stdout.write(' '.join(map(str, res)) + '\n')


main()
