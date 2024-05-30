import database_utils_v04 as dbu
mysql = dbu.mariadb
import parameters_v35 as parms
import sys

conn = dbu.get_conn()
my_cursor = dbu.get_cursor(conn)

species = parms.species

panel_count = 0
sql = ("SELECT panel_id, panel_desc FROM panels WHERE species = '" + species + "'")
my_cursor.execute(sql)
for row in my_cursor:
    if panel_count == 0:
        print ("List of panels:")
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
        prompt = "Enter Panel ID: "
        first_time = False
    else:
        prompt = "Panel " + panel_id + " not found. Enter Panel ID: "
    panel_id = input(prompt)
    sql = ("SELECT species FROM panels WHERE panel_id = '" + panel_id + "'")
    my_cursor.execute(sql)
    row = my_cursor.fetchone()
    if row:
        species = row['species']
        panel_ok = True
    else:
        print ("** Species not found **")
        sys.exit(1)

existing_panellists = []
sql = ("SELECT player_id, player_name FROM panellists WHERE panel_id = '" + panel_id + "'")
result = my_cursor.execute(sql)
if result:
    rows = my_cursor.fetchall()
    if rows:
        print ("Panel already contains:")
        for row in rows:
            existing_panellists.append(row[0])
            print (row[0] + ' ' + row[1])
    else:
        print ('Panel currently empty')
else:
    print ('Panel currently empty')

sql = ("SELECT robot_id, robot_name FROM robots WHERE species = '" + species + "'")
my_cursor.execute(sql)
print (" ")
found_one = False
for row in my_cursor:
    robot_id = row['robot_id']
    robot_name = row['robot_name']
    if robot_id not in existing_panellists:
        if not found_one:
            print ("Robots available are:")
            found_one = True
        print (robot_id + ' ' + robot_name)
if not found_one:
    print ('No robots found')

prompt = "Enter Robot ID: "
while True:
    try:
        robot_id = input(prompt)
        if robot_id == '':
            break
        sql = ("SELECT COUNT(*) AS existing FROM panellists WHERE panel_id = '" + panel_id + "' AND player_id = '" + robot_id + "'")
        my_cursor.execute(sql)
        row = my_cursor.fetchone()
        if row['existing'] == 0:     # it's a new entry
            panellist_id = dbu.get_next_id('PNST', 8)
            sql = ("SELECT robot_instance, robot_name FROM robots WHERE robot_id = '" + robot_id + "'")
            my_cursor.execute(sql)
            row = my_cursor.fetchone()
            score = 0
            sql = ("INSERT INTO panellists (panellist_id, panel_id, score, player_id, player_instance, player_name) " +
                   "VALUES (%s,%s,%s,%s,%s,%s)")
            #prepared_cursor = conn.cursor()
            #result = prepared_cursor.execute(sql, (panellist_id, panel_id, score,
            #                                      robot_id, row['robot_instance'], row['robot_name']))
            my_cursor.execute(sql, (panellist_id, panel_id, score,
                                                   robot_id, row['robot_instance'], row['robot_name']))
        else:
            print ("panellist " + robot_id + " already a member")
    except EOFError:
        break

print ("Don't forget to run panel_play_self to nomalise the scores")

conn.commit()
my_cursor.close()
conn.close()
