import sys


def main():
    data = sys.stdin.readline().strip()
    while not data:
        line = sys.stdin.readline()
        if not line:
            return
        data = line.strip()
    n = int(data)

    # Minimum number of friends: smallest M with 2^M >= n.
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    # Bottle b (1-indexed) is encoded by value b-1 in binary.
    # Friend j receives every bottle whose bit j of (b-1) is set.
    for j in range(m):
        bottles = [b for b in range(1, n + 1) if ((b - 1) >> j) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    value = 0
    for j, ch in enumerate(s):
        if ch == "1":
            value |= 1 << j
    print(value + 1, flush=True)


if __name__ == "__main__":
    main()
