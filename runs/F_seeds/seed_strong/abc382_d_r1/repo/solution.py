import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    out = []
    seq = [0] * n
    count = 0

    # Iterative-style recursion; depth at most 12.
    def dfs(i, lo):
        nonlocal count
        if i == n:
            count += 1
            out.append(' '.join(map(str, seq)))
            return
        remaining = n - 1 - i  # elements still to place after this one
        hi = m - 10 * remaining
        for v in range(lo, hi + 1):
            seq[i] = v
            dfs(i + 1, v + 10)

    dfs(0, 1)
    sys.stdout.write(str(count) + "\n" + "\n".join(out) + ("\n" if out else ""))


main()
