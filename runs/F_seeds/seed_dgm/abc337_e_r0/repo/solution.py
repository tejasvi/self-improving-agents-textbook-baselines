import sys


def read_token_line():
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None  # EOF
        line = line.strip()
        if line:
            return line


def main():
    data = read_token_line()
    if data is None:
        return
    n = int(data)

    # Minimum M with 2^M >= n
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    for i in range(m):
        bottles = [j + 1 for j in range(n) if (j >> i) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = read_token_line()
    if s is None:
        return

    # Bit i of (X-1) is s[i]
    val = 0
    for i, c in enumerate(s):
        if c == "1":
            val |= (1 << i)
    x = val + 1

    sys.stdout.write(str(x) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
