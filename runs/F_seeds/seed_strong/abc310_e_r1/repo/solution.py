import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    c0 = 0  # count of starts i<j with f(i,j-1)=0
    c1 = 0  # count of starts i<j with f(i,j-1)=1
    total = 0
    for ch in s:
        if ch == '0':
            # all previous become 1
            c1 = c0 + c1
            c0 = 1  # new start i=j with value 0
        else:
            # all previous flip
            c0, c1 = c1, c0
            c1 += 1  # new start i=j with value 1
        total += c1
    print(total)


main()
