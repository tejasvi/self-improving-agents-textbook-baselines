import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    best = 0
    # A valid subarray consists of consecutive "units" (pairs of equal adjacent
    # elements) starting at positions of the same parity, with pairwise distinct
    # values. Process each parity class independently with a sliding window.
    for p in (0, 1):
        left = 0
        last = {}
        t = 0
        j = p
        while j + 1 < n:
            if a[j] != a[j + 1]:
                left = t + 1
            else:
                v = a[j]
                lv = last.get(v)
                if lv is not None and lv >= left:
                    left = lv + 1
                last[v] = t
                length = 2 * (t - left + 1)
                if length > best:
                    best = length
            t += 1
            j += 2
    print(best)


main()
