import sys


def read_line():
    # Skip blank lines, but stop at EOF instead of spinning forever.
    while True:
        line = sys.stdin.readline()
        if line == "":
            return ""
        line = line.strip()
        if line:
            return line


def main():
    n = int(read_line())

    # Minimum number of friends: smallest m with 2^m >= n.
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    for j in range(m):
        group = [b for b in range(1, n + 1) if ((b - 1) >> j) & 1]
        out.append(" ".join([str(len(group))] + [str(b) for b in group]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = read_line()

    x = 0
    for j, ch in enumerate(s):
        if ch == "1":
            x |= 1 << j
    x += 1

    sys.stdout.write(str(x) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
