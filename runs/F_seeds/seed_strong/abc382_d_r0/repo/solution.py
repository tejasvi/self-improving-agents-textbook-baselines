import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    out = []
    seq = [0] * n

    def dfs(pos, lo):
        # choose seq[pos] in [lo, m - 10*(n-1-pos)]
        if pos == n:
            out.append(' '.join(map(str, seq)))
            return
        hi = m - 10 * (n - 1 - pos)
        for v in range(lo, hi + 1):
            seq[pos] = v
            dfs(pos + 1, v + 10)

    dfs(0, 1)
    sys.stdout.write(str(len(out)) + '\n')
    if out:
        sys.stdout.write('\n'.join(out) + '\n')


main()
