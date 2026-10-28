import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    results = []
    cur = []

    def dfs(last, depth):
        # depth: number of elements already chosen
        if depth == n:
            results.append(' '.join(map(str, cur)))
            return
        remaining_after = n - depth - 1
        if depth == 0:
            lo = 1
        else:
            lo = last + 10
        hi = m - 10 * remaining_after
        for v in range(lo, hi + 1):
            cur.append(v)
            dfs(v, depth + 1)
            cur.pop()

    dfs(0, 0)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write('\n'.join(out) + '\n')


main()
