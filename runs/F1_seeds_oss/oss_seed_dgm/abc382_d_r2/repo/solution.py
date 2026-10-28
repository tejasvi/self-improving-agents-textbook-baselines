# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N, M = map(int, data)
    result = []
    seq = [0] * N
    def dfs(i, prev):
        # i is 0-indexed position to fill
        if i == N:
            result.append(seq.copy())
            return
        # compute lower and upper bounds for this position
        if i == 0:
            lower = 1
        else:
            lower = prev + 10
        # ensure enough room for remaining positions
        # remaining positions after this one: N - i - 1, each needs +10 at least
        upper = M - (N - i - 1) * 10
        if i == N - 1:
            upper = M
        # if bounds invalid, prune
        if lower > upper:
            return
        for val in range(lower, upper + 1):
            seq[i] = val
            dfs(i + 1, val)
    dfs(0, 0)
    out_lines = [str(len(result))]
    for s in result:
        out_lines.append(' '.join(map(str, s)))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
