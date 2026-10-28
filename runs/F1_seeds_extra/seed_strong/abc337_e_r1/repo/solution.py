import sys


def main():
    data = sys.stdin.readline().strip()
    while data == "":
        data = sys.stdin.readline().strip()
    n = int(data)

    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    for i in range(m):
        bottles = [x + 1 for x in range(n) if (x >> i) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()

    x = 0
    for i, c in enumerate(s):
        if c == "1":
            x |= 1 << i
    sys.stdout.write(str(x + 1) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
