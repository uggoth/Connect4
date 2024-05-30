# Ask each panel member what move to play next

import panel_v11 as panel
import game_utils_v02 as game_utils
import game_v09 as c4game
import database_utils_v02 as dbu
mysql = dbu.mysql
import parameters_v34 as parms
import player_v02 as player

conn = dbu.get_dict_conn()
my_cursor = conn.cursor()

species = parms.species

game_id = dbu.get_next_id('GAME',8)
game = c4game.Connect4Game(no_columns=parms.game_columns,
                        no_rows=parms.game_rows,
                        name=game_id,
                        winning_run=4)

panel_count = 0
sql = ("SELECT panel_id, panel_desc FROM panels WHERE species = '" + species + "'")
result = my_cursor.execute(sql)
if result:
    rows = my_cursor.fetchall()
    for row in rows:
        if panel_count == 0:
            print ("List of panels in " + species)
        print (row['panel_id'] + ' ' + row['panel_desc'])
        panel_count += 1
else:
    print ("** DATABASE ERROR **")
    sys.exit(1)
if panel_count == 0:
    print ("No panels found")
    raise SystemExit
else:
    print (" ")

first_time = True
#panel_id = 'PANL00000011'
panel_ok = False
while not panel_ok:
    if first_time:
        prompt = "Enter Panel ID: "
        first_time = False
    else:
        prompt = "Panel " + panel_id + " not found. Enter Panel ID: "
    panel_id = raw_input(prompt)
    sql = ("SELECT COUNT(*) as count, lowest_acceptable_score FROM panels WHERE panel_id = '" + panel_id + "'")
    result = my_cursor.execute(sql)
    if result:
        row = my_cursor.fetchone()
        if row['count'] > 0:
            panel_lowest_acceptable_score = row['lowest_acceptable_score']
            panel_ok = True
    else:
        print ("** DATABASE ERROR **")
        sys.exit(1)

my_panel = panel.Panel(panel_id)
my_panel.link(game)

default_selector = 'B'
selector = raw_input("Test States Selector. Default " + default_selector + ": ")
if selector == '':
    selector = default_selector

sql = ("SELECT test_state_id, state_string, state_desc " +
       "FROM test_states " +
       "WHERE selector = '" + selector + "' " +
       "ORDER BY test_state_id")
result = my_cursor.execute(sql)
if not result:
    print ("Database Error")
    exit(1)
rows = my_cursor.fetchall()
for row in rows:
    print ("\n" + row['test_state_id'] + "  " + row['state_desc'])
    state_string = row['state_string']
    #print(state_string)
    #game_utils.print_state_string(state_string)
    game_state = game_utils.state_string_to_array(state_string)
    #print (game_state)
    game_utils.print_game_state(game_state)

    for panellist_id in my_panel.panellists:
        this_panellist = my_panel.panellists[panellist_id]
        player_id = this_panellist['ID']
        candidate = game_utils.load_instance_from_database(player_id)
        if not candidate:
            print (panellist_id + ' Failed to load')
            continue
        whoami = 0
        proposed = candidate.propose_column(game_state, whoami, 4)
        if hasattr(candidate, 'name'):
            name_string = candidate.name
        else:
            name_string = candidate.id
        print (player_id + ' ' + name_string + ' proposes ' + str(proposed))

my_cursor.close()
conn.close()

