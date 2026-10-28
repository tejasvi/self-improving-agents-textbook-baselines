# Write your solution here. Read from stdin, write to stdout.
import sys

def main():
    # Read N (first line)
    line = sys.stdin.readline()
    if not line:
        return
    N = int(line.strip())
    # Minimum number of friends (bits) to differentiate N bottles
    M = 0
    while (1 << M) < N:
        M += 1
    # Output M
    sys.stdout.write(str(M) + "\n")
    # For each friend i (0-indexed), give bottles where i-th bit of (b-1) is 1
    for i in range(M):
        bottles = []
        for b in range(1, N + 1):
            if ((b - 1) >> i) & 1:
                bottles.append(b)
        # K_i followed by the bottle numbers
        line_parts = [str(len(bottles))] + [str(b) for b in bottles]
        sys.stdout.write(" ".join(line_parts) + "\n")
    sys.stdout.flush()
    # Read the judge's response string S of length M
    S = ''
    while len(S) < M:
        next_line = sys.stdin.readline()
        if not next_line:
            break
        S += next_line.strip()
    S = S[:M]
    # Decode the bottle number (0-indexed) from bits
    value = 0
    for i, ch in enumerate(S):
        if ch == '1':
            value |= (1 << i)
    X = value + 1  # convert to 1-indexed bottle number
    sys.stdout.write(str(X) + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
