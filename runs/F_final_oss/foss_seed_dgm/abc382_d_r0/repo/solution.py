# Write your solution here. Read from stdin, write to stdout.
import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N, M = map(int, data)
    results = []
    seq = [0] * N
    def backtrack(idx, prev):
        if idx == N:
            results.append(seq.copy())
            return
        # Minimum value for this position
        min_val = 1 if idx == 0 else prev + 10
        # Remaining positions after this one
        rem = N - idx - 1
        # Maximum value such that we can still fit remaining positions
        max_val = M - 10 * rem
        if min_val > max_val:
            return
        for v in range(min_val, max_val + 1):
            seq[idx] = v
            backtrack(idx + 1, v)
    backtrack(0, 0)
    out_lines = []
    out_lines.append(str(len(results)))
    for r in results:
        out_lines.append(' '.join(map(str, r)))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    main()
