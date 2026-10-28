import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 2)
    for i in range(n):
        A[i + 1] = int(data[1 + i])
    INF = float("inf")
    A[0] = INF
    A[n + 1] = INF
    P = [0] * (n + 2)
    for i in range(1, n + 1):
        P[i] = P[i - 1] + A[i]
    # pge[i]: nearest j < i with A[j] >= A[i] (0 is sentinel with INF)
    # pgeR[i]: nearest j > i with A[j] >= A[i] (n+1 sentinel)
    LOG = 1
    while (1 << LOG) <= n + 2:
        LOG += 1
    # left chain binary lifting
    pl = [0] * (n + 2)
    st = [0]
    for i in range(1, n + 1):
        while A[st[-1]] < A[i]:
            st.pop()
        pl[i] = st[-1]
        st.append(i)
    pr = [n + 1] * (n + 2)
    st = [n + 1]
    for i in range(n, 0, -1):
        while A[st[-1]] < A[i]:
            st.pop()
        pr[i] = st[-1]
        st.append(i)
    # up[k][i] for left chain and right chain
    upl = [pl]
    for k in range(1, LOG):
        prev = upl[-1]
        upl.append(list(map(prev.__getitem__, prev)))
    upr = [pr]
    for k in range(1, LOG):
        prev = upr[-1]
        upr.append(list(map(prev.__getitem__, prev)))

    def nearest_left(p, S):
        # nearest j <= p with A[j] >= S, along chain; A[0]=INF guarantees existence
        if A[p] >= S:
            return p
        for k in range(LOG - 1, -1, -1):
            q = upl[k][p]
            if A[q] < S:
                p = q
        return pl[p]

    def nearest_right(p, S):
        if A[p] >= S:
            return p
        for k in range(LOG - 1, -1, -1):
            q = upr[k][p]
            if A[q] < S:
                p = q
        return pr[p]

    out = []
    levels = list(range(LOG - 1, -1, -1))
    upl_r = upl[::-1]
    upr_r = upr[::-1]
    for K in range(1, n + 1):
        l = r = K
        S = A[K]
        while True:
            # nearest j <= l-1 with A[j] >= S
            p = l - 1
            if A[p] < S:
                for tb in upl_r:
                    q = tb[p]
                    if A[q] < S:
                        p = q
                p = pl[p]
            jl = p
            # nearest j >= r+1 with A[j] >= S
            p = r + 1
            if A[p] < S:
                for tb in upr_r:
                    q = tb[p]
                    if A[q] < S:
                        p = q
                p = pr[p]
            jr = p
            nl = jl + 1
            nr = jr - 1
            if nl == l and nr == r:
                break
            l, r = nl, nr
            S = P[r] - P[l - 1]
        out.append(S)
    sys.stdout.write(" ".join(map(str, out)) + "\n")

main()
