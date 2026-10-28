#!/usr/bin/env python3
import sys
import math

def next_power_of_two(x):
    return 1 << (x - 1).bit_length()

def fft(a, invert=False):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        ang = 2 * math.pi / length * (-1 if invert else 1)
        wlen = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n, length):
            w = 1+0j
            half = length // 2
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w
                a[j] = u + v
                a[j + half] = u - v
                w *= wlen
        length <<= 1
    if invert:
        for i in range(n):
            a[i] /= n

def convolution(a, b):
    # a and b are lists of ints (0/1)
    n = next_power_of_two(len(a) + len(b) - 1)
    fa = [complex(x, 0) for x in a] + [0j] * (n - len(a))
    fb = [complex(x, 0) for x in b] + [0j] * (n - len(b))
    fft(fa, False)
    fft(fb, False)
    for i in range(n):
        fa[i] *= fb[i]
    fft(fa, True)
    result = [int(round(fa[i].real)) for i in range(len(a) + len(b) - 1)]
    return result

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    vals = [int(next(it)) for _ in range(n)]
    max_val = max(vals)
    size = max_val + 1
    indicator = [0] * size
    for v in vals:
        indicator[v] = 1
    # convolution of indicator with itself
    conv = convolution(indicator, indicator)
    total = 0
    for b in vals:
        s = conv[2 * b]
        # s counts ordered pairs (a,c) with a+c=2b, including (b,b)
        total += (s - 1) // 2
    print(total)

if __name__ == "__main__":
    solve()
