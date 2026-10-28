import sys
from math import isqrt


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    target = sorted(s)
    limit = 10 ** n
    count = 0
    k_max = isqrt(limit - 1)
    for k in range(k_max + 1):
        t = str(k * k).zfill(n)
        if sorted(t) == target:
            count += 1
    print(count)


if __name__ == "__main__":
    main()
