# Fine Triplets solution using NTT convolution
import sys

MOD = 998244353  # 119 * 2^23 + 1, suitable for NTT
ROOT = 3  # primitive root modulo MOD

def ntt(a, invert=False):
    n = len(a)
    j = 0
    # Bit-reversal permutation
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
        wlen = pow(ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length // 2
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a, b):
    n = 1
    total_len = len(a) + len(b) - 1
    while n < total_len:
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:total_len]

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    nums = list(map(int, data[1:1 + n]))
    if n < 3:
        print(0)
        return
    max_val = max(nums)
    size = 1
    while size <= 2 * max_val:
        size <<= 1
    # indicator array
    a = [0] * size
    for x in nums:
        a[x] = 1
    # convolution of a with itself
    conv = convolution(a, a)
    total = 0
    # conv length is at most 2*max_val+1
    for b in nums:
        pairs = conv[2 * b]
        # subtract the (b,b) pair and divide by 2 for unordered distinct pairs
        total += (pairs - 1) // 2
    print(total)

if __name__ == "__main__":
    main()
