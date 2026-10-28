# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    # Minimal number of friends needed is ceil(log2 N)
    M = (N - 1).bit_length()
    # Prepare plan lines
    lines = [str(M)]
    for i in range(M):
        bottles = [str(b) for b in range(1, N + 1) if ((b - 1) >> i) & 1]
        if bottles:
            lines.append(str(len(bottles)) + " " + " ".join(bottles))
        else:
            lines.append("0")
    # Output the plan
    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()

    # The judge (offline version) provides the response string S next in the input
    S = ""
    if len(data) >= 2:
        S = data[1].strip()
    # Decode the spoiled bottle number from the bits
    value = 0
    for i, ch in enumerate(S):
        if ch == '1':
            value |= (1 << i)
    X = value + 1 if S else 1  # default to 1 if S is empty (should not happen)
    sys.stdout.write(str(X) + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
