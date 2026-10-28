import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    results = []
    seq = [0] * n

    def dfs(i, lo):
        # i: index (0-based) to fill, lo: minimum allowed value
        if i == n:
            results.append(' '.join(map(str, seq)))
            return
        remaining_after = n - i - 1
        hi = m - 10 * remaining_after
        v = lo
        while v <= hi:
            seq[i] = v
            dfs(i + 1, v + 10)
            v += 1

    dfs(0, 1)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write('\n'.join(out) + '\n')


main()
