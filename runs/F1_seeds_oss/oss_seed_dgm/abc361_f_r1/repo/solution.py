# Write your solution here. Read from stdin, write to stdout.
import sys, math

def count_perfect_powers(N: int) -> int:
    # Count numbers x (1 <= x <= N) that can be expressed as a^b with b >= 2.
    # Include 1 (=1^b).
    # Count all perfect squares, then add higher powers while avoiding double counting.
    sqrtN = math.isqrt(N)
    # Compute integer cube root floor
    # Initial approximation using float then adjust
    cube_root = int(N ** (1/3))
    while (cube_root + 1) ** 3 <= N:
        cube_root += 1
    while cube_root ** 3 > N:
        cube_root -= 1
    higher = set()
    for a in range(2, cube_root + 1):
        # start from exponent 3
        val = a * a * a
        while val <= N:
            higher.add(val)
            # avoid overflow when multiplying by a
            if val > N // a:
                break
            val *= a
    # Count how many of the higher powers are also perfect squares
    squares_in_higher = sum(1 for x in higher if math.isqrt(x) ** 2 == x)
    return sqrtN + len(higher) - squares_in_higher

def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)
    print(count_perfect_powers(N))

if __name__ == "__main__":
    main()
