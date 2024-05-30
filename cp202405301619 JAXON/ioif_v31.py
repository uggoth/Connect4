# Input Output and Utility Facilities

import time
start_time = time.strftime('%Y %m %d %H:%M:%S')
import logging
logging.basicConfig(filename='/home/pi/aaa_ioif.log',level=logging.INFO)
logging.info('********* ioif starting at ' + start_time)

import pigpio
gpio = pigpio.pi()

import database_utils_v02 as dbu
mysql = dbu.mysql

controllers = {}
controllers['PI_GPIO'] = {}
controllers['PI_GPIO']['INSTANCE'] = gpio
controllers['PI_GPIO']['TYPE'] = 'GPIO'
controllers['PI_GPIO']['PARMS'] = {'INPUT_LOW': 0, 'INPUT_HIGH': 1, 'OUTPUT_LOW': 0, 'OUTPUT_HIGH': 1}
controllers['PI_GPIO']['PINS'] = {18:'D', 23:'D', 24:'D', 25:'D', 12:'D', 16:'D', 20:'D', 21:'D',
                                   4:'D', 17:'D', 27:'D', 22:'D',  5:'D',  6:'D', 13:'D', 19:'D', 26:'D'}

port_types = {}
port_types['IRP'] = {'DESC': 'IR proximity',       'INPUT': True,  'DIGITAL': True,  'PULLUP': 'UP',  'NORMALLY': 'OFF'}
port_types['IRE'] = {'DESC': 'IR edge detect',     'INPUT': True,  'DIGITAL': True,  'PULLUP': 'UP',  'NORMALLY': 'ON'}
port_types['FLD'] = {'DESC': 'Flame Detector',     'INPUT': True,  'DIGITAL': True,  'PULLUP': 'NO',  'NORMALLY': 'ON'}
port_types['SWI'] = {'DESC': 'Mechanical Switch',  'INPUT': True,  'DIGITAL': True,  'PULLUP': 'UP',  'NORMALLY': 'OFF'}
port_types['SWP'] = {'DESC': 'Switch With Pullup', 'INPUT': True,  'DIGITAL': True,  'PULLUP': 'NO',  'NORMALLY': 'OFF'}
port_types['ANA'] = {'DESC': 'Analogue Sensor',    'INPUT': True,  'DIGITAL': False, 'PULLUP': 'NO'}
port_types['REL'] = {'DESC': 'Relay',              'INPUT': False, 'DIGITAL': True,                   'NORMALLY': 'OFF'}
port_types['LED'] = {'DESC': 'LED',                'INPUT': False, 'DIGITAL': True,                   'NORMALLY': 'OFF'}
port_types['SRV'] = {'DESC': 'Servo',              'INPUT': False, 'DIGITAL': False}
port_types['STP'] = {'DESC': 'Stepper Motor',      'INPUT': False, 'DIGITAL': True,                   'NORMALLY': 'OFF'}

port_map = {}
port_map['RAND_HOLD_READ']  = {'NAME': 'Randomiser Hold Read',  'TYPE': 'FIN', 'CONTROLLER': 'PI_GPIO',  'PORT': 22, 'INVERT': True}
port_map['RAND_HOLD_WRITE'] = {'NAME': 'Randomiser Hold Write', 'TYPE': 'FOU', 'CONTROLLER': 'PI_GPIO',  'PORT': 22, 'INVERT': True}

max_switch_name_len = 12

switches = {}
switches['RANDOM_HOLD'] = {}
switches['RANDOM_HOLD']['TYPE'] = 'MYSQL'
switches['VARY_HOLD'] = {}
switches['VARY_HOLD']['TYPE'] = 'MYSQL'
switches['EVOLVE_HOLD'] = {}
switches['EVOLVE_HOLD']['TYPE'] = 'MYSQL'
switches['SHUT_DOWN'] = {}
switches['SHUT_DOWN']['TYPE'] = 'MYSQL'

for switch in switches:
    if len(switch) > max_switch_name_len:
        print ('**ERROR** in ioif switch definitions ' + switch + ' too long. Max is ' + str(max_switch_name_len))

def print_dictionary(my_dict):
    for key in my_dict:
        print (key + ':  ' + str(my_dict[key]))

def get_cpu_temp():
    f = open("/sys/class/thermal/thermal_zone0/temp", "r")
    if f.mode == "r":
        contents = f.readlines()
        for line in contents:
            result = float(line) / 1000.0
        f.close()
        return result
    else:
        return False

def ensure_switch_there(switch_name, cursor, conn):
    sql = "SELECT switch_state FROM switches WHERE switch_name = '" + switch_name + "'"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is None:
        sql = "INSERT INTO switches (switch_name, switch_state) VALUES ('" + switch_name + "', 'OFF')"
        cursor.execute(sql)
        conn.commit()

def set_switch(switch_name, state): # state is by convention 'ON' or 'OFF'
    if switches[switch_name]['TYPE'] == 'MYSQL':
        conn = dbu.get_conn()
        cursor = conn.cursor()
        ensure_switch_there(switch_name, cursor, conn)
        sql = "UPDATE switches SET switch_state = '" + state + "' WHERE switch_name='" + switch_name + "'"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    else:
        return False

def get_switch(switch_name):
    if switches[switch_name]['TYPE'] == 'MYSQL':
        conn = dbu.get_conn()
        cursor = conn.cursor()
        ensure_switch_there(switch_name, cursor, conn)
        sql = "SELECT switch_state FROM switches WHERE switch_name = '" + switch_name + "'"
        cursor.execute(sql)
        row = cursor.fetchone()
        state = row[0]
        conn.commit()
        cursor.close()
        conn.close()
        return state
    else:
        return False

def speak(text):
    result = {"SUCCESS": False}
    # -p is pitch (0 to 99)
    # -a is amplitude (0 to 200)
    # -s is speed (0 to 500)
    # -v is the voice. -ven is English, -ven-sc is Scottish, -ven-sc+f3 is female Scottish
    # -k is the level of emphasis for capitalised words
    command = "espeak -ven+f3 -k5 -s150 -m -p85 -a199 '" + text + "'"
    os.system(command)
    result["SUCCESS"] = True
    return result

def initialise_input_port(interface):
    global port_map, port_types, controllers
    port_config = port_map[interface]
    port_type = port_config['TYPE']
    port_type_config = port_types[port_type]
    is_input = port_type_config['INPUT']
    controller_name = port_config['CONTROLLER']
    controller_config = controllers[controller_name]
    controller_type = controller_config['TYPE']
    if is_input and controller_type == 'GPIO':
        controller_instance = controllers[controller_name]['INSTANCE']
        port = port_config['PORT']
        controller_instance.set_mode(port, pigpio.INPUT)
        if port_type_config['PULLUP'] == 'UP':
            controller_instance.set_pull_up_down(port, pigpio.PUD_UP)
        elif port_type_config['PULLUP'] == 'DOWN':
            controller_instance.set_pull_up_down(port, pigpio.PUD_DOWN)
        else:
            controller_instance.set_pull_up_down(port, pigpio.PUD_OFF)

def initialise_output_port(interface):
    global port_map, port_types, controllers
    port_config = port_map[interface]
    port_type = port_config['TYPE']
    port_type_config = port_types[port_type]
    is_input = port_type_config['INPUT']
    controller_name = port_config['CONTROLLER']
    controller_config = controllers[controller_name]
    controller_type = controller_config['TYPE']
    if controller_type == 'GPIO':
        controller_instance = controllers[controller_name]['INSTANCE']
        port = port_map[interface]['PORT']
        controller_instance.set_mode(port, pigpio.OUTPUT)
        controller_instance.write(port,0)
    if 'SPEED' in port_config:
        sub_result = set_speed(interface, port_config['SPEED'])
    if 'ACCELERATION' in port_config:
        sub_result = set_acceleration(interface, port_config['ACCELERATION'])
    if 'NORMALLY' in port_type_config:
        sub_result = set_state(interface, port_type_config['NORMALLY'])
    return True

def initialise_all_ports():
    global port_map, port_type
    for interface in port_map:
        port_config = port_map[interface]
        this_type = port_config['TYPE']
        type_config = port_types[this_type]
        if type_config['INPUT']:
            initialise_input_port(interface)
        else:
            initialise_output_port(interface)
    return True

def set_value(interface, state):
    global port_map, port_types, controllers
    port_config = port_map[interface]
    port_type = port_config['TYPE']
    port_type_config = port_types[port_type]
    is_input = port_type_config['INPUT']
    if not is_input:
        controller_name = port_config['CONTROLLER']
        controller_config = controllers[controller_name]
        controller_type = controller_config['TYPE']
        if controller_type == 'GPIO':
            controller_instance = controllers[controller_name]['INSTANCE']
            port = port_map[interface]['PORT']
            controller_instance.write(port,state)
        elif controller_type == 'MAESTRO':
            controller_instance = controllers[controller_name]['INSTANCE']
            port = port_map[interface]['PORT']
            controller_instance.setTarget(port, state)

def get_value(interface):
    global port_map, port_type, controllers
    logging.debug('get_value: called for '  + interface)
    result = {}
    result['SUCCESS'] = False
    port_config = port_map[interface]
    port_type = port_config['TYPE']
    port_type_config = port_types[port_type]
    is_input = port_type_config['INPUT']
    if is_input:
        controller_name = port_config['CONTROLLER']
        controller_config = controllers[controller_name]
        controller_type = controller_config['TYPE']
        port = port_config['PORT']
        if controller_type == 'MAESTRO':
            controller_instance = controllers[controller_name]['INSTANCE']
            position = controller_instance.getPosition(port)
            logging.debug('get_value: Returning ' + str(position) + ' for ' + interface)
            result['SUCCESS'] = True
            result['VALUE'] = position
            return result
        elif controller_type == 'GPIO':
            controller_instance = controllers[controller_name]['INSTANCE']
            position = controller_instance.read(port)
            logging.debug('get_value: Returning ' + str(position) + ' for ' + interface)
            result['SUCCESS'] = True
            result['VALUE'] = position
            return result
        else:
            result['SUCCESS'] = False
            return result
    else:
        result['SUCCESS'] = False
        return result

def get_state(interface):
    global port_map, controllers
    result = {}
    result['SUCCESS'] = False
    sub_result = get_value(interface)
    if sub_result['SUCCESS']:
        port_config = port_map[interface]
        controller_name = port_config['CONTROLLER']
        controller_config = controllers[controller_name]
        low = controller_config['PARMS']['INPUT_LOW']
        high = controller_config['PARMS']['INPUT_HIGH']
        position = sub_result['VALUE']
        if position <= low:
            if 'INVERT' in port_config:
                result['STATE'] = 'ON'
            else:
                result['STATE'] = 'OFF'
            result['SUCCESS'] = True
            return result
        elif position >= high:
            if 'INVERT' in port_config:
                result['STATE'] = 'OFF'
            else:
                result['STATE'] = 'ON'
            result['SUCCESS'] = True
            return result
        else:
            result['SUCCESS'] = False
            return result
    else:
        result['SUCCESS'] = False
        return result

def set_state(interface, state):
    global port_map, controllers
    result = {}
    result['SUCCESS'] = False
    port_config = port_map[interface]
    if 'INVERT' in port_config:
        if state == 'ON':
            this_state = 'OFF'
        else:
            this_state = 'ON'
    else:
        this_state = state
    controller_name = port_config['CONTROLLER']
    controller_config = controllers[controller_name]
    if this_state == 'ON':
        high = controller_config['PARMS']['OUTPUT_HIGH']
        set_value(interface, high)
    elif this_state == 'OFF':
        low = controller_config['PARMS']['OUTPUT_LOW']
        set_value(interface, low)

def get_cpu_secs():
    global gpio
    result = float(gpio.get_current_tick()) / 1000000.0
    return result

