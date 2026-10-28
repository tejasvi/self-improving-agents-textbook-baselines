# Write your solution here. Read from stdin, write to stdout.
import sys

def generate_sequences(N, M):
    result = []
    seq = [0] * N
    def backtrack(idx, prev):
        # idx: current position (0-indexed)
        if idx == N:
            result.append(seq.copy())
            return
        # lower bound for this position
        low = max(1, prev + 10) if idx > 0 else 1
        # upper bound to allow remaining positions
        remaining = N - idx - 1
        high = M - 10 * remaining
        if low > high:
            return
        for v in range(low, high + 1):
            seq[idx] = v
            backtrack(idx + 1, v)
    backtrack(0, 0)
    return result

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N, M = map(int, data[:2])
    sequences = generate_sequences(N, M)
    out_lines = [str(len(sequences))]
    for s in sequences:
        out_lines.append(' '.join(map(str, s)))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    main()
