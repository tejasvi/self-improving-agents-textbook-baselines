import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    results = []
    seq = [0] * n

    def dfs(i, lo):
        # choose seq[i] in [lo, m - 10*(n-1-i)]
        if i == n:
            results.append(' '.join(map(str, seq)))
            return
        hi = m - 10 * (n - 1 - i)
        for v in range(lo, hi + 1):
            seq[i] = v
            dfs(i + 1, v + 10)

    dfs(0, 1)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write('\n'.join(out) + '\n')


main()
