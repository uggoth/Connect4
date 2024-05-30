# deletes orphaned children

import game_utils_v04 as game_utils
dbu = game_utils.dbu
mysql = game_utils.mysql
parms = game_utils.parms
pickle = game_utils.pickle
copy = game_utils.copy

conn = dbu.get_dict_conn()
my_cursor = conn.cursor()
out_cursor = conn.cursor()

sql = ("SELECT pl.panellist_id, pl.panel_id AS child, p.panel_id as parent FROM " +
       "panellists pl LEFT OUTER JOIN panels p ON pl.panel_id = p.panel_id")
result = my_cursor.execute(sql)
if not result:
    print ("Bad SQL " + sql)
    exit(1)
orphan_count = 0
rows = my_cursor.fetchall()
for row in rows:
    panellist_id = row['panellist_id']
    parent_panel_id = row['parent']
    child_panel_id = row['child']
    if parent_panel_id != child_panel_id:
        print ("Deleting orphan " + panellist_id)
        orphan_count+= 1
        sql = ("DELETE FROM panellists WHERE panellist_id='" + panellist_id + "'")
        out_cursor.execute(sql)

if orphan_count > 0:
    print (str(orphan_count) + " orphans deleted")
    conn.commit()
else:
    print ("No orphans found")

print ("\nFinished")

my_cursor.close()
out_cursor.close()
conn.close()
