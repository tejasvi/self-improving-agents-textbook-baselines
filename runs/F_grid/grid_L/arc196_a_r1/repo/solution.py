import sys
import heapq


def prefix_values(arr):
    # res[m] = best score for arr[:m] when m is even (top half - bottom half), else None
    n = len(arr)
    res = [None] * (n + 1)
    lo = []  # max-heap (stored negated): smallest m//2 elements
    hi = []  # min-heap: remaining elements
    sum_lo = 0
    sum_hi = 0
    res[0] = 0
    for m in range(1, n + 1):
        x = arr[m - 1]
        # push into lo, then move max of lo to hi
        heapq.heappush(lo, -x)
        sum_lo += x
        y = -heapq.heappop(lo)
        sum_lo -= y
        heapq.heappush(hi, y)
        sum_hi += y
        target = m // 2
        if len(lo) < target:
            z = heapq.heappop(hi)
            sum_hi -= z
            heapq.heappush(lo, -z)
            sum_lo += z
        if m % 2 == 0:
            res[m] = sum_hi - sum_lo
    return res


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    if n % 2 == 0:
        pre = prefix_values(a)
        print(pre[n])
        return
    pre = prefix_values(a)
    suf_rev = prefix_values(a[::-1])  # suf_rev[k] = best for last k elements
    best = None
    # survivor at index i (0-based), i even; prefix length i, suffix length n-1-i
    for i in range(0, n, 2):
        left = pre[i]
        right = suf_rev[n - 1 - i]
        val = left + right
        if best is None or val > best:
            best = val
    print(best)


if __name__ == "__main__":
    main()
