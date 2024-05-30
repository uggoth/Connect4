import  mysql.connector as mariadb

def get_conn():
    conn = mariadb.connect(user='robotuser',
                    passwd='bankalore',
                    host='localhost',
                    db='robotdb',
                    autocommit=True)
    return conn

def get_cursor(conn):
    return conn.cursor(dictionary=True, buffered=True)

def get_next_serial_no(object_type):
    conn = get_conn()
    sql = 'SELECT last_no_used FROM serial_nos WHERE object_type = \'' + object_type + '\''
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is None:
        last_no_used = 0
        last_no_used += 1
        sql = 'INSERT INTO serial_nos (object_type, last_no_used) VALUES (\'' + object_type + '\', ' + str(last_no_used) + ')'
        cursor.execute(sql)
    else:
        last_no_used = row[0]
        last_no_used += 1
        sql = 'UPDATE serial_nos SET last_no_used = ' + str(last_no_used) + ' WHERE object_type = \'' + object_type + '\''
        cursor.execute(sql)
    cursor.close()
    conn.close()
    return last_no_used

def get_next_id(object_type, number_length=8):
    format_code = '{:0' + str(number_length) + '}'
    sno = format_code.format(get_next_serial_no(object_type))
    return object_type + sno

def get_parm(which_parm):
    conn = get_conn()
    local_cursor = conn.cursor()
    sql = ("SELECT parm_value FROM parameters WHERE parm_index = '" + which_parm + "'")
    local_cursor.execute(sql)
    row = local_cursor.fetchone()
    if row:
        return row[0]
    else:
        return False
    local_cursor.close()
    conn.close()
    
def set_parm(which_parm, parm_value):
    conn = get_conn()
    my_cursor = conn.cursor()
    sql = ("SELECT parm_value FROM parameters WHERE parm_index = '" + which_parm + "'")
    my_cursor.execute(sql)
    row = my_cursor.fetchone()
    if row:
        sql = ("UPDATE parameters SET parm_value = '" + parm_value + "' WHERE parm_index = '" + which_parm + "'")
    else:
        sql = ("INSERT INTO parameters (parm_index, parm_value) VALUES ('" + which_parm + "', '" + parm_value + "')")
    my_cursor.execute(sql)
    conn.commit()
    my_cursor.close()
    conn.close()
    return True

def get_parm(which_parm):
    conn = get_conn()
    local_cursor = conn.cursor()
    sql = ("SELECT parm_value FROM parameters WHERE parm_index = '" + which_parm + "'")
    local_cursor.execute(sql)
    row = local_cursor.fetchone()
    if row:
        return row[0]
    else:
        return False
    local_cursor.close()
    conn.close()
    
def set_parm(which_parm, parm_value):
    conn = get_conn()
    my_cursor = conn.cursor()
    sql = ("SELECT parm_value FROM parameters WHERE parm_index = '" + which_parm + "'")
    my_cursor.execute(sql)
    row = my_cursor.fetchone()
    if row:
        sql = ("UPDATE parameters SET parm_value = '" + parm_value + "' WHERE parm_index = '" + which_parm + "'")
    else:
        sql = ("INSERT INTO parameters (parm_index, parm_value) VALUES ('" + which_parm + "', '" + parm_value + "')")
    my_cursor.execute(sql)
    conn.commit()
    my_cursor.close()
    conn.close()
    return True

