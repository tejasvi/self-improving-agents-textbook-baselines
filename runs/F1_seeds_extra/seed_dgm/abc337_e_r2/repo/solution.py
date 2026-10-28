import sys


def read_token_line():
    # Read the next non-empty line; return None on EOF.
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        line = line.strip()
        if line != "":
            return line


def main():
    line = read_token_line()
    if line is None:
        return
    n = int(line)

    # Minimum M with 2^M >= n
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    # Friend i gets every bottle x whose code (x-1) has bit i set.
    for i in range(m):
        group = [x for x in range(1, n + 1) if ((x - 1) >> i) & 1]
        out.append(" ".join([str(len(group))] + [str(x) for x in group]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = read_token_line()
    if s is None:
        return
    code = 0
    for i, ch in enumerate(s[:m]):
        if ch == "1":
            code |= 1 << i
    sys.stdout.write(str(code + 1) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
