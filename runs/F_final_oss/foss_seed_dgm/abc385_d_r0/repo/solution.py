# Santa Claus 2 solution
import sys, bisect

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    sx = int(next(it))
    sy = int(next(it))

    # Build maps: for each x, list of y's; for each y, list of x's
    x_to_ys = {}
    y_to_xs = {}
    for _ in range(N):
        x = int(next(it))
        y = int(next(it))
        x_to_ys.setdefault(x, []).append(y)
        y_to_xs.setdefault(y, []).append(x)

    # Sort the coordinate lists for binary search
    for lst in x_to_ys.values():
        lst.sort()
    for lst in y_to_xs.values():
        lst.sort()

    visited_cnt = 0
    cx, cy = sx, sy
    for _ in range(M):
        d = next(it).decode()
        c = int(next(it))
        if d == 'U':
            nx, ny = cx, cy + c
            lo, hi = cy, ny
            lst = x_to_ys.get(cx, [])
            l = bisect.bisect_left(lst, lo)
            r = bisect.bisect_right(lst, hi)
            segment = lst[l:r]
            if segment:
                del lst[l:r]
                for y in segment:
                    lst2 = y_to_xs.get(y)
                    if lst2 is not None:
                        idx = bisect.bisect_left(lst2, cx)
                        if idx < len(lst2) and lst2[idx] == cx:
                            del lst2[idx]
                    visited_cnt += 1
        elif d == 'D':
            nx, ny = cx, cy - c
            lo, hi = ny, cy
            lst = x_to_ys.get(cx, [])
            l = bisect.bisect_left(lst, lo)
            r = bisect.bisect_right(lst, hi)
            segment = lst[l:r]
            if segment:
                del lst[l:r]
                for y in segment:
                    lst2 = y_to_xs.get(y)
                    if lst2 is not None:
                        idx = bisect.bisect_left(lst2, cx)
                        if idx < len(lst2) and lst2[idx] == cx:
                            del lst2[idx]
                    visited_cnt += 1
        elif d == 'R':
            nx, ny = cx + c, cy
            lo, hi = cx, nx
            lst = y_to_xs.get(cy, [])
            l = bisect.bisect_left(lst, lo)
            r = bisect.bisect_right(lst, hi)
            segment = lst[l:r]
            if segment:
                del lst[l:r]
                for x in segment:
                    lst2 = x_to_ys.get(x, [])
                    idx = bisect.bisect_left(lst2, cy)
                    if idx < len(lst2) and lst2[idx] == cy:
                        del lst2[idx]
                    visited_cnt += 1
        elif d == 'L':
            nx, ny = cx - c, cy
            lo, hi = nx, cx
            lst = y_to_xs.get(cy, [])
            l = bisect.bisect_left(lst, lo)
            r = bisect.bisect_right(lst, hi)
            segment = lst[l:r]
            if segment:
                del lst[l:r]
                for x in segment:
                    lst2 = x_to_ys.get(x, [])
                    idx = bisect.bisect_left(lst2, cy)
                    if idx < len(lst2) and lst2[idx] == cy:
                        del lst2[idx]
                    visited_cnt += 1
        else:
            raise ValueError('invalid direction')
        cx, cy = nx, ny
    sys.stdout.write(f"{cx} {cy} {visited_cnt}")

if __name__ == "__main__":
    solve()
