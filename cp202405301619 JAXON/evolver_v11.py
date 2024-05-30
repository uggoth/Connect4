#   produces variations on an existing neural network

import game_utils_v05 as game_utils
dbu = game_utils.dbu
mysql = game_utils.mysql
parms = game_utils.parms
pickle = game_utils.pickle
copy = game_utils.copy
import random
import time
from scipy.stats import pearsonr
import neural_network_v18 as nn
import panel_v12 as panel
import game_v09 as c4g

def evolve_layer(base_net, next_gen_net, which_layer, net_list):
    sindex = 0
    base_layer = base_net.layer_list[which_layer]
    next_gen_layer = next_gen_net.layer_list[which_layer]
    for synapse in base_layer.synapse_list:
        x = []
        y = []
        for net in net_list:
            xval = net.layer_list[which_layer].synapse_list[sindex].weight
            yval = net.score
            x.append(float(xval))
            y.append(float(yval))
        r_value,p_value = pearsonr(x, y)
        #print ("Pearson R: " + str(r_value) + ",  P: " + str(p_value))
        min_r = -0.1
        if abs(r_value) > min_r:
        #if True:
            old_w = next_gen_net.layer_list[which_layer].synapse_list[sindex].weight
            new_w = old_w * (1.0 + (r_value / 100.0))
            #print ('old_w: ' + str(old_w) + ',  new_w: ' + str(new_w))
            next_gen_net.layer_list[which_layer].synapse_list[sindex].weight = new_w
        sindex += 1
    return sindex

def evolve(base_net, net_list, i):
    next_gen_net = copy.deepcopy(base_net)
    next_id = dbu.get_next_id('ENET', 8)
    next_gen_net.name = next_id
    next_gen_net.id = next_id
    if i < 1:
        if hasattr(base_net, 'genealogy'):
            next_gen_net.genealogy = base_net.genealogy + ' ' + base_net.id
        else:
            next_gen_net.genealogy = base_net.id
        next_gen_net.parent_id = base_net.id
    evolve_layer(base_net, next_gen_net, 1, net_list)
    evolve_layer(base_net, next_gen_net, 2, net_list)
    return next_gen_net

now_time_s = time.strftime('%H:%M:%S')
print (' ')
print ('*************** Evolver starting at ' + now_time_s + ' ********************')
print (' ')
conn = dbu.get_conn()
my_cursor = dbu.get_cursor(conn)

net_folder = 'Nets'

game_name = dbu.get_next_id('GAME',8)
game = c4g.Connect4Game(no_columns=parms.game_columns, no_rows=parms.game_rows,
                        name=game_name, winning_run=parms.game_winning_run)

print ('Species ' + parms.species)

my_panel = panel.Panel(parms.current_panel)
my_panel.link(game)

game_count = len(my_panel.panellists) * 2
print ('Game ' + game.name + ' to be played ' + str(game_count) + ' times')

iterations = 999
attempts = 11

new_nets_made = 0
start_time = time.time()

for i in range(iterations):

    sql = ("SELECT lowest_acceptable_score FROM sessions WHERE session_id = '" + parms.session_id + "'")
    my_cursor.execute(sql)
    row=my_cursor.fetchone()
    lowest_acceptable_score = row['lowest_acceptable_score']

    sql = ("SELECT session_id, parent_net, parent_score, variability FROM variegation_sessions " +
           "WHERE species='" + parms.species + "' AND available = 1 ORDER BY variability DESC LIMIT 1")
    my_cursor.execute(sql)
    row = my_cursor.fetchone()

    if row is None:
        print ('sleeping')
        time.sleep(100)
    else:
        session_id = row['session_id']
        base_net_id = row['parent_net']
        parent_score = row['parent_score']
        variability = row['variability']
        sql = "UPDATE variegation_sessions SET available = 0 WHERE session_id = '" + session_id + "'"
        my_cursor.execute(sql)
        conn.commit()

        print ('\nSession ' + session_id + ', variability ' + str(variability) + ', Base Net ' + base_net_id +
               ' score: ' + str(parent_score))

        sql = "SELECT net_id, instance, score FROM child_nets WHERE session = '" + session_id + "'"
        my_cursor.execute(sql)
        rows = my_cursor.fetchall()
        best_score = 0
        best_id = ''

        variants = {}
        net_list = []

        for row in rows:
            net_id = row['net_id']
            score = row['score']
            print ("Adding " + net_id + " " + str(score) + " to set")
            variants[net_id] = {}
            instance = pickle.loads(row['instance'])
            variants[net_id]['INSTANCE'] = instance
            net_list.append(instance)
            variants[net_id]['SCORE'] = score
            if score > best_score:
                best_score = score
                best_id = net_id

        base_net = variants[best_id]['INSTANCE']
        base_score = variants[best_id]['SCORE']
        print ("Evolving " + best_id + ' ' + str(base_score))

        generations = []
        different_scores = []


        for j in range(attempts):
            #print ('Iteration ' + str(j))
            if j < 1:
                evolved_net = evolve(base_net, net_list, j)
                generations.append(evolved_net)
                previous_score = evolved_net.score
                #print (evolved_net.id + ' ' + str(evolved_net.score))
            else:
                evolved_net = generations[j-1]
                #print (evolved_net.id)
                next_gen_net = evolve(evolved_net, net_list, j)
                generations.append(next_gen_net)
                #print (next_gen_net.id + str(next_gen_net.score))
                if (previous_score - parms.max_deterioration) > next_gen_net.score:
                    break
                else:
                    previous_score = next_gen_net.score
 
            sub_result = my_panel.do_tests(evolved_net)
            if not sub_result['SUCCESS']:
                break
            wins_as_2 = sub_result['WINS_AS_2']
            wins_as_1 = sub_result['WINS_AS_1']
            draws = sub_result['DRAWS']
            losses = sub_result['LOSSES']
            score = game_utils.get_score(wins_as_2, wins_as_1, draws, losses)
            comment = ''
            if score > base_score:
                comment = '** GOOD SCORE ** '
            total_wins = wins_as_2 + wins_as_1
            #print (comment + 'Net ' + evolved_net.id + ' score: ' + str(score) + ', after: ' + str(j) + ' iterations')
            ng_score = score
            generations[j].score = ng_score

            if ng_score not in different_scores:
                different_scores.append(ng_score)
                if ((ng_score > base_score) and (ng_score >= lowest_acceptable_score)):
                    new_nets_made += 1
                    now_time = time.time()
                    time_diff = now_time - start_time
                    print ('Evolved Net No. ' + str(new_nets_made) + '  ' +
                           generations[j].name + ' scored ' + str(ng_score) +
                           ' after ' + '{0:05}'.format(int(time_diff)) + ' seconds')
                    generations[j].save_self_to_database()
        scores = str(base_score)
        for score in different_scores:
            scores += ' ' + str(score)
        print ("Different scores: " + scores)
        sql = ("DELETE FROM child_nets WHERE session = '" + session_id + "'")
        my_cursor.execute(sql)
        sql = ("DELETE FROM variegation_sessions WHERE session_id = '" + session_id + "'")
        my_cursor.execute(sql)
        conn.commit()

my_cursor.close()
conn.close()

print ('Finished')
