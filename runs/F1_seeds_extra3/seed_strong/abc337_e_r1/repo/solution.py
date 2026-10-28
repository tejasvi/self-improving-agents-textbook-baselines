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
    for j in range(m):
        bottles = [i for i in range(1, n + 1) if ((i - 1) >> j) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()
    s = sys.stdin.readline().strip()
    code = 0
    for j, ch in enumerate(s):
        if ch == "1":
            code |= 1 << j
    print(code + 1)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
