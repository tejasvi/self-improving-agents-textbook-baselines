import sys


def main():
    data = sys.stdin.readline().strip()
    n = int(data)

    # Minimum number of friends: ceil(log2 n)
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    # Friend j receives every bottle whose 0-indexed id has bit j set.
    for j in range(m):
        bottles = [i + 1 for i in range(n) if (i >> j) & 1]
        out.append(str(len(bottles)) + (" " + " ".join(map(str, bottles)) if bottles else ""))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    x = 0
    for j, c in enumerate(s):
        if c == "1":
            x |= 1 << j
    sys.stdout.write(str(x + 1) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
