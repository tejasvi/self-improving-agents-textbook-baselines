import sys

def cell(i, j):
    # 2 * black area of unit cell [i,i+1]x[j,j+1]; i, j nonnegative after shifting
    if (i + j) % 2 == 1:
        return 1  # split by anti-diagonal: exactly half black
    # uniform cell: color from parity of floor(x)+floor(y/2)+floor((x+y)/2) at center
    g = (i + j // 2 + (i + j) // 2) % 2
    return 2 if g == 0 else 0

# period-4 table
P = [[cell(i, j) for j in range(4)] for i in range(4)]
# prefix Q[rx][ry] = sum over i<rx, j<ry
Q = [[0] * 5 for _ in range(5)]
for rx in range(5):
    for ry in range(5):
        if rx == 0 or ry == 0:
            Q[rx][ry] = 0
        else:
            Q[rx][ry] = sum(P[i][j] for i in range(rx) for j in range(ry))
T = Q[4][4]

def G(X, Y):
    # sum of cells in [0,X) x [0,Y), X,Y >= 0
    qx, rx = divmod(X, 4)
    qy, ry = divmod(Y, 4)
    rowfull = Q[4][ry]  # sum over i in full period, j<ry
    colfull = Q[rx][4]  # sum over i<rx, j in full period
    return qx * qy * T + qx * rowfull + qy * colfull + Q[rx][ry]

def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    OFF = 1000000004  # multiple of 4, makes all coordinates nonnegative
    A += OFF; B += OFF; C += OFF; D += OFF
    print(G(C, D) - G(A, D) - G(C, B) + G(A, B))

main()
