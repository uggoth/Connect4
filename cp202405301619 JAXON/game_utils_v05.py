import database_utils_v04 as dbu
mysql = dbu.mariadb
import parameters_v35 as parms
import pickle
import copy

def make_test_states():

    available_states = []

    empty_columns = 7
    empty_rows = 6
    empty = []
    for x in range(empty_columns):
        empty.append([])
        for y in range(empty_rows):
            empty[x].append(0)

    player = 1
    opponent = 2

    test_0 = copy.deepcopy(empty)
    test_0[1][0] = opponent
    test_0[1][1] = player
    test_0[2][0] = opponent
    test_0[2][1] = player
    test_0[3][0] = opponent
    available_states.append(test_0)

    test_1 = copy.deepcopy(empty)
    test_1[3][0] = player
    test_1[3][1] = opponent
    test_1[4][0] = player
    available_states.append(test_1)

    test_2 = copy.deepcopy(empty)
    test_2[3][0] = player
    test_2[4][0] = opponent
    test_2[3][1] = player
    test_2[4][1] = opponent
    test_2[3][2] = player
    test_2[4][2] = opponent
    available_states.append(test_2)

    test_3 = copy.deepcopy(empty)
    test_3[4][0] = player
    test_3[4][1] = opponent
    test_3[5][0] = player
    test_3[5][1] = opponent
    test_3[3][0] = player
    test_3[4][1] = opponent
    available_states.append(test_3)

    test_4 = copy.deepcopy(empty) # has potential winning move in column 6
    test_4[3][0] = player
    test_4[4][0] = opponent
    test_4[4][1] = player
    test_4[5][0] = opponent
    test_4[6][0] = player
    test_4[5][1] = opponent
    test_4[5][2] = player
    test_4[6][1] = opponent
    test_4[6][2] = player
    test_4[2][0] = opponent
    available_states.append(test_4)

    test_5 = copy.deepcopy(empty) # has potential winning move in column 6
    test_5[2][3] = player
    test_5[3][0] = player
    test_5[4][0] = player
    test_5[5][0] = player
    test_5[4][1] = player
    test_5[1][0] = opponent
    test_5[2][0] = opponent
    test_5[2][1] = opponent
    test_5[2][2] = opponent
    test_5[2][4] = opponent
    available_states.append(test_5)

    return available_states

def print_available_states(available_states):
    print ("Available Game States:")
    index = 0
    for game_state in available_states:
        print ("Game State " + str(index))
        print_game_state(game_state)
        print (" ")
        index += 1

def get_score(wins_as_2, wins_as_1, draws, losses):
    win_as_2_value = 3  # wins when playing second gets a bonus
    win_as_1_value = 2  # win when playing first
    draw_value = 1      # any draw
    loss_value = 0      # any loss
    score = ((wins_as_2 * win_as_2_value) +
             (wins_as_1 * win_as_1_value) +
             (draws * draw_value) +
             (losses * loss_value))
    return score

def print_state_string(state_string):
    col_start = parms.game_rows - 1
    for i in range(col_start, -1, -1):
        row_start = i * parms.game_columns
        row_string = ""
        for j in range(parms.game_columns):
            row_item = state_string[row_start + j:row_start + j + 1]
            filler = " "
            row_string += row_item + filler
        print (str(i+1) + ":  " + row_string)

def state_string_to_array(state_string):
    result = []
    for x in range(parms.game_columns):
        col = []
        for y in range(parms.game_rows):
            offset = x + (y * (parms.game_columns))
            col.append(int(state_string[offset:offset+1]))
        result.append(col)
    return result

def print_game_state(game_state):
    no_cols = len(game_state)
    no_rows = len(game_state[0])
    for y in range(no_rows - 1, -1, -1):
        s = ''
        for x in range(no_cols):
            s = s + ' ' + str(game_state[x][y])
        print (str(y+1) + ": " + s)

def load_instance_from_database(player_id):
    conn = dbu.get_conn()
    my_cursor = conn.cursor()
    instance = None
    if ('RBOT' == player_id[0:4]):    # it's a robot
        sql = ("SELECT robot_instance FROM robots WHERE robot_id = '" + player_id + "'")
        my_cursor.execute(sql)
        data_row = my_cursor.fetchone()
        instance = data_row[0]
    elif ('CNET' == player_id[0:4]):
        sql = ("SELECT instance FROM nets WHERE net_id = '" + player_id + "'")
        my_cursor.execute(sql)
        data_row = my_cursor.fetchone()
        instance = data_row[0]
    elif (('RNET' == player_id[0:4]) or ('VNET' == player_id[0:4]) or ('ENET' == player_id[0:4])):
        sql = ("SELECT instance FROM nets WHERE net_id = '" + player_id + "'")
        my_cursor.execute(sql)
        data_row = my_cursor.fetchone()
        instance = data_row[0]
    if instance:
        return pickle.loads(instance)
    else:
        return False

def get_test_state(test_state_id):
    result = {}
    result['SUCCESS'] =  False
    conn = dbu.get_conn()
    my_cursor = conn.cursor(dictionary=True)
    sql = ("SELECT state_string, state_desc " +
           "FROM test_states " +
           "WHERE test_state_id='" + test_state_id + "'")
    my_cursor.execute(sql)
    row = my_cursor.fetchone()
    result['STATE_STRING'] = row['state_string']
    result['STATE_DESC'] = row['state_desc']
    result['SUCCESS'] = True
    return result

def print_test_states():
    print ("Available Test Game States:")
    conn = dbu.get_dict_conn()
    my_cursor = conn.cursor()
    sql = ("SELECT test_state_id, state_desc, state_string FROM test_states ORDER BY test_state_id")
    result = my_cursor.execute(sql)
    if not result:
        print ("No states found")
        return
    rows = my_cursor.fetchall()
    for row in rows:
        print ("Game State " + row['test_state_id'] + ' ' + row['state_desc'])
        print_state_string(row['state_string'])
        print (" ")

def is_in(x,y,min_x,min_y,max_x,max_y):
    if ((x < min_x) or (x > max_x)):
        return False
    if ((y < min_y) or (y > max_y)):
        return False
    return True

def constrain(x,min_x,max_x):
    if x > max_x:
        return max_x
    if x < min_x:
        return min_x
    return x

def bigger_of(x1,x2):
    if x1 > x2:
        return x1
    else:
        return x2

def smaller_of(x1,x2):
    if x1 < x2:
        return x1
    else:
        return x2

def find_edge(x,y,min_x,min_y,max_x,max_y,direction):
    result = {}
    result['SUCCESS'] = False
    valid_directions = ['N','S','E','W','NE','SE','SW','NW']
    if direction not in valid_directions:
        return result
    if not is_in(x,y,min_x,min_y,max_x,max_y):
        return result
    if direction == 'N':
        rx = x
        ry = max_y
    elif direction == 'S':
        rx = x
        ry = min_y
    elif direction == 'E':
        rx = max_x
        ry = y
    elif direction == 'W':
        rx = min_x
        ry = y
    elif direction == 'NE':
        dx = max_x - x
        dy = max_y - y
        sd = smaller_of(dx,dy)
        rx = x + sd
        ry = y + sd
    elif direction == 'SE':
        dx = max_x - x
        dy = y - min_y
        sd = smaller_of(dx,dy)
        rx = x + sd
        ry = y - sd
    elif direction == 'SW':
        dx = x - min_x
        dy = y - min_y
        sd = smaller_of(dx,dy)
        rx = x - sd
        ry = y - sd
    elif direction == 'NW':
        dx = x - min_x
        dy = max_y - y
        sd = smaller_of(dx,dy)
        rx = x - sd
        ry = y + sd
    result['RX'] = rx
    result['RY'] = ry
    return result

def find_preferred (game_state): # returns preferred column to play in
    preferred = [[4,1],
                 [4,2],[3,1],[5,1],
                 [4,3],[3,2],[5,2],[2,1],[6,1],
                 [4,4],[3,3],[5,3],[2,2],[6,2],[1,1],[7,1],
                 [4,5],[3,4],[5,4],[2,3],[6,3],[1,2],[7,2],
                 [4,6],[3,5],[5,5],[2,4],[6,4],[1,3],[7,3],
                 [4,7],[3,6],[5,6],[2,5],[5,5],[1,4],[7,4],
                 [3,7],[5,7],[2,6],[6,6],[1,5],[7,5],
                 [2,7],[6,7],[1,6],[7,6],
                 [1,7],[7,7]]
    for slot in preferred:
        column = slot[0]
        row = slot[1]
        available_row = find_free_row(column, game_state)
        if row == available_row:
            return column
    return 0

def new_find_preferred (game_state, avoid_columns=False): # returns preferred column to play in
    preferred = [[4,1],
                 [4,2],[3,1],[5,1],
                 [4,3],[3,2],[5,2],[2,1],[6,1],
                 [4,4],[3,3],[5,3],[2,2],[6,2],[1,1],[7,1],
                 [4,5],[3,4],[5,4],[2,3],[6,3],[1,2],[7,2],
                 [4,6],[3,5],[5,5],[2,4],[6,4],[1,3],[7,3],
                 [4,7],[3,6],[5,6],[2,5],[5,5],[1,4],[7,4],
                 [3,7],[5,7],[2,6],[6,6],[1,5],[7,5],
                 [2,7],[6,7],[1,6],[7,6],
                 [1,7],[7,7]]
    for slot in preferred:
        column = slot[0]
        if avoid_columns and column in avoid_columns:
            continue
        row = slot[1]
        available_row = find_free_row(column, game_state)
        if row == available_row:
            return column
    return 0

def find_free_row(column, game_state):
    no_columns = len(game_state)
    no_rows = len(game_state[0])
    x = column - 1
    for y in range(no_rows):
        if game_state[x][y] == 0:
            return y+1
    return 0

def check_move_possible( column, game_state):
    x = column - 1
    if x<0 or x>(len(game_state)-1):
        return False
    y = len(game_state[0]) - 1
    if game_state[x][y] == 0:
        return True
    return False

def format_result(result):
    sequence = ['PLAY_X','PLAY_Y','START_X','START_Y','END_X','END_Y','STEP_X','STEP_Y','X_RANGE','Y_RANGE','LOOP_RANGE']
    s = ''
    for item in sequence:
        s += '  '
        s += item
        s += ': '
        s += str(result[item])
    return s

def make_result(start_x, end_x, start_y, end_y, play_x, play_y, game_state):
    result = {}
    result['SUCCESS'] = False
    return_array = []
    no_columns = len(game_state)
    no_rows = len(game_state[0])

    if end_x == start_x:
        step_x = 0
    elif end_x < start_x:
        step_x = -1
    else:
        step_x = 1

    if end_y == start_y:
        step_y = 0
    elif end_y < start_y:
        step_y = -1
    else:
        step_y = 1

    for x in range(no_columns):
        column = x + 1
        row = find_free_row(column, game_state)
        if row:
            y = row - 1
            game_state[x][y] = 4

    x = start_x
    y = start_y

    x_range = abs(end_x - start_x)
    y_range = abs(end_y - start_y)
    loop_range = bigger_of(x_range, y_range)

    result['START_X'] = start_x
    result['END_X'] = end_x
    result['STEP_X'] = step_x
    result['START_Y'] = start_y
    result['END_Y'] = end_y
    result['STEP_Y'] = step_y
    result['PLAY_X'] = play_x
    result['PLAY_Y'] = play_y
    result['X_RANGE'] = x_range
    result['Y_RANGE'] = y_range
    result['LOOP_RANGE'] = loop_range

    #print format_result(result)

    for i in range(loop_range+1):
        if ((x == play_x) and (y == play_y)):
            z = 3
        else:
            z = game_state[x][y]
        return_array.append(z)
        x += step_x
        y += step_y

    result['ARRAY'] = return_array
    result['SUCCESS'] = True
    return result

def make_slice_string(start_x, end_x, start_y, end_y, game_state):

    if end_x == start_x:
        step_x = 0
    elif end_x < start_x:
        step_x = -1
    else:
        step_x = 1

    if end_y == start_y:
        step_y = 0
    elif end_y < start_y:
        step_y = -1
    else:
        step_y = 1

    x_range = abs(end_x - start_x)
    y_range = abs(end_y - start_y)
    loop_range = bigger_of(x_range, y_range)

    return_string = ''
    x = start_x
    y = start_y

    for i in range(loop_range+1):
        return_string += str(game_state[x][y])
        x += step_x
        y += step_y
        
    return return_string

def get_slice_string(play_x, play_y, angle, game_state):

    no_columns = len(game_state)
    no_rows = len(game_state[0])

    min_x = 0
    max_x = no_columns - 1
    min_y = 0
    max_y = no_rows - 1

    if angle == 'V':
        start_x = play_x
        start_y = 0
        end_x = play_x
        end_y = max_y
        return make_slice_string(start_x, end_x, start_y, end_y, game_state)    
    elif angle == 'H':
        start_x = 0
        start_y = play_y
        end_x = max_x
        end_y = play_y
        return make_slice_string(start_x, end_x, start_y, end_y, game_state)
    elif angle == 'R':
        sub_result = find_edge(play_x,play_y,min_x,min_y,max_x,max_y,'SW')
        start_x = sub_result['RX']
        start_y = sub_result['RY']
        sub_result = find_edge(play_x,play_y,min_x,min_y,max_x,max_y,'NE')
        end_x = sub_result['RX']
        end_y = sub_result['RY']
        return make_slice_string(start_x, end_x, start_y, end_y, game_state)          
    elif angle == 'F':
        sub_result = find_edge(play_x,play_y,min_x,min_y,max_x,max_y,'NW')
        start_x = sub_result['RX']
        start_y = sub_result['RY']
        sub_result = find_edge(play_x,play_y,min_x,min_y,max_x,max_y,'SE')
        end_x = sub_result['RX']
        end_y = sub_result['RY']
        return make_slice_string(start_x, end_x, start_y, end_y, game_state)
    else:
        return False
    

def get_slice( play_x, play_y, angle, game_state_in):
    # what happens if I go in cell[x][y] (currently empty)
    # returns an array of values for cells at angle (or False on error)
    # angle can be bottom to top 'V' left to right 'H'
    # rising from left to right 'R' or falling left to right 'F'
    # the array cells contain:
    # 0 - empty
    # 1 - player 1
    # 2 - player 2
    # 3 - the cell for the column
    # 4 - empty now, but next row to fill
    
    angles = ['V','H','R','F']
    if not angle in angles:
        print ("Bad Angle " + angle)
        return False

    game_state = copy.deepcopy(game_state_in)

    no_columns = len(game_state)
    no_rows = len(game_state[0])

    min_x = 0
    max_x = no_columns - 1
    min_y = 0
    max_y = no_rows - 1

    if play_x < 0 or play_x > max_x:
        print ("Bad X " + str(play_x))
        return False

    if play_y < 0 or play_y > max_y:
        print ("Bad Y " + str(play_y))
        return False

    if game_state[play_x][play_y] != 0:
        print ("Cell not empty")
        return False

    result = {}
    result['SUCCESS'] = False

    #print_game_state(game_state)

    if angle == 'V':
        start_x = play_x
        start_y = 0
        end_x = play_x
        end_y = max_y
        return make_result(start_x, end_x, start_y, end_y, play_x, play_y, game_state)
    
    if angle == 'H':
        start_x = 0
        start_y = play_y
        end_x = max_x
        end_y = play_y
        return make_result(start_x, end_x, start_y, end_y, play_x, play_y, game_state)
    
    if angle == 'R':
        sub_result = find_edge(play_x,play_y,min_x,min_y,max_x,max_y,'SW')
        start_x = sub_result['RX']
        start_y = sub_result['RY']
        sub_result = find_edge(play_x,play_y,min_x,min_y,max_x,max_y,'NE')
        end_x = sub_result['RX']
        end_y = sub_result['RY']
        return make_result(start_x, end_x, start_y, end_y, play_x, play_y, game_state)
                    
    if angle == 'F':
        sub_result = find_edge(play_x,play_y,min_x,min_y,max_x,max_y,'NW')
        start_x = sub_result['RX']
        start_y = sub_result['RY']
        sub_result = find_edge(play_x,play_y,min_x,min_y,max_x,max_y,'SE')
        end_x = sub_result['RX']
        end_y = sub_result['RY']
        return make_result(start_x, end_x, start_y, end_y, play_x, play_y, game_state)

    print ("Bottomed Out")
    result['SUCCESS'] = False
    return result        

def array_to_string(in_array):
    result = ''
    for i in range(len(in_array)):
        result += str(in_array[i])
    return result

def analyse_slice(slice_array, player):
    #print ("Slice Array " + str(slice_array))
    slice_string = array_to_string(slice_array)
    #print (slice_string)
    return slice_string;

def column_playable(column, game_state):
    no_rows = len(game_state[0])
    if game_state[column-1][no_rows-1] == 0:
        return True
    else:
        return False

def player_valid(player):
    if ((player == 1) or (player == 2)):
        return True
    else:
        return False

def column_valid(column, game_state):
    no_columns = len(game_state)
    if column < 1 or column > no_columns:
        return False
    else:
        return True 

def new_make_angle_array(game_state):
    angle_array = {}
    angles = ['H','V','R','F']
    no_columns = len(game_state)
    for play_x in range(0, no_columns):
        angle_array[play_x] = {}
        row = find_free_row(play_x + 1, game_state)
        #print ("Column: " + str(play_x) + ", Free Row: " + str(row))
        if row == 0:
            continue
        play_y = row - 1
        for angle in angles:
            slice_string = get_slice_string(play_x, play_y, angle, game_state)
            if not slice_string:
                print ('Slice Failed')
                return False
            angle_array[play_x][angle] = slice_string
    return angle_array
    

def make_angle_array(game_state):
    angle_array = {}
    angles = ['H','V','R','F']
    no_columns = len(game_state)
    for play_x in range(0, no_columns):
        angle_array[play_x] = {}
        row = find_free_row(play_x + 1, game_state)
        #print ("Column: " + str(play_x) + ", Free Row: " + str(row))
        if row == 0:
            continue
        play_y = row - 1
        for angle in angles:
            sub_result = get_slice (play_x, play_y, angle, game_state)
            if not sub_result['SUCCESS']:
                print ('Slice Failed')
                return 0
            slice_string = array_to_string(sub_result['ARRAY'])
            angle_array[play_x][angle] = slice_string
    return angle_array

def print_angle_array(angle_array):
    for x in angle_array:
        for a in angle_array[x]:
            print (str(x) + ' ' + a + ' ' + angle_array[x][a])

def find_pattern (game_state, player, patterns): # returns column to play in if matches pattern
    #print (game_state)
    if not player_valid(player):
        return 0

    angles = ['H','V','R','F']

    no_columns = len(game_state)

    for play_x in range(0, no_columns):
        row = find_free_row(play_x + 1, game_state)
        #print ("Column: " + str(play_x) + ", Free Row: " + str(row))
        if row == 0:
            continue
        play_y = row - 1
        for angle in angles:
            sub_result = get_slice (play_x, play_y, angle, game_state)
            if not sub_result['SUCCESS']:
                print ('Slice Failed')
                return 0
            slice_string = array_to_string(sub_result['ARRAY'])
            #print (str(play_x) + ' ' + angle + ' ' + slice_string)
            for search_string in patterns:
                if slice_string.find (search_string) > -1:
                    return play_x + 1
    return 0

def find_4 (game_state, player): # returns column to play in to win, or 0

    if not player_valid(player):
        return 0

    angles = ['H','V','R','F']

    base_strings = []
    base_strings.append('PPP3')
    base_strings.append('PP3P')
    base_strings.append('P3PP')
    base_strings.append('3PPP')

    ps = str(player)

    search_strings = []
    for base_string in base_strings:
        search_strings.append(base_string.replace('P',ps))
    #print(search_strings)

    return find_pattern (game_state, player, search_strings)

def find_3 (game_state, player): # returns column to play in for open-ended triple, or 0

    if not player_valid(player):
        return 0

    angles = ['H','V','R','F']

    base_strings = []
    base_strings.append('4PP34')
    base_strings.append('4P3P4')
    base_strings.append('43PP4')

    ps = str(player)

    search_strings = []
    for base_string in base_strings:
        search_strings.append(base_string.replace('P',ps))

    return find_pattern (game_state, player, search_strings)

def find_strings (angle_array, player, base_strings): # returns best column, or 0
    search_strings = []
    for base_string in base_strings:
        search_strings.append(base_string.replace('P',str(player)))
    for x in angle_array:
        for a in angle_array[x]:
            slice_string = angle_array[x][a]
            for search_string in search_strings:
                if slice_string.find(search_string) > -1:
                    return x+1
    return 0

def new_find_4 (angle_array, player): # returns column to play in to win, or 0
    base_strings = []
    base_strings.append('PPP3')
    base_strings.append('PP3P')
    base_strings.append('P3PP')
    base_strings.append('3PPP')
    return find_strings (angle_array, player, base_strings)

def new_find_3a (angle_array, player): # returns column to play in to win, or 0
    base_strings = []
    base_strings.append('4PP34')
    base_strings.append('4P3P4')
    base_strings.append('43PP4')
    return find_strings (angle_array, player, base_strings)

def new_find_3b (angle_array, player): # returns column to play in to win, or 0
    base_strings = []
    base_strings.append('4PP30')
    base_strings.append('4P3P0')
    base_strings.append('43PP0')
    base_strings.append('0PP34')
    base_strings.append('0P3P4')
    base_strings.append('03PP4')
    return find_strings (angle_array, player, base_strings)

def new_find_3c (angle_array, player): # returns column to play in to win, or 0
    base_strings = []
    base_strings.append('0PP30')
    base_strings.append('0P3P0')
    base_strings.append('03PP0')
    return find_strings (angle_array, player, base_strings)

def new_find_3d (angle_array, player): # returns column to play in to win, or 0
    base_strings = []
    base_strings.append('PP30')
    base_strings.append('P3P0')
    base_strings.append('3PP0')
    base_strings.append('0PP3')
    base_strings.append('0P3P')
    base_strings.append('03PP')
    return find_strings (angle_array, player, base_strings)

def new_find_2 (angle_array, player): # returns column to play in to win, or 0
    base_strings = []
    base_strings.append('44P34')
    base_strings.append('443P4')
    base_strings.append('4P344')
    base_strings.append('43P44')
    return find_strings (angle_array, player, base_strings)

def build_tree(game_state, depth, next_player):
    max_depth = 2
    if ((depth < 0) or (depth > max_depth)):
        return False
    if (next_player not in [1,2]):
        return False
    no_columns = len(game_state)
    no_rows = len(game_state[0])
    if ((no_columns != 7) or (no_rows != 6)):
        return False

    tree = []

    tree.append({})
    tree[0]['M0C0'] = {}
    tree[0]['M0C0']['COLUMN'] = 0
    tree[0]['M0C0']['STATE'] = game_state
    tree[0]['M0C0']['SLICE_STRING'] = concatenate_all_slices(game_state)
    if depth < 1:
        return tree

    current_player = next_player

    for level in range(1, depth+1):
        tree.append({})
        for current_root in tree[level-1]:
            game_state = tree[level-1][current_root]['STATE']
            for x in range(no_columns):
                column = x + 1
                row = find_free_row(column, game_state)
                if row < 1:     # don't include impossible moves
                    continue
                new_game_state = copy.deepcopy(game_state)
                new_game_state[x][row-1] = current_player
                tree_index = current_root + 'M' + str(level) + 'C' + str(column)
                tree[level][tree_index] = {}
                tree[level][tree_index]['LEVEL'] = level
                tree[level][tree_index]['COLUMN'] = column
                tree[level][tree_index]['STATE'] = new_game_state
                tree[level][tree_index]['SLICE_STRING'] = concatenate_all_slices(new_game_state)
        current_player = 3 - current_player

    return tree

def find_pattern_in_tree(tree, pattern):
    result = False
    for level in range(len(tree)):
        for index in tree[level]:
            slice_string = tree[level][index]['SLICE_STRING']
            if pattern in slice_string:
                if not result:
                    result = {}
                result[index] = tree[level][index]
    return result

def find_pair_of_patterns_in_tree(tree, pattern, player, stop_on_first=False):
    #print ("Search Pattern: " + search_pattern)
    player_search_pattern = pattern.replace('P',str(player))
    result = {}
    result['SUCCESS'] = False
    found_for_player = False
    opponent_search_pattern = pattern.replace('P',str(3-player))
    found_for_opponent = False
    for level in range(len(tree)):
        for index in tree[level]:
            slice_string = tree[level][index]['SLICE_STRING']
            #print (index + ' ' + slice_string)

            if player_search_pattern in slice_string:
                if not found_for_player:
                    found_for_player = []
                found_for_player.append(tree[level][index]['COLUMN'])
                if stop_on_first:
                    break

            if opponent_search_pattern in slice_string:
                if not found_for_opponent:
                    found_for_opponent = []
                found_for_opponent.append(tree[level][index]['COLUMN'])
                if stop_on_first:
                    break
    result['FOUND_FOR_PLAYER'] = found_for_player
    result['FOUND_FOR_OPPONENT'] = found_for_opponent
    result['SUCCESS'] = True
    return result

def make_one_slice(game_state, starts, ends, x_inc, y_inc, terminator):
    this_slice = ''
    for i in range(len(starts)):
        start_x = starts[i][0]
        start_y = starts[i][1]
        end_x = ends[i][0]
        end_y = ends[i][1]
        x_range = abs(end_x - start_x)
        y_range = abs(end_y - start_y)
        loop_range = bigger_of(x_range, y_range)
        x = start_x
        y = start_y
        for i in range(loop_range+1):
            this_slice += str(game_state[x][y])
            x += x_inc
            y += y_inc
        this_slice += terminator
    return this_slice

def concatenate_all_slices(game_state):
    terminator = '*'
    all_slices = ''

    # horizontal
    starts = [[0,5],[0,4],[0,3],[0,2],[0,1],[0,0]]
    ends =   [[6,5],[6,4],[6,3],[6,2],[6,1],[6,0]]
    x_inc = 1
    y_inc = 0
    all_slices += make_one_slice(game_state, starts, ends, x_inc, y_inc, terminator)

    # vertical
    starts = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0]]
    ends =   [[0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5]]
    x_inc = 0
    y_inc = 1
    all_slices += make_one_slice(game_state, starts, ends, x_inc, y_inc, terminator)

    # rising diagonal
    starts = [[0,5],[0,4],[0,3],[0,2],[0,1],[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0]]
    ends =   [[0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[6,4],[6,3],[6,2],[6,1],[6,0]]
    x_inc = 1
    y_inc = 1
    all_slices += make_one_slice(game_state, starts, ends, x_inc, y_inc, terminator)
            
    # falling diagonal
    starts = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5]]
    ends =   [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[6,1],[6,2],[6,3],[6,4],[6,5]]
    x_inc = 1
    y_inc = -1
    all_slices += make_one_slice(game_state, starts, ends, x_inc, y_inc, terminator)

    return all_slices

def extract_columns(slice_string):
    start = 0
    first_c = slice_string[start:].find('C')
    if first_c == -1:
        return False
    columns = []
    max_depth = 5
    for i in range(max_depth):
        start += first_c + 1
        chunk = slice_string[start:start+1]
        #print (chunk)
        columns.append(int(chunk))
        first_c = slice_string[start:].find('C')
        if first_c == -1:
            break
    return columns

def print_index(tree, index):
    li = len(index)
    level = (li/4) - 1
    if index in tree[level]:
        print_game_state(tree[level][index]['STATE'])
        print (tree[level][index])
    else:
        print ("Not Found")

def threat_of_4(game_state, player):
    depth = 2
    tree = build_tree(game_state, depth, player)
    pattern = 'PPPP'.replace('P',str(3-player))
    sub_result = find_pattern_in_tree(tree, pattern)
    if sub_result:
        avoids = []
        for item in sub_result:
            column = int(item[7:8])
            avoids.append(column)
        return avoids
    return False

def opportunity_of_4(game_state, player):
    depth = 1
    tree = build_tree(game_state, depth, player)
    pattern = 'PPPP'.replace('P',str(player))
    stop_on_first = True
    sub_result = find_pattern_in_tree(tree, pattern)
    if sub_result:
        for item in sub_result:
            column = sub_result[item]['COLUMN']
            #print ("\n" + item + " " + str(column))
            return column   # Only need first one
    return False

def opportunity_of_3(game_state, player):
    depth = 1
    tree = build_tree(game_state, depth, player)
    stop_on_first = True
    pattern = '0PPP0'.replace('P',str(player))
    sub_result = find_pattern_in_tree(tree, pattern)
    if sub_result:
        for item in sub_result:
            column = sub_result[item]['COLUMN']
            return column   # Only need first one
    pattern = '0PPP'.replace('P',str(player))
    sub_result = find_pattern_in_tree(tree, pattern)
    if sub_result:
        for item in sub_result:
            column = sub_result[item]['COLUMN']
            return column   # Only need first one
    pattern = 'PPP0'.replace('P',str(player))
    sub_result = find_pattern_in_tree(tree, pattern)
    if sub_result:
        for item in sub_result:
            column = sub_result[item]['COLUMN']
            return column   # Only need first one
    return False

def opportunity_of_2(game_state, player):
    depth = 1
    tree = build_tree(game_state, depth, player)
    stop_on_first = True
    pattern = '0PP0'.replace('P',str(player))
    sub_result = find_pattern_in_tree(tree, pattern)
    if sub_result:
        for item in sub_result:
            column = sub_result[item]['COLUMN']
            return column   # Only need first one
    pattern = '00PP'.replace('P',str(player))
    sub_result = find_pattern_in_tree(tree, pattern)
    if sub_result:
        for item in sub_result:
            column = sub_result[item]['COLUMN']
            return column   # Only need first one
    pattern = 'PP00'.replace('P',str(player))
    sub_result = find_pattern_in_tree(tree, pattern)
    if sub_result:
        for item in sub_result:
            column = sub_result[item]['COLUMN']
            return column   # Only need first one
    return False
