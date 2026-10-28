import sys
import math

def main():
    # Read N
    N = int(input())
    
    # Calculate minimum number of friends needed
    M = math.ceil(math.log2(N)) if N > 1 else 1
    
    # Print number of friends
    print(M)
    sys.stdout.flush()
    
    # For each friend, determine which bottles to give them
    # We use binary representation: bottle i is given to friend j if bit j is set in i
    for friend in range(M):
        bottles = []
        for bottle in range(1, N + 1):
            # Check if bit 'friend' is set in bottle's binary representation
            if (bottle >> friend) & 1:
                bottles.append(bottle)
        
        # Print the distribution for this friend
        print(len(bottles), *bottles)
        sys.stdout.flush()
    
    # Read the result
    result = input().strip()
    
    # Reconstruct the bottle number from the binary representation
    spoiled_bottle = 0
    for friend in range(M):
        if result[friend] == '1':
            spoiled_bottle |= (1 << friend)
    
    # Print the answer
    print(spoiled_bottle)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
