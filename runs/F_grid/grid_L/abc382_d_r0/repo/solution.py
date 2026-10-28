import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    results = []
    seq = [0] * n

    def dfs(i, lo):
        # Position i (0-indexed) must be >= lo; must leave room for remaining elements.
        hi = m - 10 * (n - 1 - i)
        for v in range(lo, hi + 1):
            seq[i] = v
            if i == n - 1:
                results.append(' '.join(map(str, seq)))
            else:
                dfs(i + 1, v + 10)

    dfs(0, 1)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
