import sys


def main():
    data = sys.stdin.readline().strip()
    n = int(data)

    # Minimum friends: smallest M with 2^M >= N.
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    # Bottle b (1..N) has binary code b-1; friend j receives bottles whose bit j is 1.
    for j in range(m):
        bottles = [b for b in range(1, n + 1) if ((b - 1) >> j) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    code = 0
    for j, ch in enumerate(s[:m]):
        if ch == "1":
            code |= 1 << j
    sys.stdout.write(str(code + 1) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
