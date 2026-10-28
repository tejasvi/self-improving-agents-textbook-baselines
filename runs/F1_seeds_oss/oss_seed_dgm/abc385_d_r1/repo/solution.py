# Santa Claus 2 solution using interval merging
import sys, bisect

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    sx = int(next(it))
    sy = int(next(it))
    houses = [(int(next(it)), int(next(it))) for _ in range(N)]
    # Dictionaries to store intervals traversed for each fixed coordinate
    vert = {}   # x -> list of (y1, y2) intervals (inclusive)
    horiz = {}  # y -> list of (x1, x2) intervals (inclusive)
    curx, cury = sx, sy
    for _ in range(M):
        d = next(it).decode()
        c = int(next(it))
        if d == 'U':
            nx, ny = curx, cury + c
            low, high = (cury, ny) if cury <= ny else (ny, cury)
            vert.setdefault(curx, []).append((low, high))
        elif d == 'D':
            nx, ny = curx, cury - c
            low, high = (cury, ny) if cury <= ny else (ny, cury)
            vert.setdefault(curx, []).append((low, high))
        elif d == 'L':
            nx, ny = curx - c, cury
            low, high = (curx, nx) if curx <= nx else (nx, curx)
            horiz.setdefault(cury, []).append((low, high))
        else:  # 'R'
            nx, ny = curx + c, cury
            low, high = (curx, nx) if curx <= nx else (nx, curx)
            horiz.setdefault(cury, []).append((low, high))
        curx, cury = nx, ny
    # Merge intervals for each key
    def merge_intervals(d):
        for key, lst in d.items():
            lst.sort()
            merged = []
            cur_start, cur_end = lst[0]
            for s, e in lst[1:]:
                if s <= cur_end + 1:  # overlapping or adjacent (inclusive)
                    if e > cur_end:
                        cur_end = e
                else:
                    merged.append((cur_start, cur_end))
                    cur_start, cur_end = s, e
            merged.append((cur_start, cur_end))
            d[key] = merged
    merge_intervals(vert)
    merge_intervals(horiz)
    # For binary search, we will separate starts and ends for each list
    vert_bounds = {}
    for x, lst in vert.items():
        starts = [s for s, _ in lst]
        ends = [e for _, e in lst]
        vert_bounds[x] = (starts, ends)
    horiz_bounds = {}
    for y, lst in horiz.items():
        starts = [s for s, _ in lst]
        ends = [e for _, e in lst]
        horiz_bounds[y] = (starts, ends)
    # Count visited houses
    count = 0
    for hx, hy in houses:
        visited = False
        # check vertical intervals at x = hx
        vb = vert_bounds.get(hx)
        if vb is not None:
            starts, ends = vb
            idx = bisect.bisect_right(starts, hy) - 1
            if idx >= 0 and ends[idx] >= hy:
                visited = True
        if not visited:
            hb = horiz_bounds.get(hy)
            if hb is not None:
                starts, ends = hb
                idx = bisect.bisect_right(starts, hx) - 1
                if idx >= 0 and ends[idx] >= hx:
                    visited = True
        if visited:
            count += 1
    # Final position is curx, cury after loop
    sys.stdout.write(f"{curx} {cury} {count}\n")

if __name__ == "__main__":
    solve()
