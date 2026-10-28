import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    c0 = 0  # number of starts whose current value is 0
    c1 = 0  # number of starts whose current value is 1
    total = 0
    for ch in s:
        if ch == '0':
            c1 = c0 + c1
            c0 = 1
        else:
            c0, c1 = c1, c0
            c1 += 1
        total += c1
    print(total)


main()
