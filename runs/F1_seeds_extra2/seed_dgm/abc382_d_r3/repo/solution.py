import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    results = []
    seq = [0] * n

    def dfs(i, lo):
        # Choose A_i (0-indexed i) with value >= lo.
        remaining = n - 1 - i  # values still needed after this one
        hi = m - 10 * remaining  # largest value so that the rest can fit
        for v in range(lo, hi + 1):
            seq[i] = v
            if i == n - 1:
                results.append(" ".join(map(str, seq)))
            else:
                dfs(i + 1, v + 10)

    dfs(0, 1)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write("\n".join(out) + "\n")


main()
