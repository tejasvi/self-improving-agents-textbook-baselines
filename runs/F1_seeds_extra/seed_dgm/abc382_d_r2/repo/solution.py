import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])

    results = []
    seq = []

    def dfs(prev, depth):
        remaining = N - depth  # elements still to place, including this one
        if depth == N:
            results.append(' '.join(map(str, seq)))
            return
        # smallest allowed value for this position
        lo = 1 if prev is None else prev + 10
        # must leave room: v + 10*(remaining-1) <= M
        hi = M - 10 * (remaining - 1)
        for v in range(lo, hi + 1):
            seq.append(v)
            dfs(v, depth + 1)
            seq.pop()

    dfs(None, 0)
    out = [str(len(results))]
    out.extend(results)
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
