import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    results = []
    seq = []

    def dfs(prev, depth):
        # depth = number of elements already chosen
        if depth == n:
            results.append(' '.join(map(str, seq)))
            return
        remaining = n - depth - 1  # elements still to place after this one
        start = 1 if depth == 0 else prev + 10
        # value v must satisfy v + 10*remaining <= m
        v = start
        while v + 10 * remaining <= m:
            seq.append(v)
            dfs(v, depth + 1)
            seq.pop()
            v += 1

    dfs(0, 0)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write('\n'.join(out) + '\n')


main()
