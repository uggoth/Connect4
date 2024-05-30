import game_utils_v05 as game_utils

available_states = game_utils.make_test_states()

game_utils.print_available_states(available_states)
chosen_state = int(input("Choose State: (0-" + str(len(available_states)-1) + "): "))
game_state = available_states[chosen_state]

no_columns = len(game_state)
no_rows = len(game_state[0])

print ("\nColumns: {:2}, Rows: {:2}".format(no_columns, no_rows))

game_utils.print_game_state(game_state)

my_player = 1
my_opponent = 2

good_column = game_utils.find_4(game_state, my_player)

if good_column == 0:
    print ('No win for 1')
else:
    print ('Win for 1 in column ' + str(good_column))

good_column = game_utils.find_4(game_state, my_opponent)

if good_column == 0:
    print ('No win for 2')
else:
    print ('Win for 2 in column ' + str(good_column))

good_column = game_utils.find_3(game_state, my_player)

if good_column == 0:
    print ('No triple for 1')
else:
    print ('triple for 1 in column ' + str(good_column))

good_column = game_utils.find_3(game_state, my_opponent)

if good_column == 0:
    print ('No triple for 2')
else:
    print ('triple for 2 in column ' + str(good_column))
