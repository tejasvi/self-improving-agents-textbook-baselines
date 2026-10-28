import sys


def main():
    data = sys.stdin.readline().strip()
    while not data:
        data = sys.stdin.readline().strip()
    n = int(data)

    # Minimum number of friends: smallest M with 2^M >= N.
    m = 0
    while (1 << m) < n:
        m += 1

    # Friend j receives every bottle i (1-indexed) whose 0-indexed value
    # (i-1) has bit j set.
    out = [str(m)]
    for j in range(m):
        bottles = [i + 1 for i in range(n) if (i >> j) & 1]
        out.append(str(len(bottles)) + " " + " ".join(map(str, bottles)))
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

    s = sys.stdin.readline().strip()
    while not s:
        s = sys.stdin.readline().strip()

    # Upset friends encode the spoiled bottle's 0-indexed value in binary.
    x = 0
    for j in range(m):
        if s[j] == "1":
            x |= (1 << j)
    print(x + 1)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
