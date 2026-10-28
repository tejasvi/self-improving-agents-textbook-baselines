import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    best = 0
    for p in (0, 1):
        # blocks at positions p, p+2, ...; block valid iff a[j] == a[j+1]
        vals = []
        j = p
        while j + 1 < n:
            vals.append(a[j] if a[j] == a[j + 1] else None)
            j += 2
        seen = set()
        left = 0
        for k, v in enumerate(vals):
            if v is None:
                seen.clear()
                left = k + 1
                continue
            while v in seen:
                seen.remove(vals[left])
                left += 1
            seen.add(v)
            if k - left + 1 > best:
                best = k - left + 1
    print(2 * best)


main()
