import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    total = 0
    for x in a:
        total ^= x
    m = min(k, n - k)
    # f[j] = set of XOR values of j-subsets of processed prefix
    f = [set() for _ in range(m + 1)]
    f[0].add(0)
    for i, x in enumerate(a):
        top = min(i + 1, m)
        for j in range(top, 0, -1):
            prev = f[j - 1]
            if prev:
                cur = f[j]
                for v in prev:
                    cur.add(v ^ x)
    ys = f[m]
    if k <= n - k:
        ans = max(ys)
    else:
        ans = max(total ^ y for y in ys)
    print(ans)


main()
