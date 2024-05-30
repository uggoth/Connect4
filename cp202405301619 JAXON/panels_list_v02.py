import database_utils_v02 as dbu
import parameters_v34 as parms

conn = dbu.get_dict_conn()
my_cursor = conn.cursor()

print ("Panels available in " + parms.species)

sql = ("SELECT l.panel_id, l.panellist_id, p.panel_desc, l.player_id, l.score, l.player_name " +
       "FROM panels p JOIN panellists l ON p.panel_id = l.panel_id " +
       "WHERE p.species = '" + parms.species + "'" +
       "ORDER BY score DESC")
result = my_cursor.execute(sql)
if result:
    rows = my_cursor.fetchall()
    current_panel = ''
    for row in rows:
        panel_id = row['panel_id']
        if panel_id != current_panel:
            print (' ')
            print (panel_id + ' - ' + row['panel_desc'])
            current_panel = panel_id
        print ("  " + row['player_id'] + "  {:14}".format(row['player_name']) + "  {:3}".format(row['score']))
        
else:
    print ("** DATABASE ERROR **")
