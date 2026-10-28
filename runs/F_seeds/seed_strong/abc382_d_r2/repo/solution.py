import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])

    results = []
    cur = [0] * N

    def dfs(i, lo):
        # choose A_i (0-indexed i) with value >= lo
        if i == N:
            results.append(' '.join(map(str, cur)))
            return
        remaining = N - 1 - i  # positions after i
        hi = M - 10 * remaining  # A_i must satisfy A_i + 10*remaining <= M
        for v in range(lo, hi + 1):
            cur[i] = v
            dfs(i + 1, v + 10)

    dfs(0, 1)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write('\n'.join(out) + '\n')


main()
