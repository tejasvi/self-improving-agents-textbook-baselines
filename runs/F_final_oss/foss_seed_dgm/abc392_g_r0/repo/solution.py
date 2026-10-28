# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    arr = list(map(int, data[1:1 + n]))
    max_val = max(arr)
    # Determine size for FFT (next power of two >= 2*max_val)
    size = 1
    while size <= 2 * max_val:
        size <<= 1
    try:
        import numpy as np
    except ImportError:
        # Fallback: simple O(N * sqrt(max_val)) method (unlikely to be needed)
        present = set(arr)
        count = 0
        arr_sorted = sorted(arr)
        max_d = max_val // 2
        for d in range(1, max_d + 1):
            for a in arr_sorted:
                b = a + d
                c = a + 2 * d
                if c > max_val:
                    break
                if b in present and c in present:
                    count += 1
        print(count)
        return
    # Prepare boolean array of presence
    a = np.zeros(size, dtype=np.int8)
    a[arr] = 1
    # FFT convolution of a with itself
    fa = np.fft.fft(a)
    conv = np.rint(np.real(np.fft.ifft(fa * fa))).astype(np.int64)
    total = 0
    for b in arr:
        # conv[2*b] counts ordered pairs (x, y) with x + y = 2b
        # Subtract the (b,b) pair and divide by 2 to get unordered distinct pairs
        total += (conv[2 * b] - 1) // 2
    print(total)

if __name__ == "__main__":
    solve()
