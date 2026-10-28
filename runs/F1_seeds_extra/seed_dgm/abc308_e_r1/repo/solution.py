import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    s = data[1 + n]

    def mex3(x, y, z):
        st = {x, y, z}
        for v in range(3):
            if v not in st:
                return v
        return 3

    mx = [[[mex3(x, y, z) for z in range(3)] for y in range(3)] for x in range(3)]

    pm = [0, 0, 0]  # counts of M values at positions before current j
    sx = [0, 0, 0]  # counts of X values at positions after current j
    for i in range(n):
        if s[i] == 'X':
            sx[a[i]] += 1
    total = 0
    for j in range(n):
        c = s[j]
        if c == 'M':
            pm[a[j]] += 1
        elif c == 'X':
            sx[a[j]] -= 1
        else:  # 'E'
            ej = a[j]
            for x in range(3):
                if pm[x] == 0:
                    continue
                for z in range(3):
                    if sx[z] == 0:
                        continue
                    total += pm[x] * sx[z] * mx[x][ej][z]
    print(total)


main()
