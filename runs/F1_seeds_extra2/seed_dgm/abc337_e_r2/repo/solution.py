import sys


def main():
    data = sys.stdin.readline().strip()
    while data == "":
        data = sys.stdin.readline().strip()
    n = int(data)

    # Minimum number of friends: smallest m with 2^m >= n.
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    for i in range(m):
        bottles = [x for x in range(1, n + 1) if ((x - 1) >> i) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    while s == "" :
        s = sys.stdin.readline().strip()

    code = 0
    for i, ch in enumerate(s[:m]):
        if ch == "1":
            code |= 1 << i

    sys.stdout.write(str(code + 1) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
