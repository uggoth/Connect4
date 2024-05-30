#   produces variations on an existing neural network

import game_utils_v05 as game_utils
dbu = game_utils.dbu
mysql = game_utils.mysql
parms = game_utils.parms
pickle = game_utils.pickle
copy = game_utils.copy
import random
import time
import neural_network_v18 as nn
import game_v09 as c4g
import panel_v12 as panel
import statistics

def tweak_weights(parent_net):
    cloned_net = copy.deepcopy(parent_net)
    child_id = dbu.get_next_id('CNET', 8)
    cloned_net.id = child_id
    cloned_net.name = child_id
    cloned_net.parent_id = parent_net.id
    if hasattr(parent_net, 'genealogy'):
        cloned_net.genealogy = parent_net.genealogy + ' ' + parent_net.id
    else:
        cloned_net.genealogy = parent_net.id
    logic_layer = cloned_net.layer_list[1]
    tweak_layer(logic_layer)
    motor_layer = cloned_net.act_layer
    tweak_layer(motor_layer)
    return cloned_net

def tweak_layer(this_layer):
    synapse_count = 0
    synapse_weights = 0
    for synapse in this_layer.synapse_list:
        synapse_count += 1
        synapse_weights += synapse.weight
    average_weight = synapse_weights / synapse_count
    for synapse in this_layer.synapse_list:
        old_weight = synapse.weight
        if old_weight > -100:   # ignore manual inhibitory synapses
            tweak_factor = random.uniform(-1,1)
            new_weight = old_weight + (average_weight * tweak_factor)
            synapse.weight = new_weight

def save_child(network, total_score, session_id):
    net_id = network.id
    table = 'child_nets'
    network.save_self_to_database(table, session_id)
    return net_id

def save_net(network, total_score):
    global session_id
    net_id = dbu.get_next_id('VNET')
    print ("Saving " + net_id + ", Score: " + str(total_score))
    network.score = total_score
    network.id = net_id
    table = 'nets'
    network.save_self_to_database(table, session_id)
    return net_id

def prompt_for(prompt, default):
    full_prompt = prompt + " - (default " + str(default) + "): "
    reply = raw_input(full_prompt)
    if reply == '':
        return default
    else:
        return reply

def score_child(child_net):
    sub_result = my_panel.do_tests(child_net)
    if not sub_result['SUCCESS']:
        return 0
    wins_as_2 = sub_result['WINS_AS_2']
    wins_as_1 = sub_result['WINS_AS_1']
    draws = sub_result['DRAWS']
    losses = sub_result['LOSSES']
    score = game_utils.get_score(wins_as_2, wins_as_1, draws, losses)
    return (score)

start_time = time.time()
start_time_s = time.strftime('%H:%M:%S')

print (' ')
print ('Variegator of ' + parms.species + ' Starting at ' + start_time_s)
print (' needs ' + str(parms.min_successes) + ' successes to save session *****')
print (' ')

conn = dbu.get_conn()
my_cursor = dbu.get_cursor(conn)

game_name = dbu.get_next_id('GAME',8)
game = c4g.Connect4Game(no_columns=parms.game_columns, no_rows=parms.game_rows,
                        name=game_name, winning_run=parms.game_winning_run)

###############################################################

my_panel = panel.Panel(parms.current_panel)
my_panel.link(game)

###############################################################

game_count = len(my_panel.panellists) * 2

print ('Game ' + game.name + ' to be played ' + str(game_count) + ' times')

new_nets_made = 0

for i in range(parms.iterations):
    session_id = dbu.get_next_id('VSES', 8)
    
    sql = ("SELECT lowest_acceptable_score FROM sessions WHERE session_id = '" + parms.session_id + "'")
    my_cursor.execute(sql)
    row=my_cursor.fetchone()
    lowest_acceptable_score = row['lowest_acceptable_score']

    my_count = 0
    while my_count == 0:
        time.sleep(1)
        sql = ("SELECT COUNT(*) AS my_count FROM nets " +
               "WHERE species = '" + parms.species + "'")
        my_cursor.execute(sql)
        row=my_cursor.fetchone()
        my_count = row['my_count']

    sql = ('SELECT net_id, filename, evolves, score, instance FROM nets ' +
           'WHERE species = \'' + parms.species + '\' ' +
           'ORDER BY evolves ASC, score DESC LIMIT 1')
    my_cursor.execute(sql)
    row=my_cursor.fetchone()
    parent_net_id = row['net_id']
    filename = row['filename']
    evolves = int(row['evolves'])
    parent_score = int(row['score'])
    instance = row['instance']

    new_evolves = evolves + 1

    sql = 'UPDATE nets SET evolves = ' + str(new_evolves) + ' WHERE net_id = \'' + parent_net_id + '\''
    my_cursor.execute(sql)

    parent_net = pickle.loads(instance)
    # repeat tests in case panel has changed
    sub_result = my_panel.do_tests(parent_net)
    
    if not sub_result['SUCCESS']:
        break
    wins_as_2 = sub_result['WINS_AS_2']
    wins_as_1 = sub_result['WINS_AS_1']
    draws = sub_result['DRAWS']
    losses = sub_result['LOSSES']

    parent_score = game_utils.get_score(wins_as_2, wins_as_1, draws, losses)
    total_wins = wins_as_2 + wins_as_1

    successes = 0

    children = []
    scores = []
    print ('\nTesting Base ' + 'Net ' + parent_net.id + ' score: ' + str(parent_score) + ', wins: ' + str(total_wins))

    for j in range(parms.attempts):
        child_net = tweak_weights(parent_net)
        child_id = child_net.id
        child_score = score_child(child_net)
        child_net.score = child_score
        improvement = child_score - parent_score
        if improvement == 0:
            break
        if child_score in scores:
            break
        if ((improvement > 0) and (child_score >= lowest_acceptable_score)):
            version_id = save_net(child_net, child_score)
            print ('Net ' + version_id + ' improvement: ' + str(improvement) + ' saved to main nets table')
        if child_score >= (parent_score - parms.max_deterioration):
            successes += 1
            children.append(child_net)
            scores.append(child_score)
            print ('Net ' + child_id + ' improvement: ' + str(improvement) + ' added to set')
        if successes > parms.max_successes:
            break

    if successes >= parms.min_successes:
        variability = statistics.stdev(scores)
        print (session_id + ' successes ' + str(successes) + ' variability: ' + str(variability))
        for child_net in children:
            child_id = save_child(child_net, child_net.score, session_id)
        save_child(parent_net, parent_score, session_id)
        sql = ("INSERT INTO variegation_sessions " +
               "(session_id, available, parent_net, parent_score, species, variability) VALUES (" +
               "'" + session_id + "',1,'" + parent_net_id + "'," + str(parent_score) + ",'" +
               parms.species + "'," + str(variability) + ")")
        my_cursor.execute(sql)
    else:
        print ("Session " + session_id + " unproductive. Not saved")

print ("\nFinished")

my_cursor.close()
conn.close()
