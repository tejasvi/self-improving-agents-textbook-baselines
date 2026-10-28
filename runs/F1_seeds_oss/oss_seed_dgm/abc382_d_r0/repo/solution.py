# Write your solution here. Read from stdin, write to stdout.

import sys

def generate_sequences(N, M):
    sequences = []
    def dfs(idx, prev, current):
        # idx: number of elements already placed
        if idx == N:
            sequences.append(current[:])
            return
        # Determine lower bound for this position
        if idx == 0:
            lower = 1
        else:
            lower = prev + 10
        # Remaining positions after this one
        remaining = N - idx - 1
        # Upper bound so that we can still place remaining elements up to M
        max_allowed = M - 10 * remaining
        # If lower > max_allowed, no valid continuation
        if lower > max_allowed:
            return
        for val in range(lower, max_allowed + 1):
            current.append(val)
            dfs(idx + 1, val, current)
            current.pop()
    dfs(0, 0, [])
    return sequences

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N, M = map(int, data)
    seqs = generate_sequences(N, M)
    out = []
    out.append(str(len(seqs)))
    for s in seqs:
        out.append(' '.join(map(str, s)))
    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    main()
