import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    out = []
    cur = [0] * n

    def dfs(idx, lo):
        # lo: smallest allowed value for position idx
        if idx == n:
            out.append(' '.join(map(str, cur)))
            return
        remaining = n - idx - 1
        hi = m - 10 * remaining
        for v in range(lo, hi + 1):
            cur[idx] = v
            dfs(idx + 1, v + 10)

    dfs(0, 1)
    sys.stdout.write(str(len(out)) + "\n")
    if out:
        sys.stdout.write("\n".join(out) + "\n")


main()
