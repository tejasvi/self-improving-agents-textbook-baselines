# Write your solution here. Read from stdin, write to stdout.

import sys, bisect
from collections import defaultdict

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    Sx = int(next(it))
    Sy = int(next(it))

    # maps
    x_to_ys = defaultdict(list)  # x : sorted list of y where house exists
    y_to_xs = defaultdict(list)  # y : sorted list of x where house exists

    # store houses for potential future reference (not needed actually)
    for _ in range(N):
        x = int(next(it))
        y = int(next(it))
        x_to_ys[x].append(y)
        y_to_xs[y].append(x)

    # sort the coordinate lists for binary search
    for x in x_to_ys:
        x_to_ys[x].sort()
    for y in y_to_xs:
        y_to_xs[y].sort()

    cur_x, cur_y = Sx, Sy
    visited = 0

    for _ in range(M):
        D = next(it).decode()
        C = int(next(it))
        if D == 'U' or D == 'D':
            # vertical movement, x stays the same
            nx = cur_x
            ny = cur_y + C if D == 'U' else cur_y - C
            lo = min(cur_y, ny)
            hi = max(cur_y, ny)
            lst = x_to_ys.get(nx)
            if lst:
                l = bisect.bisect_left(lst, lo)
                r = bisect.bisect_right(lst, hi)
                if l < r:
                    to_visit = lst[l:r]
                    # remove visited y's from this list
                    del lst[l:r]
                    for y in to_visit:
                        # count this house
                        visited += 1
                        # also remove x from the corresponding y list
                        lst2 = y_to_xs.get(y)
                        if lst2:
                            pos = bisect.bisect_left(lst2, nx)
                            if pos < len(lst2) and lst2[pos] == nx:
                                lst2.pop(pos)
            cur_x, cur_y = nx, ny
        else:  # 'L' or 'R'
            ny = cur_y
            nx = cur_x - C if D == 'L' else cur_x + C
            lo = min(cur_x, nx)
            hi = max(cur_x, nx)
            lst = y_to_xs.get(ny)
            if lst:
                l = bisect.bisect_left(lst, lo)
                r = bisect.bisect_right(lst, hi)
                if l < r:
                    to_visit = lst[l:r]
                    del lst[l:r]
                    for x in to_visit:
                        visited += 1
                        lst2 = x_to_ys.get(x)
                        if lst2:
                            pos = bisect.bisect_left(lst2, ny)
                            if pos < len(lst2) and lst2[pos] == ny:
                                lst2.pop(pos)
            cur_x, cur_y = nx, ny

    # output final position and visited count
    out = f"{cur_x} {cur_y} {visited}\n"
    sys.stdout.write(out)

if __name__ == "__main__":
    main()
