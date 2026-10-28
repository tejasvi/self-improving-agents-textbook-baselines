#!/usr/bin/env python3
import sys

def main():
    # Read N (first line)
    line = sys.stdin.readline()
    if not line:
        return
    N = int(line.strip())
    # Minimum number of friends needed: ceil(log2 N)
    M = (N - 1).bit_length()
    out = []
    out.append(str(M))
    # Build plan: for each friend i, give bottles where i-th bit of (b-1) is 1
    for i in range(M):
        bottles = [str(b) for b in range(1, N + 1) if ((b - 1) >> i) & 1]
        line = str(len(bottles))
        if bottles:
            line += ' ' + ' '.join(bottles)
        out.append(line)
    sys.stdout.write('\n'.join(out) + '\n')
    sys.stdout.flush()
    # Read the judge's response string S
    S = sys.stdin.readline().strip()
    # In case of empty line (e.g., extra newlines), keep reading
    while S == '' and not sys.stdin.closed:
        nxt = sys.stdin.readline()
        if not nxt:
            break
        S = nxt.strip()
    # Ensure S has length M (pad with '0' if missing)
    if len(S) < M:
        S = S.ljust(M, '0')
    # Decode the spoiled bottle number (0-indexed bits)
    value = 0
    for i, ch in enumerate(S[:M]):
        if ch == '1':
            value |= (1 << i)
    X = value + 1
    # Clamp to valid range just in case
    if X < 1:
        X = 1
    if X > N:
        X = N
    sys.stdout.write(str(X) + '\n')
    sys.stdout.flush()

if __name__ == "__main__":
    main()
