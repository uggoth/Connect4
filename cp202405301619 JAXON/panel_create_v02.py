import database_utils_v04 as dbu
mysql = dbu.mariadb
import parameters_v35 as parms

conn = dbu.get_conn()
my_cursor = dbu.get_cursor(conn)

species = parms.species

panel_count = 0
sql = ("SELECT panel_id, panel_desc FROM panels WHERE species = '" + species + "'")
my_cursor.execute(sql)
for row in my_cursor:
    if panel_count == 0:
        print ("List of panels before creation:")
    print (row['panel_id'] + '  ' + row['panel_desc'])
    panel_count += 1
if panel_count < 1:
    print ('No existing panels for species ' + species)

panel_desc = input("Enter new panel description: ")
survival_score = input("Enter survival score required: ")
panel_id = dbu.get_next_id('PANL')
lowest_acceptable_score = input("Enter lowest acceptable score required: ")

sql = ("INSERT INTO panels (panel_id, panel_desc, species, survival_score, lowest_acceptable_score) VALUES ('" +
       panel_id + "', '" + panel_desc + "','" + species + "'," + str(survival_score) + ", " + str(lowest_acceptable_score) + ")")
my_cursor.execute(sql)

sql = ("SELECT panel_id, panel_desc FROM panels WHERE species = '" + species + "'")
my_cursor.execute(sql)
panel_count = 0
for row in my_cursor:
    if panel_count == 0:
        print ("List of panels after creation:")
    print (row['panel_id'] + '  ' + row['panel_desc'])
    panel_count += 1
if panel_count < 1:
    print ('No existing panels for species ' + species)
