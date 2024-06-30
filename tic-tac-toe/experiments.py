import re
import numpy as np

game_space = np.array([[np.nan, 1, np.nan], [np.nan, 1, np.nan], [1, np.nan, np.nan]])
print(game_space)

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

while True:
    player_input = input("Enter coordinates:\n")

    if re.match(pattern=pattern, string=player_input):
        print(player_input, "OK")
        
        player_input_row = int(player_input[0])
        player_input_col = int(player_input[1])

        if np.isnan(game_space[player_input_row][player_input_col]):
            game_space[player_input_row][player_input_col] = 0
            print(game_space)

            # check if game is is_won
            if check_win(game_space, np.float64(1), np.float64(0)) == True:
                break
        else:
            print("Field already filled!")



    else:
        print(player_input, "NOT OK")