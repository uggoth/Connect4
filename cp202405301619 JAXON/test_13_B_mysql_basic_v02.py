import database_utils_v03 as database_utils
mariadb = database_utils.mariadb
print ('MariaDB Version:', mariadb.__version__)
import sys
from pprint import pprint

conn = database_utils.get_conn()

if conn is None:
    print("Error connecting to MariaDB Platform")
    sys.exit(1)
    
object_type = 'TEST'

print ('\nget_next_serial_no()')
for i in range(3):
    n = database_utils.get_next_serial_no(object_type)
    print (object_type, n)

print ('\nget_next_id()')
for i in range(3):
    m = database_utils.get_next_id(object_type)
    print (m)

conn.close()
