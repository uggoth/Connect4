import game_utils_v05 as game_utils
dbu = game_utils.dbu
mysql = game_utils.mysql
print ('MariaDB Version:', mysql.__version__)
parms = game_utils.parms
pickle = game_utils.pickle
copy = game_utils.copy

conn = dbu.get_conn()
conn.commit()
cursor = conn.cursor(dictionary=True)

sql = ("SELECT test_state_id, state_string, state_desc " +
       "FROM test_states " +
       "WHERE selector = 'A' " +
       "ORDER BY test_state_id")
cursor.execute(sql)
rows = cursor.fetchall()
for row in rows:
    print (row['test_state_id'] + "  " + row['state_desc'])

test_state_id = input("Enter test state ID: ")
sub_result = game_utils.get_test_state(test_state_id)
if not sub_result['SUCCESS']:
    print ("** FAILED TO RETRIEVE TEST STATE **")
    exit(1)
conn.commit()

test_state = game_utils.state_string_to_array(sub_result['STATE_STRING'])
game_utils.print_game_state(test_state)

all_slices = game_utils.concatenate_all_slices(test_state)
print (all_slices)
