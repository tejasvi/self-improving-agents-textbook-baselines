import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = []
    B = []
    for i in range(n):
        A.append(int(data[1 + 2 * i]))
        B.append(int(data[2 + 2 * i]))
    S = sum(B)
    if S % 3 != 0:
        print(-1)
        return
    T = S // 3
    W = T + 1
    # bitset index: s1 * W + s2, with 0 <= s1, s2 <= T
    FULL = 0
    for s1 in range(W):
        FULL |= ((1 << W) - 1) << (s1 * W)
    # M2[b]: states with s2 + b <= T (and s1 <= T)
    M2 = {}

    def get_m2(b):
        if b in M2:
            return M2[b]
        if b > T:
            m = 0
        else:
            row = (1 << (T - b + 1)) - 1
            m = 0
            for s1 in range(W):
                m |= row << (s1 * W)
        M2[b] = m
        return m

    # layers[k]: bitset of states reachable with exactly k moves so far
    INF_LAYER = 0
    layers = [0] * (n + 2)
    layers[0] = 1  # state (0,0)
    for i in range(n):
        a = A[i] - 1
        b = B[i]
        new = [0] * (n + 2)
        m2 = get_m2(b)
        sh1 = b * W
        for k in range(i + 1):
            L = layers[k]
            if not L:
                continue
            for t in range(3):
                c = 0 if t == a else 1
                if t == 0:
                    X = (L << sh1) & FULL
                elif t == 1:
                    X = (L & m2) << b
                else:
                    X = L
                new[k + c] |= X
        layers = new
    target = T * W + T
    for k in range(n + 1):
        if (layers[k] >> target) & 1:
            print(k)
            return
    print(-1)


main()
