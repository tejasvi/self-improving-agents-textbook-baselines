import sys


def floor_sum(n, m, a, b):
    # sum_{i=0}^{n-1} floor((a*i+b)/m), with 0<=a,b (ACL-style)
    ans = 0
    while True:
        if a >= m:
            ans += (n - 1) * n // 2 * (a // m)
            a %= m
        if b >= m:
            ans += n * (b // m)
            b %= m
        y_max = a * n + b
        if y_max < m:
            break
        n, b = y_max // m, y_max % m
        m, a = a, m
    return ans


def main():
    data = sys.stdin.read().split()
    N, M, C, K = int(data[0]), int(data[1]), int(data[2]), int(data[3])
    A = sorted(set(int(v) for v in data[4:4 + N]))
    n = len(A)  # A[0]=a_1 ... A[n-1]=a_n

    S0 = floor_sum(K, M, C, 0)  # sum floor(Ck/M)

    def G(X):
        # number of k in [0,K) with (Ck mod M) >= X, for X in [0,M]
        return floor_sum(K, M, C, M - X) - S0

    sum_x = C * K * (K - 1) // 2 - M * S0

    # pieces: [0, M-a_n) offset a_1; [M-a_t, M-a_{t-1}) offset a_t - M (t=n..2);
    # [M-a_1, M) offset a_1 - M
    total = sum_x
    # piece 0
    L, R = 0, M - A[n - 1]
    total += A[0] * (G(L) - G(R))
    for t in range(n, 0, -1):
        # a_t = A[t-1]
        L = M - A[t - 1]
        R = M if t == 1 else M - A[t - 2]
        total += (A[t - 1] - M) * (G(L) - G(R))
    print(total)


main()
