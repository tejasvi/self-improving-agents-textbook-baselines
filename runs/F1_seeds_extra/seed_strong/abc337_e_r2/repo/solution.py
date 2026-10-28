import sys


def main():
    data = sys.stdin.readline().strip()
    n = int(data)
    m = 0
    while (1 << m) < n:
        m += 1
    out = [str(m)]
    for i in range(m):
        # friend i gets bottles j (1-based) whose (j-1) has bit i set
        group = [j for j in range(1, n + 1) if ((j - 1) >> i) & 1]
        out.append(" ".join([str(len(group))] + [str(j) for j in group]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()
    s = sys.stdin.readline().strip()
    x = 0
    for i, c in enumerate(s):
        if c == "1":
            x |= 1 << i
    print(x + 1, flush=True)


if __name__ == "__main__":
    main()
