import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    out = []
    seq = [0] * n

    def dfs(i, lo):
        # choose seq[i] >= lo, such that remaining positions fit under m
        if i == n:
            out.append(' '.join(map(str, seq)))
            return
        remaining = n - 1 - i
        hi = m - 10 * remaining
        for v in range(lo, hi + 1):
            seq[i] = v
            dfs(i + 1, v + 10)

    dfs(0, 1)
    sys.stdout.write(str(len(out)) + "\n")
    if out:
        sys.stdout.write("\n".join(out) + "\n")


main()
