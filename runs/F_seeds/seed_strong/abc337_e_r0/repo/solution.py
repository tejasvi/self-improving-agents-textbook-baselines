import sys


def main():
    n = int(sys.stdin.readline().strip())

    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    for j in range(m):
        group = [str(i + 1) for i in range(n) if (i >> j) & 1]
        out.append(" ".join([str(len(group))] + group))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    code = 0
    for j in range(m):
        if s[j] == "1":
            code |= 1 << j
    sys.stdout.write(str(code + 1) + "\n")
    sys.stdout.flush()


main()
