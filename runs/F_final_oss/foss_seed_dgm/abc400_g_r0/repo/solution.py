# Solution for AtCoder ABC 400 Patisserie ABC 3
# The optimal total price equals the maximum among the sums of the largest 2K values
# of each attribute (beauty, tastiness, popularity). This follows because for any
# pairing the total price is at least the sum of the chosen attribute values,
# and we can achieve that bound by selecting the 2K cakes with the largest
# values of the best attribute.

import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    T = int(next(it))
    out = []
    for _ in range(T):
        N = int(next(it)); K = int(next(it))
        xs = []
        ys = []
        zs = []
        for _ in range(N):
            xs.append(int(next(it)))
            ys.append(int(next(it)))
            zs.append(int(next(it)))
        need = 2 * K
        xs.sort(reverse=True)
        ys.sort(reverse=True)
        zs.sort(reverse=True)
        sum_x = sum(xs[:need])
        sum_y = sum(ys[:need])
        sum_z = sum(zs[:need])
        out.append(str(max(sum_x, sum_y, sum_z)))
    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()
