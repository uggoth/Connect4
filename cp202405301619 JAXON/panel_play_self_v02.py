# Score each panel member on games against the others

import game_utils_v05 as game_utils
dbu = game_utils.dbu
mysql = game_utils.mysql
parms = game_utils.parms
pickle = game_utils.pickle
copy = game_utils.copy
import player_v02 as player
import panel_v12 as panel
import game_v09 as c4game
import sys

conn = dbu.get_conn()
my_cursor = dbu.get_cursor(conn)

species = parms.species

game_id = dbu.get_next_id('GAME',8)
game = c4game.Connect4Game(no_columns=parms.game_columns,
                        no_rows=parms.game_rows,
                        name=game_id,
                        winning_run=4)

panel_count = 0
sql = ("SELECT panel_id, panel_desc FROM panels WHERE species = '" + species + "'")
my_cursor.execute(sql)
for row in my_cursor:
    if panel_count == 0:
        print ("List of panels in " + species)
    print (row['panel_id'] + ' ' + row['panel_desc'])
    panel_count += 1
if panel_count == 0:
    print ("No panels found")
    raise SystemExit
else:
    print (" ")

first_time = True
panel_ok = False
while not panel_ok:
    if first_time:
        prompt = "Enter Panel ID (Default " + parms.current_panel + "): "
        first_time = False
    else:
        prompt = "Panel " + panel_id + " not found. Enter Panel ID: "
    panel_id = input(prompt)
    if not panel_id:
        panel_id = parms.current_panel
    sql = ("SELECT COUNT(*) as count, lowest_acceptable_score FROM panels WHERE panel_id = '" + panel_id + "'")
    my_cursor.execute(sql)
    row = my_cursor.fetchone()
    if row['count'] > 0:
        panel_lowest_acceptable_score = row['lowest_acceptable_score']
        panel_ok = True

my_panel = panel.Panel(panel_id)
my_panel.link(game)

big_score = 99999
lowest_acceptable_score = big_score

nets_found = 0

for panellist_id in my_panel.panellists:
    this_panellist = my_panel.panellists[panellist_id]
    player_id = this_panellist['ID']
    print ('Testing ' + panellist_id + ' ' + player_id)
    candidate = this_panellist['INSTANCE']
    if not candidate:
        print ('Failed to load ' + panellist_id)
        continue
    result = my_panel.do_tests(candidate)
    if result and result['SUCCESS']:
        player_type = player_id[0:4]
        if 'RBOT' == player_type:
            candidate_name = candidate.robot_name
        else:
            candidate_name = 'Network'
        candidate_string = "{:12}".format(" (" + candidate_name + ") ")
        score = result['SCORE']
        print (player_id + candidate_string + 'Scored: ' + str(score))
        if 'RBOT' != player_type:
            nets_found += 1
            if score < lowest_acceptable_score:
                lowest_acceptable_score = score
        sql = ("UPDATE panellists SET score = " + str(score) +
               " WHERE panellist_id = '" + panellist_id + "' AND panel_id = '" + panel_id + "'")
        my_cursor.execute(sql)
        conn.commit()
    else:
        print (panellist_id + ' ** TEST ERROR **')

if lowest_acceptable_score < big_score:
    sql = ("UPDATE panels SET lowest_acceptable_score = " + str(lowest_acceptable_score) +
           " WHERE panel_id = '" + panel_id + "'")
    my_cursor.execute(sql)
    print ("Panel Lowest Acceptable Score set to: " + str(lowest_acceptable_score))
else:
    print ("Panel Lowest Acceptable Score left at: " + str(panel_lowest_acceptable_score))

sql = ("SELECT player_id, player_name, score FROM panellists WHERE " +
       "panel_id='" + panel_id + "' AND SUBSTRING(player_id,1,4) != 'RBOT' ORDER BY score DESC")
result = my_cursor.execute(sql)
if result:
    rows = my_cursor.fetchall()
    index = 0
    for row in rows:
        index += 1
        print ("{:3} {:13} {:13} {:5}".format(index, row['player_id'],row['player_name'],row['score']))

if nets_found > 0:
    prune = input("Enter number of networks to keep in panel, or 0 for all ")
    pint = int(prune)
    if pint > 0:
        deletes = []
        sql = ("SELECT player_id, player_name, score FROM panellists WHERE " +
               "panel_id='" + panel_id + "' AND SUBSTRING(player_id,1,4) != 'RBOT' ORDER BY score DESC")
        result = my_cursor.execute(sql)
        if result:
            rows = my_cursor.fetchall()
            index = 0
            for row in rows:
                index += 1
                if index > pint:
                    deletes.append(row['player_id'])
        for player_id in deletes:
            sql = ("DELETE FROM panellists WHERE panel_id = '" + panel_id + "' AND player_id = '" + player_id + "'")
            my_cursor.execute(sql)
        print ('Run again to renormalise scores')


conn.commit()
my_cursor.close()
conn.close()
