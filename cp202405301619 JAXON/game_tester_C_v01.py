module_name = 'game_tester_C_v01.py'
print (module_name, 'starting')

import game_v09 as game
import game_utils_v05 as game_utils

my_game = game.Connect4Game('My Game')

# each move is a red / yellow pair
moves = [[4,4],[4,3],[2,5],[1,6],[3,5],[3,5]]

red_player = 1
yellow_player = 2

turn = 0

for move in moves:
    turn += 1
    print ('\nAfter Turn', turn)

    red_column = move[red_player-1]
    if game_utils.column_playable(red_column, my_game.game_state):
        my_game.play_in(red_column)
    else:
        print ('Invalid column', red_column)
    if my_game.game_over:
        game_utils.print_game_state(my_game.game_state)
        print ('**** red wins')
        break

    yellow_column = move[yellow_player-1]
    if game_utils.column_playable(red_column, my_game.game_state):
        my_game.play_in(red_column)
    else:
        print ('Invalid column', red_column)
    if my_game.game_over:
        game_utils.print_game_state(my_game.game_state)
        print ('**** yellow wins')
        break

    game_utils.print_game_state(my_game.game_state)

print (module_name, 'finished')
