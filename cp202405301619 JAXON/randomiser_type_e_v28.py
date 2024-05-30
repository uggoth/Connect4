# generate random nets

import game_utils_v05 as game_utils
dbu = game_utils.dbu
mysql = game_utils.mysql
parms = game_utils.parms
pickle = game_utils.pickle
import random
import time
import game_v09 as c4game
import panel_v12 as panel
import neural_network_v18 as nn

def make_random_net(network_name, method, thresholds, game_columns, game_rows, species,
                    logic_threshold_low, logic_threshold_high,
                    motor_threshold_low, motor_threshold_high,
                    logic_weight_low, logic_weight_high,
                    motor_weight_low, motor_weight_high,
                    logic_count_low, logic_count_high,
                    memory_count_low, memory_count_high):

    this_net = nn.Network(network_name, method, thresholds, species)

    input_layer = nn.Input_Layer('SENSOR_LAYER', this_net)

    for x in range(game_columns):
        column = x + 1
        row = 0     # irrelevant for column sensors
        coords = str(column) + str(row)
        
        #neuron_type = 'MY_CONSECUTIVES_2'
        #name = neuron_type + '_' + coords
        #neuron = nn.Connect_4_Sensor_Neuron(name, input_layer, column, row)
        #neuron.type = neuron_type

        neuron_type = 'HIS_CONSECUTIVES_2'
        name = neuron_type + '_' + coords
        neuron = nn.Connect_4_Sensor_Neuron(name, input_layer, column, row)
        neuron.type = neuron_type

    for column in [4,5,3,6,2,7,1]:
        row = 0     # irrelevant for column sensors
        coords = str(column) + str(row)
        neuron_type = 'COLUMN'
        name = 'C_EMPTY' + '_' + coords
        neuron = nn.Connect_4_Sensor_Neuron(name, input_layer, column, row)
        neuron.type = neuron_type
        neuron.stimulus = 0

    logic_layer = nn.Logic_Layer('LOGIC_LAYER', this_net)
    logic_count = int(random.uniform(logic_count_low, logic_count_high))
    this_net.logic_count = logic_count
    memory_count = int(random.uniform(memory_count_low, memory_count_high))
    this_net.memory_count = memory_count
    logic_layer.populate(logic_count, memory_count, method)
    logic_layer.link_back()
    logic_layer.randomise_weights(logic_weight_low, logic_weight_high)
    logic_layer.randomise_thresholds(logic_threshold_low, logic_threshold_high)

    motor_layer = nn.Output_Layer('MOTOR_LAYER', this_net)
    for x in range(game_columns):
        column = x + 1
        name = 'MN' + str(column)
        neuron = nn.Connect_4_Motor_Neuron(name, motor_layer, 0, method)
        neuron.column = column
    motor_layer.link_back()
    motor_layer.randomise_weights(motor_weight_low, motor_weight_high)
    motor_layer.randomise_thresholds(motor_threshold_low, motor_threshold_high)

    # hand-coded stuff ('instincts')

    sense_directory = this_net.sense_layer.neuron_directory
    motor_directory = this_net.act_layer.neuron_directory

    # hand-coded excitatory synapse to encourage starting in the centre of the game
    sense_neuron = sense_directory['C_EMPTY_40']
    motor_neuron = motor_directory['MN' + str(column)]
    result = nn.Synapse(motor_layer,sense_neuron,motor_neuron,9)

    # hand-coded preference for 4 in a row for this player
    #for x in range(game.no_columns):
    #    column = x + 1
    #    coords = str(column) + '0'
    #    sense_neuron = sense_directory['MY_CONSECUTIVES_2_' + coords]
    #    motor_neuron = motor_directory['MN' + str(column)]
    #    result = nn.Synapse(motor_layer,sense_neuron,motor_neuron,999999)

    # hand-coded preference to block 4 in a row for opponent
    for x in range(game.no_columns):
        column = x + 1
        coords = str(column) + '0'
        sense_neuron = sense_directory['HIS_CONSECUTIVES_2_' + coords]
        motor_neuron = motor_directory['MN' + str(column)]
        result = nn.Synapse(motor_layer,sense_neuron,motor_neuron,99999)

    return this_net

def print_inhibitory_synapses(this_net):
    for x in range(parms.game_columns):
        column = x + 1
        for y in range(parms.game_no_rows):
            row = y + 1
            red = this_net.sense_layer.neuron_directory['S_RED_' + str(column) + str(row)]
            yellow = this_net.sense_layer.neuron_directory['S_YELLOW_' + str(column) + str(row)]
            print ('Column ' +  str(column) +
                   ' Row ' + str(row) + '  RED ' + str(red.output) + '  YELLOW ' + str(yellow.output))

def set_lowest_acceptable_score(score):
    global lowest_acceptable_score, my_cursor, conn
    lowest_acceptable_score = score
    sql = ("INSERT INTO sessions (session_id, lowest_acceptable_score) " +
           "VALUES ('" + parms.session_id + "', " + str(lowest_acceptable_score) + ") "
           "ON DUPLICATE KEY UPDATE lowest_acceptable_score=" + str(lowest_acceptable_score))
    my_cursor.execute(sql)
    conn.commit()

now_time_s = time.strftime('%H:%M:%S')
print (' ')
print ('****** Randomiser ** Type F (instinct to make 4) ** starting at ' + now_time_s + ' **** ')
print (' ')

conn = dbu.get_conn()
my_cursor = dbu.get_cursor(conn)

method_list = ['SIGMOIDAL','DIGITAL','SIGMOIDAL','ANALOGUE','SIGMOIDAL']
mlen = len(method_list) # sigmoidal expected to be best, but just in case

thresholds_list = [True, True, True, False, True, False, True]
tlen = len(thresholds_list)

start_time = time.time()

game_id = dbu.get_next_id('GAME',8)
game = c4game.Connect4Game(no_columns=parms.game_columns,
                        no_rows=parms.game_rows,
                        name=game_id,
                        winning_run=4)

print ('Species ' + parms.species)


###############################################################

my_panel = panel.Panel(parms.current_panel)
my_panel.link(game)

###############################################################

print ('Panel ' + my_panel.panel_id + ' ' + my_panel.panel_desc)

game_count = len(my_panel.panellists) * 2

print ('Game ' + game.name + ' to be played ' + str(game_count) + ' times')

sql = ("SELECT COUNT(*) as count FROM panellists WHERE panel_id = '" + parms.current_panel + "'")
my_cursor.execute(sql)
row = my_cursor.fetchone()
if row:
    panellists_count = row['count']
else:
    print ("**failed** " + sql)
    exit(1)

max_score = ((panellists_count * parms.win_as_1_score) + (panellists_count * parms.win_as_2_score))
print ("Maximum possible score is " + str(max_score))

set_lowest_acceptable_score(my_panel.lowest_acceptable_score - parms.max_deterioration)

print ('Lowest acceptable score: ' + str(lowest_acceptable_score))

answer = input("Clear out old nets? ")
if ((answer == 'y') or (answer == 'Y')):
    sql = "TRUNCATE TABLE nets"
    my_cursor.execute(sql)
    sql = "TRUNCATE TABLE child_nets"
    my_cursor.execute(sql)
    sql = "TRUNCATE TABLE variegation_sessions"
    my_cursor.execute(sql)  

nets_per_run = 0
scores = {}

for session in range(parms.sessions_count):
    print ("\nSession " + str(session+1) + "\n")
    consecutive_unsaved = 0
    nets_per_session = 0
    score_raised = False
    for trial in range(parms.trials_count):
        nets_per_trial = 0
        net_name = dbu.get_next_id('RNET', 8)

        logic_threshold_low = random.uniform(parms.logic_threshold_low_low, parms.logic_threshold_low_high)
        logic_threshold_high = random.uniform(parms.logic_threshold_high_low, parms.logic_threshold_high_high)
        logic_weight_low = random.uniform(parms.logic_weight_low_low, parms.logic_weight_low_high)
        logic_weight_high = random.uniform(parms.logic_weight_high_low, parms.logic_weight_high_high)
        motor_threshold_low = random.uniform(parms.motor_threshold_low_low, parms.motor_threshold_low_high)
        motor_threshold_high = random.uniform(parms.motor_threshold_high_low, parms.motor_threshold_high_high)
        motor_weight_low = random.uniform(parms.motor_weight_low_low, parms.motor_weight_low_high)
        motor_weight_high = random.uniform(parms.motor_weight_high_low, parms.motor_weight_high_high)
        logic_count_low = parms.logic_count_low
        logic_count_high = parms.logic_count_high
        memory_count_low = parms.memory_count_low
        memory_count_high = parms.memory_count_high
        mindex = trial % mlen
        method = method_list[mindex]
        tindex = trial % tlen
        thresholds = thresholds_list[tindex]

        candidate_net = make_random_net(net_name, method, thresholds, parms.game_columns, parms.game_rows, parms.species,
                                 logic_threshold_low, logic_threshold_high, motor_threshold_low, motor_threshold_high,
                                 logic_weight_low, logic_weight_high, motor_weight_low, motor_weight_high,
                                 logic_count_low, logic_count_high, memory_count_low, memory_count_high)
        candidate_net.debug_level = 0                               #########################################
        result = my_panel.do_tests(candidate_net, recording=False)   #########################################
        if not result['SUCCESS']:
            break
        wins_as_2 = result['WINS_AS_2']
        wins_as_1 = result['WINS_AS_1']
        draws = result['DRAWS']
        losses = result['LOSSES']

        score = game_utils.get_score(wins_as_2, wins_as_1, draws, losses)
        total_wins = wins_as_2 + wins_as_1
        score_string = 'Net ' + candidate_net.id + ' score: ' + str(score) + ', wins: ' + str(total_wins)
        if total_wins < 1:
            #print (score_string + ' not saved because did not win any games')
            consecutive_unsaved += 1
        elif score >= lowest_acceptable_score:
            score_index = '{:9}'.format(score)
            if score_index in scores:
                scores[score_index] += 1
            else:
                scores[score_index] = 1
            candidate_net.score = score
            now_time = time.time()
            now_time_s = time.strftime('%H:%M:%S')
            time_diff = str(int(now_time - start_time))
            if candidate_net.thresholds:
                ts = ' Thresholds ON'
            else:
                ts = ' Thresholds OFF'
            candidate_net.save_self_to_database()
            if parms.save_to_folder:
                candidate_net.export_self_to_file()
                folder_string =  'to ' + parms.net_folder
            else:
                folder_string = ''
            print (str(nets_per_session + 1) + '  ' + score_string +
                   ' method ' + candidate_net.standard_method + ts + ' saved ' + folder_string +
                   ' at ' + now_time_s + ' after ' + time_diff + ' seconds')
            nets_per_trial += 1
            if nets_per_trial > parms.max_nets_per_trial:
                lowest_acceptable_score += 1
                print ("\nLowest acceptable score set to: " + str(lowest_acceptable_score) + ' during session')
                score_raised = True
                break
            nets_per_session += 1
            if nets_per_session > parms.max_nets_per_session:
                break
        else:
            #print (score_string + ' not saved because score < ' + str(lowest_acceptable_score))
            consecutive_unsaved += 1
            if consecutive_unsaved % parms.warn_interval == 0:
                now_time_s = time.strftime('%H:%M:%S')
                print (str(consecutive_unsaved) + ' nets unsaved at ' + now_time_s)
        if nets_per_session > parms.max_nets_per_session:
            break
    
    if nets_per_session > 0:
        print (str(nets_per_session) + ' new nets made in session ' + str(session + 1))
    else:
        print ('No new nets made in session ' + str(session + 1))
        break
    set_lowest_acceptable_score(lowest_acceptable_score + 1)
    print ("\nLowest acceptable score set to: " + str(lowest_acceptable_score) + ' at end of session')
    nets_per_run += nets_per_session

my_cursor.close()
conn.close()
print (' ')
print ("Randomiser finished after " + str(session+1) + " sessions")
print (str(nets_per_run) + " nets created. Scores were:")
print (" Score      Nets count")
for index in sorted(scores):
    print (index + "{:5}".format(scores[index]))
print ('Finished')
