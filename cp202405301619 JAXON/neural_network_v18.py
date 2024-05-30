# Neural networks for robots

from scipy.special import expit
import random
import game_utils_v05 as game_utils
dbu = game_utils.dbu
mysql = game_utils.mysql
parms = game_utils.parms
pickle = game_utils.pickle
copy = game_utils.copy
import player_v02 as player

class Network(player.Player):
    'Base class for neural networks'
    def __init__(self, net_id, standard_method, thresholds, species):
        # Note that for convenience many of these properties are also saved in the
        # nets or child_nets tables, but the definitive versions are those here
        self.id = net_id
        self.name = net_id
        self.parent_id = ''
        self.genealogy = ''
        self.type = 'NETWORK'
        self.game_state = None
        self.whoami = None
        self.winning_run = None
        self.debug_level = 0
        self.proposed_column = 0
        self.decisive_neuron_name = ''
        self.species = species
        self.layer_list = []
        self.sense_layer = None
        self.act_layer = None
        self.standard_method = standard_method
        self.thresholds = thresholds    # True or False
        self.score = 0
        self.wins = 0
        self.games = 0
        self.panel_id = ''
        self.filename = ''
        self.logic_count = 0
        self.memory_count = 0
        self.evolves = 0

    def __str__(self):
        lenfs = len(self.layer_list)
        return ('Network ' + self.id + ' of ' + str(lenfs) + ' layers. Score: ' + str(self.score))

    def str_explode(self, levels=1):
        return_string = ''
        padding = '   '
        if levels > 0:
            return_string += str(self)
        if levels > 1:
            for layer in self.layer_list:
                return_string += ("\n" + padding + str(layer))
                if levels > 2:
                    for neuron in layer.neuron_list:
                        return_string += ("\n" + padding + padding + str(neuron))
                        if levels > 3:
                            for synapse in neuron.synapse_list:
                                return_string += ("\n"  + padding + padding + padding+ str(synapse))
        return (return_string)

    def cycle(self):
        last_neuron = None
        lenfs = len(self.layer_list)
        for i in range(lenfs):
            this_layer = self.layer_list[i]
            last_neuron = this_layer.cycle()
        if last_neuron == None:
            return 0
        else:
            self.decisive_neuron_name = last_neuron.name
            return last_neuron.column

    def print_game_state(self, game_state):
        no_cols = len(game_state)
        no_rows = len(game_state[0])
        for y in range(no_rows - 1, -1, -1):
            s = ''
            for x in range(no_cols):
                s = s + ' ' + str(game_state[x][y])
            print (str(y+1) + ": " + s)

    def propose_column(self, game_state, whoami, winning_run):  # principal interface
                        # game_state is 7x6 array, whoami is 0 or 1, winning_run is 4
        instinctive_column = game_utils.opportunity_of_4(game_state, whoami+1)
        if instinctive_column:
            return instinctive_column
        self.game_state = game_state
        self.no_columns = len(game_state)
        self.no_rows = len(game_state[0])
        top_row = self.no_rows - 1
        self.whoami = whoami
        self.winning_run = winning_run
        self.proposed_column = self.cycle()
        if game_state[self.proposed_column-1][top_row] == 0:   # can play there
            return self.proposed_column
        else:   # find any playable column
            for self.proposed_column in [4,5,3,6,2,7,1]:
                if game_state[self.proposed_column-1][top_row] == 0:   # can play there
                    return self.proposed_column
        print ("*** NETWORK "+ self.id + " FAILED TOO PROPOSE COLUMN ***")
        self.print_game_state(game_state)
        return 0
            

    def whats_in(self, column, row):    # returns 0,1,2
        x = column - 1
        y = row - 1
        return self.game_state[x][y]

    def generate_filename(self, folder=''):
        if folder == '':
            save_folder = player.Player.save_folder
        else:
            save_folder = folder
        filename = (save_folder + '/' + self.species + '_' +
                       'S' + '{:04}'.format(self.score) + '_' +
                       self.id + '_' +
                       self.standard_method + 
                       '.pkl')
        return filename

    def save_self_to_database(self, table='nets', session_id=''):
        conn = dbu.get_conn()
        my_cursor = conn.cursor()
        if self.thresholds:
            tss = '1'
        else:
            tss = '0'
        blob = pickle.dumps(self, pickle.HIGHEST_PROTOCOL)
        if table == 'child_nets':
            session_clause = "session, "
            session_value = "'" + session_id + "', "
        else:
            session_clause = ''
            session_value = ''
        if hasattr(self, 'genealogy'):
            genealogy_clause = "genealogy, "
            genealogy_value = "'" + self.genealogy + "', "
        else:
            genealogy_clause = ''
            genealogy_value = ''
        sql = ("INSERT INTO " + table + " (net_id, panel_id, score, wins, games, evolves, " +
               session_clause +
               genealogy_clause +
               "method, logic_count, memory_count, thresholds, species, instance) VALUES (" +
               "'" + self.id + "', " +
               "'" + self.panel_id + "', " +
               str(self.score) + ", " +
               str(self.wins) + ", " +
               str(self.games) + ", " +
               "0, " +
               session_value +
               genealogy_value +
               "'" + self.standard_method + "', " +
               str(self.logic_count) + ", " +
               str(self.memory_count) + ", " +
               tss  + ", " +
               "'" + self.species + "', " +
               "%s) " +
               " ON DUPLICATE KEY UPDATE " +
               "score=" + str(self.score) + ", " +
               "wins=" + str(self.wins) + ", " +
               "games=" + str(self.games) + ", " +
               "panel_id='" + self.panel_id + "', " +
               "evolves=" + str(self.evolves) + ", " +
               "filename='" + self.filename + "', " +
               "timestamp=NOW();")
        my_cursor.execute(sql, (blob, ))
        conn.commit()
        my_cursor.close()
        conn.close()

    def export_self_to_file(self, folder='nets'):
        filename = self.generate_filename(folder)
        self.filename = filename
        with open(filename,'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        conn = dbu.get_conn()
        my_cursor = conn.cursor()
        sql = ("UPDATE nets SET filename = '" + filename + "' WHERE net_id = '" + self.id + "'")
        my_cursor.execute(sql)
        conn.commit()
        my_cursor.close()
        conn.close()

#-----------------------------------------------------------------------

class Layer:
    'Layers of neurons. Can be input, logic, or output. If not input have synapses'
    def __init__(self, name, network, level):
        self.name = name
        self.network = network
        self.level = level
        self.neuron_list = []
        self.neuron_directory = {}
        self.layer_index = len(network.layer_list)
        network.layer_list.append(self)

    def __str__(self):
        return ('Layer ' + self.name +
                ' type ' + self.level +
                ' of network ' + self.network.name +
                ' has ' + str(len(self.neuron_list)) + ' neurons')

    def randomise_thresholds(self, low, high):
        for neuron in self.neuron_list:
            neuron.threshold = random.uniform(low, high)

    def cycle(self, game_state, whoami, winning_run):
        print ('**ERROR**') # MUST OVERRIDE

        
class Input_Layer(Layer):
    def __init__(self, name, network):
        Layer.__init__(self, name, network, 'INPUT')
        network.sense_layer = self
    def cycle(self):
        self.network.inputs = ''
        for neuron in self.neuron_list:
            neuron.cycle()
            if neuron.fired:
                self.network.inputs += (neuron.name + ' ON ')
    
class Non_Input_Layer(Layer):
    
    def __init__(self, name, network):
        Layer.__init__(self, name, network, 'NON_INPUT')
        self.synapse_list = []

    def link_back(self):
        standard_weight = 0.5
        previous_layer = self.network.layer_list[self.layer_index - 1]
        #print ('Linking back from ' + self.name + ' to ' + previous_layer.name)
        for in_neuron in previous_layer.neuron_list:
            #print ('Linking from ' + in_neuron.name)
            for out_neuron in self.neuron_list:
                syn = Synapse(self, in_neuron, out_neuron, standard_weight)
                #print (syn)
        
    def randomise_weights(self, low, high):
        for synapse in self.synapse_list:
            synapse.weight = random.uniform(low, high)

    def cycle(self):
        for neuron in self.neuron_list:
            neuron.input = 0
        for synapse in self.synapse_list:
            synapse.cycle()
        for neuron in self.neuron_list:
            neuron.cycle()

class Logic_Layer(Non_Input_Layer):

    def __init__(self, name, network):
        Non_Input_Layer.__init__(self, name, network)
        self.level = 'LOGIC'

    def populate(self, logic_count, memory_count, method):  # no. of logic and memory neurons to create
        standard_threshold = 0.5
        standard_memory = 0.5
        for i in range(logic_count):
            lname = 'l' + str(i)
            Logic_Neuron(lname, self, standard_threshold, method)
        for i in range(memory_count):
            lname = 'm' + str(i)
            Memory_Neuron(lname, self, standard_threshold, method, standard_memory)

class Output_Layer(Non_Input_Layer):
    
    def __init__(self, name, network):
        Non_Input_Layer.__init__(self, name, network)
        self.level = 'OUTPUT'
        network.act_layer = self

    def cycle(self):    # NB only does ONE thing
        for neuron in self.neuron_list:
            neuron.input = 0
        for synapse in self.synapse_list:
            synapse.cycle()
        strongest_output = 0
        strongest_neuron = None
        for neuron in self.neuron_list:
            neuron.cycle()
            if neuron.fired:
                if neuron.output > strongest_output:
                    strongest_neuron = neuron
                    strongest_output = neuron.output
        if self.network.debug_level > 1:
            print ('Strongest neuron ' + strongest_neuron.name +
                   ' output ' + str(strongest_neuron.output))
        return strongest_neuron


#----------------------------------------------------------------------

class Neuron:
    'Common base class for all types of neuron'

    def __init__(self, name, layer, threshold, method):
        self.name = name
        self.layer = layer
        self.input = 0
        self.threshold = threshold
        self.fired = False
        self.object_class = 'CLASS'
        self.method = method
        self.synapse_list = []
        layer.neuron_list.append(self)
        layer.neuron_directory[name] = self

    def __str__(self):
        return (self.object_class + ' neuron ' + self.name +
               ', output ' + str(self.output) +
               ' of layer ' + self.layer.name)

    def cycle(self): # Must override
        print ('**ERROR**')

class Logic_Neuron (Neuron):
    'Internal logical analysis'

    def __init__(self, name, layer, threshold, method):
        Neuron.__init__(self, name, layer, threshold, method)
        self.object_class = 'LOGIC'
        self.input = 0
        self.output = 0

    def __str__(self):
        if hasattr(self, 'method'):
            method_string = ", method: " + self.method
        else:
            method_string = ''
        smallest = 0.001

        if self.threshold < smallest:
            my_threshold = 0.0
        else:
            my_threshold = self.threshold

        if self.input < smallest:
            my_input = 0.0
        else:
            my_input = self.input

        if self.output < smallest:
            my_output = 0.0
        else:
            my_output = self.output
        return ('Logic Neuron ' + "{:>3},".format(self.name) + 
               ' threshold ' + "{:8.2f}".format(my_threshold) + 
               ', inputs ' + "{:8.2f}".format(my_input) + 
               ', output ' + "{:8.2f}".format(my_output) +
                method_string)
        

    def cycle(self):
        if ((self.input > self.threshold) or (not self.layer.network.thresholds)):
            self.fired = True
            if self.method == 'DIGITAL':
                self.output = 1
            elif self.method == 'SIGMOIDAL':
                self.output = expit(self.input)
            else:
                self.output = self.input
            #print (self.name + ' output ' + str(self.output))
        else:
            self.fired = False
            self.output = 0

class Memory_Neuron(Logic_Neuron):
    
    def __init__(self, name, layer, threshold, method, memory_factor):
        Logic_Neuron.__init__(self, name, layer, threshold, method)
        self.object_class = 'MEMORY'
        self.memory_factor = memory_factor
        self.previous_input = threshold
        
    def cycle(self):
        corrected_input = self.previous_input + (
            (self.input - self.previous_input) * (1.0 - self.memory_factor))
        if ((corrected_input > self.threshold) or (not self.layer.network.thresholds)):
            self.fired = True
            if self.method == 'DIGITAL':
                self.output = 1
            elif self.method == 'SIGMOIDAL':
                self.output = expit(self.input)
            else:
                self.output = self.input
        else:
            self.fired = False
            self.output = 0
        self.previous_input = corrected_input


class Connect_4_Motor_Neuron(Neuron):
    'Interacts with the outside world'
    def __init__(self, name, layer, threshold, method):
        Neuron.__init__(self, name, layer, threshold, method)
        self.object_class = 'MOTOR'
        self.input = 0
        self.output = 0
        self.column = 0

    def __str__(self):
        smallest = 0.001

        if self.threshold < smallest:
            my_threshold = 0.0
        else:
            my_threshold = self.threshold

        if self.input < smallest:
            my_input = 0.0
        else:
            my_input = self.input

        if self.output < smallest:
            my_output = 0.0
        else:
            my_output = self.output
        return ('Motor Neuron ' + self.name + 
               ' threshold ' + "{:8.2f}".format(my_threshold) + 
               ', inputs ' + "{:8.2f}".format(my_input) + 
               ', output ' + "{:8.2f}".format(my_output))

    def cycle(self):
        self.fired = False
        self.output = 0
        if self.input > self.threshold:     # check to see if column is playable
            if self.layer.network.whats_in(self.column, self.layer.network.no_rows) == 0:
                self.output = self.input
                self.fired = True

class Connect_4_Sensor_Neuron(Neuron):
    'Responds to one exact stimulus. Behaviour depends on type'
    def __init__(self, name, layer, column, row):
        Neuron.__init__(self, name, layer, 0, 'DIGITAL')
        self.object_class = 'SENSOR'
        self.type = 'SINGLE' # default, usually overriden
        self.column = column
        self.row = row
        self.output = 0

    def __str__(self):
        return_string = "Sensor Neuron: " + "{:>22}".format(self.name)
        if hasattr(self, 'sense_function'):
            return_string += ",  Function: " + str(self.sense_function)
        return_string += ",  Output " + "{:3}".format(self.output)
        return (return_string)

    def find_free_row(self):
        x = self.column - 1
        for y in range(self.no_rows):
            if self.game_state[x][y] == 0:
                return y+1
        return 0

    def find_consecutives(self, player, row, column):     # returns the number of consecutive counters of player colour if
                                            # player plays in row, column
        play_x = column - 1
        play_y = row - 1
        play_state = player + 1
        best_run = 0

        # East West
        consecutive = 1 # number of counters in line; starting with the counter to be played
        for check_x in range(play_x + 1, self.no_columns):
            if self.game_state[check_x][play_y] == play_state:
                consecutive += 1
            else:
                break
        for check_x in range(play_x - 1, -1, -1):
            if self.game_state[check_x][play_y] == play_state:
                consecutive += 1
            else:
                break
        if consecutive > best_run:
            best_run = consecutive

        # North South
        consecutive = 1
        for check_y in range(play_y + 1, self.no_rows):
            if self.game_state[play_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        for check_y in range(play_y - 1, -1, -1):
            if self.game_state[play_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        if consecutive > best_run:
            best_run = consecutive

        # NorthEast SouthWest
        consecutive = 1
        check_x = play_x
        for check_y in range(play_y + 1, self.no_rows):
            check_x += 1
            if check_x >= self.no_columns:
                break
            if self.game_state[check_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        check_x = play_x
        for check_y in range(play_y - 1, -1, -1):
            check_x -= 1
            if check_x < 0:
                break
            if self.game_state[check_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        if consecutive > best_run:
            best_run = consecutive
            
        # NorthWest SouthEast
        consecutive = 1 # the counter just played
        check_x = play_x
        for check_y in range(play_y + 1, self.no_rows):
            check_x -= 1
            if check_x < 0:
                break
            if self.game_state[check_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        check_x = play_x
        for check_y in range(play_y - 1, -1, -1):
            check_x += 1
            if check_x >= self.no_columns:
                break
            if self.game_state[check_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        if consecutive > best_run:
            best_run = consecutive

        return best_run

    def cycle(self):
        self.fired = False
        self.output = 0
        self.stimulus = 0
        self.game_state = self.layer.network.game_state
        self.no_columns = len(self.game_state)
        self.no_rows = len(self.game_state[0])
        self.whoami = self.layer.network.whoami
        self.whohe = 1 - self.whoami
        free_row = self.find_free_row()
        if self.type == 'MY_CONSECUTIVES_2':
            if free_row > 0:
                my_score = self.find_consecutives(player=self.whoami, row=free_row, column=self.column)
                self.fired = True
                self.output = my_score * my_score
                return self.fired
            else:
                self.fired = False
                self.output = 0
                return self.fired
        elif self.type == 'HIS_CONSECUTIVES_2':
            if free_row > 0:
                my_score = self.find_consecutives(player=self.whohe, row=free_row, column=self.column)
                self.fired = True
                self.output = my_score * my_score
                return self.fired
            else:
                self.fired = False
                self.output = 0
                return self.fired
        elif self.type == 'MY_CONSECUTIVES':
            if free_row > 0:
                my_score = self.find_consecutives(player=self.whoami, row=free_row, column=self.column)
                self.fired = True
                self.output = my_score
                return self.fired
            else:
                self.fired = False
                self.output = 0
                return self.fired
        elif self.type == 'HIS_CONSECUTIVES':
            if free_row > 0:
                my_score = self.find_consecutives(player=self.whohe, row=free_row, column=self.column)
                self.fired = True
                self.output = my_score
                return self.fired
            else:
                self.fired = False
                self.output = 0
                return self.fired
        elif self.type == 'COLUMN':
            if self.layer.network.whats_in(self.column, 1) == 0: # column is empty. don't need to look further
                if self.stimulus  == 0:
                    self.fired = True
                    self.output = 1
                    return self.fired
                else:
                    self.fired = False
                    self.output = 0
                    return self.fired
            consecutives = 0
            for j in range(self.no_rows,0,-1):
                content = self.layer.network.whats_in(self.column, j)
                if content == self.stimulus:
                    consecutives += 1
                else:
                    consecutives = 0
            if consecutives == 0:
                self.fired = False
                self.output = 0
                return self.fired
            else:
                self.fired = True
                self.output = consecutives * consecutives
                return self.fired
        elif self.type == 'ROW':
            best_consecutives = 0
            consecutives = 0
            for i in range(columns):
                content = whats_in(i+1, self.row)
                if content == self.stimulus:
                    consecutives += 1
                else:
                    consecutives = 0
                if consecutives > best_consecutives:
                    best_consecutives = consecutives
            if best_consecutives == 0:
                self.fired = False
                self.output = 0
                return self.fired
            else:
                self.fired = True
                self.output = best_consecutives * best_consecutives
                return self.fired
        elif self.type == 'SINGLE':
            if whats_in(self.column, self.row) == self.stimulus:
                self.fired = True
                self.output = 1
            else:
                self.fired = False
                self.output = 0
        else:
            self.fired = False
            self.output = 0
            return self.fired

#--------------------------------------------------------------------------

class Synapse:
    'Common base class for all types of synapse'

    def __init__(self, layer, in_neuron, out_neuron, weight, special=False):
        self.in_neuron = in_neuron
        self.out_neuron = out_neuron
        self.name = in_neuron.name + ':' + out_neuron.name
        self.weight = weight
        self.special = special
        self.output = 0
        layer.synapse_list.append(self)
        out_neuron.synapse_list.append(self)

    def __str__(self):
        return ('synapse ' + self.name +
               ', weight: ' + "{:8.2f}".format(self.weight) + 
               ', output: ' + "{:8.2f}".format(self.output))

    def cycle(self):
        nin = self.in_neuron
        self.output = nin.output * self.weight
        nout = self.out_neuron
        before = nout.input
        nout.input = nout.input + self.output
        after = nout.input
        if self.special:
            if self.output != 0:
                print (self.name + ' setting output neuron ' + nout.name +
                       ' from ' + str(before) + ' to ' + str(after))
