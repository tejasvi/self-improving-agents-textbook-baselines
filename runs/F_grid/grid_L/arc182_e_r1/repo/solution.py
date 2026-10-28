import sys


def floor_sum(n, m, a, b):
    # sum_{i=0}^{n-1} floor((a*i + b) / m), a, b >= 0, m >= 1
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
    A = sorted(set(int(x) for x in data[4:4 + N]))
    n = len(A)

    def cnt(L):
        # number of k in [0,K) with (C*k mod M) >= L, for 0 <= L <= M
        return floor_sum(K, M, C, M - L) - floor_sum(K, M, C, 0)

    # sum of y_k = C*sum(k) - M*sum(floor(Ck/M))
    sum_y = C * (K * (K - 1) // 2) - M * floor_sum(K, M, C, 0)

    total = sum_y
    # region [0, M - a_n): min = y + a_1
    total += A[0] * (K - cnt(M - A[-1]))
    # region [M - a_j, U_j) with U_1 = M, U_j = M - a_{j-1}: min = y + a_j - M
    for j in range(n):
        lo = M - A[j]
        hi = M if j == 0 else M - A[j - 1]
        if lo >= hi:
            continue
        total += (A[j] - M) * (cnt(lo) - cnt(hi))
    print(total)


main()
