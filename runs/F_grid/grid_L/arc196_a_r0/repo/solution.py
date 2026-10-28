import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]

    # Unique ranks 1..n (ties broken by index).
    order = sorted(range(n), key=lambda i: a[i])
    rank = [0] * n
    for r, i in enumerate(order, 1):
        rank[i] = r
    LOG = 1
    while (1 << LOG) <= n:
        LOG += 1

    def run(indices):
        """Yield f(set) after each addition, where f = sum(top half) - sum(bottom half)
        for the even-sized multiset added so far; returns dict size->f for even sizes."""
        cnt = [0] * (n + 1)
        sm = [0] * (n + 1)
        total = 0
        size = 0
        res = {}
        for i in indices:
            r = rank[i]
            v = a[i]
            total += v
            size += 1
            p = r
            while p <= n:
                cnt[p] += 1
                sm[p] += v
                p += p & -p
            if size % 2 == 0:
                m = size // 2
                # sum of smallest m elements
                pos = 0
                acc_c = 0
                acc_s = 0
                step = 1 << LOG
                while step:
                    np_ = pos + step
                    if np_ <= n and acc_c + cnt[np_] <= m:
                        pos = np_
                        acc_c += cnt[np_]
                        acc_s += sm[np_]
                    step >>= 1
                # acc_c == m here since ranks are unique and present
                res[size] = total - 2 * acc_s
        return res

    if n % 2 == 0:
        pre = run(range(n))
        print(pre[n])
        return

    # n odd: remove a leftover element at 0-indexed k (k even), split into
    # prefix A[0..k-1] and suffix A[k+1..n-1], both must be even-length.
    pre = run(range(n))  # pre[L] = f(A[0..L-1]) for even L
    suf_rev = run(range(n - 1, -1, -1))  # suf_rev[L] = f(A[n-L..n-1]) for even L
    best = 0
    for k in range(0, n, 2):
        left = pre.get(k, 0) if k > 0 else 0
        rlen = n - 1 - k
        right = suf_rev.get(rlen, 0) if rlen > 0 else 0
        best = max(best, left + right)
    print(best)


main()
