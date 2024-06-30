import numpy as np
import random
import re

pattern = r'^[0-2][0-2]$'

def check_win(game_space: np.array, computer_character: np.float64, player_character: np.float64):
    is_won = False

    # rows
    for row in range(0,3):
        if game_space[row][0] == game_space[row][1] == game_space[row][2] == computer_character:
            is_won = True
            print("Computer is_won!")

        elif game_space[row][0] == game_space[row][1] == game_space[row][2] == player_character:
            is_won = True
            print("Player is_won!")

    # columns
    for col in range(0,3):
        if game_space[0][col] == game_space[1][col] == game_space[2][col] == computer_character:
            is_won = True
            print("Computer is_won!")
        
        elif game_space[0][col] == game_space[1][col] == game_space[2][col] == player_character:
            is_won = True
            print("Player is_won!")

    # diagonal
    if (game_space[0][0] == game_space[1][1] == game_space[2][2] == computer_character) or (game_space[0][2] == game_space[1][1] == game_space[2][0] == computer_character):
        is_won = True
        print("Computer is_won!")

    elif (game_space[0][0] == game_space[1][1] == game_space[2][2] == player_character) or (game_space[0][2] == game_space[1][1] == game_space[2][0] == player_character):
        is_won = True
        print("Player is_won!")

    return is_won

# create game space
game_space = np.array([[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]])
print("Initial state:\n", game_space)

computer_character = 1
player_character = 0

# computer takes first step
first_computer_step = (random.randint(0,2), random.randint(0,2))
print("First computer step:", first_computer_step)

game_space[first_computer_step] = computer_character
print(game_space)

i = 0

# game loop
while np.isnan(game_space).any():
    try:
        print("Iteration:", i)

        # get player step TODO
        while True:
            player_input = input("Enter choice (eg. 12):\n")

            if re.match(pattern=pattern, string=player_input):
                print(player_input, "OK")

                player_input_row = int(player_input[0])
                player_input_col = int(player_input[1])

                if np.isnan(game_space[player_input_row][player_input_col]):
                    game_space[player_input_row][player_input_col] = player_character
                    print(game_space)

                    break
                else:
                    print("Field already filled!")

        # check if game is is_won after player step
        if check_win(game_space, np.float64(1), np.float64(0)) == True:
            break   

        nan_elements_idx = np.argwhere(np.isnan(game_space)) 
        print(nan_elements_idx)

        computer_step = random.randint(0, len(nan_elements_idx)-1)
        print(computer_step)
        
        game_space[tuple(nan_elements_idx[computer_step])] = computer_character
        print(game_space)

        # check if game is is_won after computer step
        if check_win(game_space, np.float64(1), np.float64(0)) == True:
            break

        i = i+1
    except Exception as e:
        print(e)






