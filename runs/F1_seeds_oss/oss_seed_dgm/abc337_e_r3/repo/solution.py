# Write your solution here. Read from stdin, write to stdout.

import sys

def main():
    # Read N (the number of bottles)
    line = sys.stdin.readline()
    if not line:
        return
    N = int(line.strip())

    # Minimum number of friends needed is ceil(log2 N)
    M = (N - 1).bit_length()
    out = []
    out.append(str(M))
    # Build each friend's set using binary representation of (bottle-1)
    for i in range(M):
        subset = [str(b) for b in range(1, N + 1) if ((b - 1) >> i) & 1]
        out.append(str(len(subset)) + (" " + " ".join(subset) if subset else ""))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    # Read the judge's response string S (length M)
    S = sys.stdin.readline().strip()
    # In case the judge sends the string without a newline (unlikely), fallback to reading remaining tokens
    if len(S) < M:
        extra = sys.stdin.read().strip().split()
        if extra:
            S = extra[0]
    # Decode the bottle index from the bits (0‑based)
    idx = 0
    for i, ch in enumerate(S[:M]):
        if ch == '1':
            idx |= (1 << i)
    X = idx + 1
    # Clamp to valid range just in case
    if X < 1:
        X = 1
    if X > N:
        X = N
    sys.stdout.write(str(X) + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
