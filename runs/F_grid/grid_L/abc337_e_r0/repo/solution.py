import sys


def main():
    data = sys.stdin
    n = int(data.readline().strip())

    # Minimum friends: ceil(log2(n)), using binary codes of bottle indices (0-based).
    m = 0
    while (1 << m) < n:
        m += 1

    out = sys.stdout
    out.write(f"{m}\n")

    for j in range(m):
        bottles = [i + 1 for i in range(n) if (i >> j) & 1]
        out.write(str(len(bottles)) + " " + " ".join(map(str, bottles)) + "\n")
    out.flush()

    s = data.readline().strip()
    code = 0
    for j, ch in enumerate(s):
        if ch == "1":
            code |= 1 << j
    out.write(f"{code + 1}\n")
    out.flush()


if __name__ == "__main__":
    main()
