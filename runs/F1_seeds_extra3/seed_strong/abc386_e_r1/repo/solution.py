import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    total = 0
    for x in a:
        total ^= x
    m = min(k, n - k)
    # f[j] = set of XOR values of j-subsets among processed elements
    f = [set() for _ in range(m + 1)]
    f[0].add(0)
    for i, v in enumerate(a):
        top = min(m, i + 1)
        for j in range(top, 0, -1):
            prev = f[j - 1]
            if prev:
                f[j].update([x ^ v for x in prev])
    vals = f[m]
    if k <= n - k:
        ans = max(vals)
    else:
        ans = max(total ^ x for x in vals)
    print(ans)


main()
