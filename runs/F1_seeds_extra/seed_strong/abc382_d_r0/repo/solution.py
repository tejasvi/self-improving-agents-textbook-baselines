import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    out = []
    cur = [0] * N

    def dfs(i, lo):
        # choose A[i] (0-indexed) with value >= lo
        remaining = N - 1 - i  # elements after position i
        hi = M - 10 * remaining
        if i == N:
            out.append(' '.join(map(str, cur)))
            return
        for v in range(lo, hi + 1):
            cur[i] = v
            dfs(i + 1, v + 10)

    dfs(0, 1)
    sys.stdout.write(str(len(out)) + "\n")
    if out:
        sys.stdout.write("\n".join(out) + "\n")


main()
