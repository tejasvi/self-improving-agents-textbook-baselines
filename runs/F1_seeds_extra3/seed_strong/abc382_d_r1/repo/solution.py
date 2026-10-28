import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    out = []
    cur = [0] * n

    def dfs(i, lo):
        # choose A_i (0-indexed i) with value in [lo, M - 10*(N-1-i)]
        if i == n:
            out.append(' '.join(map(str, cur)))
            return
        hi = m - 10 * (n - 1 - i)
        for v in range(lo, hi + 1):
            cur[i] = v
            dfs(i + 1, v + 10)

    dfs(0, 1)
    sys.stdout.write(str(len(out)) + '\n')
    if out:
        sys.stdout.write('\n'.join(out) + '\n')


main()
