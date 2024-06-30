import numpy as np
import random

# create game space
game_space = np.array([[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]])
print("Initial state:\n", game_space)

# choose computer and player characters: 0 for o, 1 for x
computer_character = random.randint(0,1)
print("Computer character:", computer_character, "o" if computer_character == 0 else "x")

player_character = 0 if computer_character == 1 else 1
print("Player character:", player_character, "o" if player_character == 0 else "x")

# computer takes first step
first_computer_step = (random.randint(0,2), random.randint(0,2))
print("First computer step:", first_computer_step)

game_space[first_computer_step] = computer_character
print(game_space)

i = 0

# game loop
while np.isnan(game_space).any():
    try:
        # get player step TODO
        while True:
            player_input = input("Enter choice (eg. 12):\n")

            if 


        print("Iteration:", i)
        nan_elements_idx = np.argwhere(np.isnan(game_space)) 
        print(nan_elements_idx)

        computer_step = random.randint(0, len(nan_elements_idx)-1)
        print(computer_step)
        
        game_space[tuple(nan_elements_idx[computer_step])] = computer_character
        print(game_space)

        i = i+1
    except Exception as e:
        print(e)






