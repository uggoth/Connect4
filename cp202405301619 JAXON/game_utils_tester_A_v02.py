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

print (' {:8}'.format('play_x') +
       ' {:7}'.format('play_y') +
       ' {:13}'.format('v_string') +
       ' {:13}'.format('h_string') +
       ' {:13}'.format('r_string') +
       ' {:13}'.format('f_string')
       )

angles = ['V','H','R','F']

def format_result(result):
    sequence = ['PLAY_X','PLAY_Y','START_X','END_X','STEP_X','START_Y','END_Y','STEP_Y']
    s = ''
    for item in sequence:
        s += '  '
        s += item
        s += ': '
        s += str(result[item])
    return s

for column in range(1,no_columns+1):
    play_x = column - 1
    play_y = game_utils.find_free_row(column, game_state) - 1
    output_string = '{:5}'.format(play_x)
    output_string += '{:9}'.format(play_y)
    output_string += '  '
    for angle in angles:
        result = game_utils.get_slice(play_x, play_y, angle, game_state)
        #output_string += format_result(result)
        angle_string = game_utils.array_to_string(result['ARRAY'])
        output_string += '  ' + angle + ': ' + '{:9}'.format(angle_string)
    print(output_string)
