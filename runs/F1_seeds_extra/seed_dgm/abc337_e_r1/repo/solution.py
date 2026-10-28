import sys


def main():
    data = sys.stdin.readline().strip()
    while data == "":
        line = sys.stdin.readline()
        if not line:
            return
        data = line.strip()
    n = int(data)

    # Minimum M with 2^M >= n
    m = 0
    while (1 << m) < n:
        m += 1

    out = sys.stdout
    out.write(f"{m}\n")
    for j in range(m):
        # Bottles x (1-indexed) whose code (x-1) has bit j set
        bottles = [x for x in range(1, n + 1) if ((x - 1) >> j) & 1]
        out.write(str(len(bottles)) + " " + " ".join(map(str, bottles)) + "\n")
    out.flush()

    s = sys.stdin.readline().strip()
    while s == "":
        line = sys.stdin.readline()
        if not line:
            return
        s = line.strip()

    code = 0
    for j in range(m):
        if s[j] == "1":
            code |= 1 << j
    out.write(f"{code + 1}\n")
    out.flush()


if __name__ == "__main__":
    main()
