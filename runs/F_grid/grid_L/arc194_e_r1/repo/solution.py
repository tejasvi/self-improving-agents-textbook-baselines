import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    x = int(data[1])
    y = int(data[2])
    s = data[3]
    t = data[4]

    # Invariant: the sequence of (position mod X) over the 1s, and the
    # sequence of (position mod Y) over the 0s, must match exactly.
    def key(u):
        ones = [i % x for i, ch in enumerate(u) if ch == '1']
        zeros = [i % y for i, ch in enumerate(u) if ch == '0']
        return ones, zeros

    print("Yes" if key(s) == key(t) else "No")


if __name__ == "__main__":
    main()
