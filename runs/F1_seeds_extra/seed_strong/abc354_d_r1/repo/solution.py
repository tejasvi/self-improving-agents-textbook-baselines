import sys

def count_mod(L, R, r, m):
    # number of x in [L, R) with x % m == r
    return (R - 1 - r) // m - (L - 1 - r) // m

def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    # Unit squares [i,i+1]x[j,j+1], i in [A,C), j in [B,D).
    # Odd (i+j) squares: half black -> contributes 1 to doubled area.
    # Even (i+j) squares: fully black iff floor(i/2) even, i.e. i%4 in {0,1}; contributes 2.
    Ei = count_mod(A, C, 0, 2)
    Oi = (C - A) - Ei
    Ej = count_mod(B, D, 0, 2)
    Oj = (D - B) - Ej
    Se = count_mod(A, C, 0, 4)
    So = count_mod(A, C, 1, 4)
    odd_pairs = Ei * Oj + Oi * Ej
    even_black = Se * Ej + So * Oj
    print(odd_pairs + 2 * even_black)

main()
