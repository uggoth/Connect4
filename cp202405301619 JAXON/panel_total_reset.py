# Clear out the nets, child_nets, and variegation_sessions files
# seed the nets file with panel members

import game_utils_v05 as game_utils
dbu = game_utils.dbu
mysql = game_utils.mysql
parms = game_utils.parms
pickle = game_utils.pickle
copy = game_utils.copy

conn = dbu.get_conn()
my_cursor = dbu.get_cursor(conn)

sql = "TRUNCATE TABLE nets"
my_cursor.execute(sql)

sql = "TRUNCATE TABLE child_nets"
my_cursor.execute(sql)

sql = "TRUNCATE TABLE variegation_sessions"
my_cursor.execute(sql)

species = parms.species

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

sql = ("SELECT player_id, player_instance, score " +
       "FROM panellists WHERE panel_id = '" + panel_id + "' AND SUBSTR(player_id,1,4) <> 'RBOT'")
my_cursor.execute(sql)
for row in my_cursor:
    print ("Saving " + row['player_id'])
    instance = pickle.loads(row['player_instance'])
    instance.score = row['score']
    instance.save_self_to_database()
        
my_cursor.close()
conn.close()
