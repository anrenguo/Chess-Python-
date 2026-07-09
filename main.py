# Chess Game
# Player vs Player chess game with all rules implemented
# Programmed by Anren Guo
# Last updated on 2026-07-09

# Import the loop function from the game module and the time variables from constants
from game import loop
from constants import CLASSICAL_TIME, RAPID_TIME, BLITZ_TIME, BULLET_TIME
# Classical:    90 minutes
# Rapid:        30 minutes
# Blitz:        5 minutes
# Bullet:       1 minute

# Function that starts the game loop
def main():
    loop(CLASSICAL_TIME)

# Running that function if the script was run directly as opposed to being imported as a module
if __name__ == '__main__':
    main()
