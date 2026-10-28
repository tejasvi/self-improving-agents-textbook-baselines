import sys


def main():
    data = sys.stdin.readline().strip()
    while not data:
        line = sys.stdin.readline()
        if not line:
            return
        data = line.strip()
    n = int(data)

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
    while not s:
        line = sys.stdin.readline()
        if not line:
            return
        s = line.strip()

    val = 0
    for i, c in enumerate(s):
        if c == "1":
            val |= 1 << i
    sys.stdout.write(str(val + 1) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
