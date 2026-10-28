# Write your solution here. Read from stdin, write to stdout.
import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    arr = list(map(int, it))
    if n == 0:
        print(0)
        return
    max_val = max(arr)
    size = 1
    while size <= 2 * max_val:
        size <<= 1
    try:
        import numpy as np
    except ImportError:
        # Fallback: simple O(max_val^2) not feasible, but environment should have numpy.
        print('0')
        return
    a = np.zeros(size, dtype=np.int64)
    a[arr] = 1
    # FFT convolution
    fa = np.fft.rfft(a)
    conv = np.fft.irfft(fa * fa, n=size)
    conv = np.rint(conv).astype(np.int64)
    presence = np.zeros(max_val + 1, dtype=bool)
    presence[arr] = True
    ans = 0
    for b in arr:
        total = conv[2 * b]
        if presence[b]:
            total -= 1  # remove (b,b) pair
        ans += total // 2
    print(ans)

if __name__ == "__main__":
    main()
