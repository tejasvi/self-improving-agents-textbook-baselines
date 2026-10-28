import sys


def main():
    data = sys.stdin.readline().strip()
    while not data:
        data = sys.stdin.readline().strip()
    n = int(data)

    # Minimum friends: smallest M with 2^M >= N.
    m = 0
    while (1 << m) < n:
        m += 1

    out = [str(m)]
    # Friend j receives bottles whose 0-based index has bit j set.
    for j in range(m):
        bottles = [i + 1 for i in range(n) if (i >> j) & 1]
        out.append(" ".join([str(len(bottles))] + [str(b) for b in bottles]))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    idx = 0
    for j in range(m):
        if j < len(s) and s[j] == "1":
            idx |= 1 << j
    print(idx + 1, flush=True)


if __name__ == "__main__":
    main()
