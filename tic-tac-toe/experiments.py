import re
import numpy as np

game_space = np.array([[np.nan, 1, np.nan], [np.nan, 1, np.nan], [1, np.nan, np.nan]])
print(game_space)

pattern = r'^[0-2][0-2]$'

def check_win(game_space: np.array):
    

while True:
    user_input = input("Enter coordinates:\n")

    if re.match(pattern=pattern, string=user_input):
        print(user_input, "OK")
        
        user_input_row = int(user_input[0])
        user_input_col = int(user_input[1])

        if np.isnan(game_space[user_input_row][user_input_col]):
            game_space[user_input_row][user_input_col] = 0
            print(game_space)

            # check if game is won
            if 
        else:
            print("Field already filled!")



    else:
        print(user_input, "NOT OK")