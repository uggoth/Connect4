import pickle
import player_v02 as player
import game_utils_v05 as game_utils
dbu = game_utils.dbu
mysql = game_utils.mysql
parms = game_utils.parms
pickle = game_utils.pickle
copy = game_utils.copy

class RobotPlayer(player.Player):

    def __init__(self, name, desc, level):
        self.default = 7
        self.robot_name = name
        self.name = name
        self.robot_desc = desc
        self.level = level
        self.id = dbu.get_next_id('RBOT', 8)
        self.score = 0  # set by the tester
        self.species = parms.species

    def __str__(self):
        self_string = ('Connect 4 Robot ' + self.robot_name +
                       ' ID ' + self.id +
                       ' level ' + self.level +
                       ' ' + self.robot_desc)
        return self_string

    def propose_column(self, game_state, whoami, winning_run):
        # Must override or extend
        player.Player.propose_column(self, game_state, whoami, winning_run)

    def export_self_to_file(self):
        folder = player.Player.save_folder
        filename = (folder + '/' + self.id + '.pkl')
        with open(filename,'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def save_self_to_database(self):
        conn = dbu.get_conn()
        my_cursor = conn.cursor()
        blob = pickle.dumps(self, pickle.HIGHEST_PROTOCOL)
        score = self.score
        sql = ('INSERT INTO robots (' +
               'robot_id, ' +
               'robot_name, ' +
               'robot_level, ' +
               'robot_score, ' +
               'species, ' +
               'robot_instance, ' +
               'robot_desc)' +
               ' VALUES (\'' + self.id + '\', '+
               '\'' + self.robot_name + '\', ' +
               '\'' + self.level + '\', ' +
               '\'' + str(score) + '\', ' +
               '\'' + self.species + '\', ' +
               '%s, ' +
               '\'' + self.robot_desc +  '\')')
        try:
            my_cursor.execute(sql, (blob, ))
            conn.commit()
        except mysql.IntegrityError:
            print ('Failed to insert record')
        finally:
            my_cursor.close()
            conn.close()


#################################################################

class RobotPlayerA(RobotPlayer):

    def __init__(self):
        name = 'Archie'
        desc = 'Plays preferred'
        level = 'A'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        best_column = game_utils.find_preferred(game_state)
        #print best_column
        if best_column > 0:
            return best_column
        no_columns = len(game_state)
        no_rows = len(game_state[0])
        for column in range(no_columns):
            if game_state[column-1][no_rows-1] == 0:
                return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')

        return 0

class RobotPlayerB(RobotPlayer):

    def __init__(self):
        name = 'Billy'
        desc = 'Plays to win, or preferred'
        level = 'B'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        # returns column to play in, or 0 if can't cope
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        opponent = 2 - whoami

        best_column = game_utils.find_4(game_state, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_preferred(game_state)
        if best_column > 0:
            return best_column
        no_columns = len(game_state)
        no_rows = len(game_state[0])
        for column in range(no_columns):
            if game_state[column-1][no_rows-1] == 0:
                return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')

        return 0

class RobotPlayerC(RobotPlayer):

    def __init__(self):
        name = 'Connor'
        desc = 'Plays win, block'
        level = 'C'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        opponent = 2 - whoami

        best_column = game_utils.find_4(game_state, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_4(game_state, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_preferred(game_state)
        if best_column > 0:
            return best_column

        no_columns = len(game_state)
        no_rows = len(game_state[0])
        for column in range(no_columns):
            if game_state[column-1][no_rows-1] == 0:
                return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')

        return 0

class RobotPlayerD(RobotPlayer):
    # Base robot for copying and modification
    def __init__(self):
        name = 'David'
        desc = 'Plays win, block, my triples'
        level = 'D'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        opponent = 2 - whoami

        best_column = game_utils.find_4(game_state, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_4(game_state, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_3(game_state, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_preferred(game_state)
        if best_column > 0:
            return best_column

        no_columns = len(game_state)
        no_rows = len(game_state[0])
        for column in range(no_columns):
            if game_state[column-1][no_rows-1] == 0:
                return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')

        return 0

class RobotPlayerE(RobotPlayer):

    def __init__(self):
        name = 'Eccles'
        desc = 'Plays win, block, open triples'
        level = 'E'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        opponent = 2 - whoami

        best_column = game_utils.find_4(game_state, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_4(game_state, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_3(game_state, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_3(game_state, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_preferred(game_state)
        if best_column > 0:
            return best_column

        no_columns = len(game_state)
        no_rows = len(game_state[0])
        for column in range(no_columns):
            if game_state[column-1][no_rows-1] == 0:
                return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')

        return 0

class RobotPlayerF(RobotPlayer):

    def __init__(self):
        name = 'Fred'
        desc = 'Plays win, block, triples a and b'
        level = 'F'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        opponent = 2 - whoami

        angle_array = game_utils.make_angle_array(game_state)

        best_column = game_utils.new_find_4(angle_array, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_4(angle_array, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3a(angle_array, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3a(angle_array, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3b(angle_array, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3b(angle_array, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_preferred(game_state)
        if best_column > 0:
            return best_column

        no_columns = len(game_state)
        no_rows = len(game_state[0])
        for column in range(no_columns):
            if game_state[column-1][no_rows-1] == 0:
                return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')

        return 0
        
class RobotPlayerG(RobotPlayer):

    def __init__(self):
        name = 'George'
        desc = 'Plays win, block, triples a, b, and c'
        level = 'G'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        opponent = 2 - whoami

        angle_array = game_utils.make_angle_array(game_state)

        best_column = game_utils.new_find_4(angle_array, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_4(angle_array, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3a(angle_array, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3a(angle_array, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3b(angle_array, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3b(angle_array, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3c(angle_array, player)
        if best_column > 0:
            return best_column

        best_column = game_utils.new_find_3c(angle_array, opponent)
        if best_column > 0:
            return best_column

        best_column = game_utils.find_preferred(game_state)
        if best_column > 0:
            return best_column

        no_columns = len(game_state)
        no_rows = len(game_state[0])
        for column in range(no_columns):
            if game_state[column-1][no_rows-1] == 0:
                return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')

        return 0
        
class RobotPlayerH(RobotPlayer):

    def __init__(self):
        name = 'Henry'
        desc = 'Plays win, block, preferred'
        level = 'H'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        opponent = 3 - player

        winning_column = game_utils.opportunity_of_4(game_state, player)
        if winning_column:
            #print (self.id + " reckons wins in " + str(winning_column))
            return winning_column

        losing_columns = game_utils.threat_of_4(game_state, player)
        if losing_columns:
            #print (self.id + " reckons losing columns are " + str(losing_columns))
            best_column = game_utils.new_find_preferred (game_state, losing_columns)
        else:
            best_column = game_utils.new_find_preferred (game_state)

        if best_column > 0:
            return best_column
        else:
            best_column = game_utils.new_find_preferred (game_state)
            return best_column

        if best_column < 1:
            no_columns = len(game_state)
            no_rows = len(game_state[0])
            for column in range(no_columns):
                if game_state[column-1][no_rows-1] == 0:
                    return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')
        return 0

class RobotPlayerI(RobotPlayer):

    def __init__(self):
        name = 'Isaac'
        desc = 'Plays win, block, preferred'
        level = 'I'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        opponent = 3 - player

        winning_column = game_utils.opportunity_of_4(game_state, player)
        if winning_column:
            #print (self.id + " reckons wins in " + str(winning_column))
            return winning_column

        losing_columns = game_utils.threat_of_4(game_state, player)
        if losing_columns:
            #print (self.id + " reckons losing columns are " + str(losing_columns))
            best_column = game_utils.new_find_preferred (game_state, losing_columns)
            return best_column

        best_column = game_utils.opportunity_of_3(game_state, player)
        if best_column:
            return best_column

        best_column = game_utils.new_find_preferred (game_state)
        if best_column:
            return best_column

        if best_column < 1:
            no_columns = len(game_state)
            no_rows = len(game_state[0])
            for column in [4,3,5,2,6,1,7]:
                if game_state[column-1][no_rows-1] == 0:
                    return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')
        return 0

class RobotPlayerJ(RobotPlayer):

    def __init__(self):
        name = 'Jemima'
        desc = 'Plays win, block, preferred'
        level = 'J'
        RobotPlayer.__init__(self, name, desc, level)

    def propose_column(self, game_state, whoami, winning_run):
        RobotPlayer.propose_column(self, game_state, whoami, winning_run)
        player = whoami + 1
        opponent = 3 - player

        winning_column = game_utils.opportunity_of_4(game_state, player)
        if winning_column:
            #print (self.id + " reckons wins in " + str(winning_column))
            return winning_column

        losing_columns = game_utils.threat_of_4(game_state, player)
        if losing_columns:
            #print (self.id + " reckons losing columns are " + str(losing_columns))
            best_column = game_utils.new_find_preferred (game_state, losing_columns)
            return best_column

        best_column = game_utils.opportunity_of_3(game_state, player)
        if best_column:
            return best_column

        best_column = game_utils.opportunity_of_2(game_state, player)
        if best_column:
            return best_column

        best_column = game_utils.new_find_preferred (game_state)
        if best_column:
            return best_column

        if best_column < 1:
            no_columns = len(game_state)
            no_rows = len(game_state[0])
            for column in [4,3,5,2,6,1,7]:
                if game_state[column-1][no_rows-1] == 0:
                    return column

        print ("*** " + self.id + " FAILED TO PROPOSE COLUMN *** GAME STATE IS ...")
        game_utils.print_game_state(game_state)
        print (' ')
        return 0


