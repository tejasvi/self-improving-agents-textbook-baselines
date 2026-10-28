import sys


def main():
    data = sys.stdin.readline().strip()
    while not data:
        line = sys.stdin.readline()
        if not line:
            return
        data = line.strip()
    n = int(data)

    # Minimum friends: smallest M with 2^M >= n.
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    # Friend j receives every bottle (1-based number b) whose 0-based index
    # i = b - 1 has bit j set. Friend j is sick iff bit j of X-1 is 1.
    for j in range(m):
        bottles = [i + 1 for i in range(n) if (i >> j) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    idx = 0
    for j, ch in enumerate(s[:m]):
        if ch == "1":
            idx |= (1 << j)
    x = idx + 1

    sys.stdout.write(str(x) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
