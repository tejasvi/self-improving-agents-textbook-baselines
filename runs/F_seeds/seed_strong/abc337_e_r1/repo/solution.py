import sys


def main():
    data = sys.stdin.readline().strip()
    while not data:
        data = sys.stdin.readline().strip()
    n = int(data)

    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    for j in range(m):
        # bottles 1..n, bottle b has code b-1; friend j gets those with bit j set
        bottles = [b for b in range(1, n + 1) if ((b - 1) >> j) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    while m > 0 and len(s) < m:
        # tolerate blank lines / whitespace quirks
        line = sys.stdin.readline()
        if not line:
            break
        s = line.strip()
    x = 0
    for j in range(m):
        if s[j] == "1":
            x |= 1 << j
    sys.stdout.write(str(x + 1) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
