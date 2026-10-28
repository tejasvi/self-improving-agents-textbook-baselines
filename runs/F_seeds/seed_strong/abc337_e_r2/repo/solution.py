import sys


def main():
    data = sys.stdin.readline().split()
    n = int(data[0])
    m = (n - 1).bit_length()
    out = [str(m)]
    for i in range(m):
        bottles = [j for j in range(1, n + 1) if ((j - 1) >> i) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    x = 1
    for i, c in enumerate(s):
        if c == "1":
            x += 1 << i
    sys.stdout.write(str(x) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
