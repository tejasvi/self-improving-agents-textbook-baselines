# Write your solution here. Read from stdin, write to stdout.

import sys
import math

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    # First value is N
    N = int(data[0])
    # Compute minimal number of friends M = ceil(log2 N)
    M = (N - 1).bit_length()  # works for N>=1
    out_lines = []
    out_lines.append(str(M))
    # For each friend i (0-index), give bottles whose (index-1) has i-th bit set
    for i in range(M):
        bottles = [str(b) for b in range(1, N + 1) if ((b - 1) >> i) & 1]
        K = len(bottles)
        line = str(K)
        if K:
            line += " " + " ".join(bottles)
        out_lines.append(line)
    # Print the queries
    sys.stdout.write("\n".join(out_lines) + "\n")
    sys.stdout.flush()
    # After printing queries, the judge will provide a string S of length M
    # Read the next token from input (the remaining part after N)
    # If S was already read (e.g., provided on same line), it will be data[1]
    # Otherwise, read from stdin again.
    # The remaining tokens after the first are either the S string or nothing.
    if len(data) >= 2:
        S = data[1].strip()
    else:
        # read next line
        S = sys.stdin.readline().strip()
    # Ensure S length is M; if not, pad with zeros (should not happen)
    if len(S) < M:
        S = S.ljust(M, '0')
    # Decode X (0-indexed)
    X_idx = 0
    for i, ch in enumerate(S):
        if ch == '1':
            X_idx |= (1 << i)
    X = X_idx + 1
    sys.stdout.write(str(X) + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
