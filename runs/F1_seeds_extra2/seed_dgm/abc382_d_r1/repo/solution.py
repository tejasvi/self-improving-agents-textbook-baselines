import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    results = []
    seq = [0] * n

    def dfs(i, lo):
        # choose A_i (index i, 0-based) with value >= lo
        if i == n:
            results.append(' '.join(map(str, seq)))
            return
        remaining = n - 1 - i  # elements still to place after this one
        hi = m - 10 * remaining
        for v in range(lo, hi + 1):
            seq[i] = v
            dfs(i + 1, v + 10)

    dfs(0, 1)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
