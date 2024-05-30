# don't forget to run panel_play_self.py afterwards to nomalise the scores

import database_utils_v04 as dbu
mysql = dbu.mariadb
import parameters_v35 as parms

conn = dbu.get_conn()
my_cursor = dbu.get_cursor(conn)

panel_count = 0
sql = ("SELECT panel_id, panel_desc FROM panels")
my_cursor.execute(sql)
for row in my_cursor:
    if panel_count == 0:
        print ("List of panels:")
    print (row['panel_id'] + ' ' + row['panel_desc'])
    panel_count += 1
if panel_count < 1:
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

existing_panellists = []
sql = ("SELECT player_id, player_name, score FROM panellists " +
       "WHERE panel_id = '" + panel_id + "' ORDER BY score DESC")
my_cursor.execute(sql)
no_panellists = 0
for row in my_cursor:
    if no_panellists == 0:
        print ("Panel already contains:")
    existing_panellists.append(row['player_id'])
    print ("  " + row['player_id'] + "  {:14}".format(row['player_name']) + "  {:3}".format(row['score']))
    no_panellists += 1
if no_panellists < 1:
    print ('Panel currently empty')

sql = ("SELECT net_id, score FROM nets " +
       "WHERE species = '" + parms.species + "'" +
       "ORDER BY score DESC LIMIT 20")
my_cursor.execute(sql)
rows = my_cursor.fetchall()
found_one = False
if rows is not None:
    for row in rows:
        player_id = row['net_id']
        score = row['score']
        if score:
            score_string = ' Score {:3d}'.format(int(score))
        else:
            score_string = ' Score 000'
        player_string = player_id + score_string
        if player_id not in existing_panellists:
            if not found_one:
                print ("\nEnter y to select n to quit, or anything else to skip:")
                found_one = True
            selected = input("Add " + player_string + "? ")
            if ((selected == 'y') or (selected == 'Y')):
                panellist_id = dbu.get_next_id('PNST', 8)
                sql = ("SELECT instance FROM nets WHERE net_id = '" + player_id + "'")
                my_cursor.execute(sql)
                row = my_cursor.fetchone()
                score = 0
                sql = ("INSERT INTO panellists (panellist_id, panel_id, score, player_id, player_instance, player_name) " +
                       "VALUES (%s,%s,%s,%s,%s,%s)")
                my_cursor.execute(sql, (panellist_id, panel_id, score, player_id, row['instance'], player_id))
            elif ((selected == 'n') or (selected == 'N')):
                break
            else:
                continue

if not found_one:
    print ("No Nets available")
else:
    print ('Run panel_play_self')
conn.commit()
my_cursor.close()
conn.close()
