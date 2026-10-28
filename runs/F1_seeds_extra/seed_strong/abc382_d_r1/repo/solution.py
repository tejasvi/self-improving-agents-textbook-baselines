import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    res = []
    cur = [0] * N

    def dfs(i, lo):
        # place position i with value >= lo
        if i == N:
            res.append(' '.join(map(str, cur)))
            return
        remaining = N - 1 - i
        hi = M - 10 * remaining
        for v in range(lo, hi + 1):
            cur[i] = v
            dfs(i + 1, v + 10)

    dfs(0, 1)
    out = [str(len(res))]
    out.extend(res)
    sys.stdout.write('\n'.join(out) + '\n')


main()
