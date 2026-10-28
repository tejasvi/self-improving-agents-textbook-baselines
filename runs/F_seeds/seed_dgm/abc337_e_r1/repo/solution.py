import sys


def main():
    data = sys.stdin.readline().strip()
    while data == "":
        line = sys.stdin.readline()
        if line == "":
            return
        data = line.strip()
    n = int(data)

    # Minimum friends: ceil(log2 n)
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    for j in range(m):
        # Bottles x (1-indexed) whose code (x-1) has bit j set
        group = [x for x in range(1, n + 1) if ((x - 1) >> j) & 1]
        out.append(" ".join([str(len(group))] + [str(x) for x in group]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    while s == "":
        line = sys.stdin.readline()
        if line == "":
            return
        s = line.strip()

    x = 0
    for j in range(m):
        if s[j] == "1":
            x |= 1 << j
    sys.stdout.write(str(x + 1) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
