import sys


def main():
    n, m = map(int, sys.stdin.read().split())
    results = []
    seq = [0] * n

    def dfs(idx, lo):
        # idx: position to fill, lo: minimum allowed value
        remaining = n - idx - 1
        hi = m - 10 * remaining
        if idx == n:
            results.append(' '.join(map(str, seq)))
            return
        for v in range(lo, hi + 1):
            seq[idx] = v
            dfs(idx + 1, v + 10)

    dfs(0, 1)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write('\n'.join(out) + '\n')


main()
