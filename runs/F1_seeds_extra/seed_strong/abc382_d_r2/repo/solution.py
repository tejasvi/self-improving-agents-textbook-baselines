import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    out = []
    seq = [0] * n
    count = 0

    def dfs(i, lo):
        nonlocal count
        # position i (0-indexed); value must be >= lo and <= m - 10*(n-1-i)
        hi = m - 10 * (n - 1 - i)
        if i == n:
            count += 1
            out.append(' '.join(map(str, seq)))
            return
        for v in range(lo, hi + 1):
            seq[i] = v
            dfs(i + 1, v + 10)

    dfs(0, 1)
    sys.stdout.write(str(count) + '\n' + ('\n'.join(out) + '\n' if out else ''))


main()
