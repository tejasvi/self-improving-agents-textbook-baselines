import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    A = [int(x) for x in data[2:2 + n]]
    vals = sorted(set(A))
    m = len(vals)
    rank = {v: i + 1 for i, v in enumerate(vals)}  # 1-based

    # Step 1: dp[i] = LIS length ending at i (strictly increasing)
    tree = [0] * (m + 1)
    dp = [0] * n
    for i in range(n):
        r = rank[A[i]]
        # prefix max over ranks < r
        best = 0
        j = r - 1
        while j > 0:
            if tree[j] > best:
                best = tree[j]
            j -= j & -j
        d = best + 1
        dp[i] = d
        j = r
        while j <= m:
            if tree[j] < d:
                tree[j] = d
            j += j & -j

    # Step 2: offline queries sorted by R
    queries = []
    idx = 2 + n
    for k in range(q):
        R = int(data[idx])
        X = int(data[idx + 1])
        idx += 2
        queries.append((R, X, k))
    queries.sort()

    tree = [0] * (m + 1)
    ans = [0] * q
    p = 0  # number of elements inserted (prefix length)
    for R, X, k in queries:
        while p < R:
            r = rank[A[p]]
            d = dp[p]
            j = r
            while j <= m:
                if tree[j] < d:
                    tree[j] = d
                j += j & -j
            p += 1
        # query over values <= X
        t = bisect_right(vals, X)
        best = 0
        j = t
        while j > 0:
            if tree[j] > best:
                best = tree[j]
            j -= j & -j
        ans[k] = best

    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
