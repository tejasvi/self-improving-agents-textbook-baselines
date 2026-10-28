import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    c0 = 0  # number of starts i <= j with f(i,j) == 0
    c1 = 0  # number of starts i <= j with f(i,j) == 1
    total = 0
    for ch in s:
        if ch == '0':
            c0, c1 = 1, c0 + c1
        else:
            c0, c1 = c1, c0 + 1
        total += c1
    print(total)


if __name__ == "__main__":
    main()
