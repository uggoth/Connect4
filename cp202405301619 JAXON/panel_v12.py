import game_utils_v05 as game_utils
dbu = game_utils.dbu
mysql = dbu.mariadb
pickle = game_utils.pickle
parms = game_utils.parms
copy = game_utils.copy
import player_v02 as player
import game_v09 as c4game

def reset_panellist_scores(panel_id):
    game_id = id_generator.get_next_id('GAME',8)
    game = c4game.Connect4Game(no_columns=parms.game_columns,
                            no_rows=parms.game_rows,
                            name=game_id,
                            winning_run=4)
    my_panel = Panel(panel_id)
    my_panel.link(game)
    local_conn = dbu.get_conn()
    local_cursor = local_conn.cursor()
    for panellist_id in my_panel.panellists:
        candidate = my_panel.panellists[panellist_id]['INSTANCE']
        result = my_panel.do_tests(candidate)
        if result and result['SUCCESS']:
            score = result['SCORE']
            sql = ("UPDATE panellists SET score = " + str(score) +
                   " WHERE panellist_id = '" + panellist_id + "'")
            local_cursor.execute(sql)
        else:
            print (panellist_id + ' ** TEST ERROR **')
    local_conn.commit()
    local_cursor.close()
    local_conn.close()

def print_panel_data(panel_id):
    print (' ')
    conn = dbu.get_conn()
    my_cursor = conn.cursor()
    sql = ("SELECT panel_desc, survival_score FROM panels WHERE panel_id = '" + panel_id + "'")
    my_cursor.execute(sql)
    row = my_cursor.fetchone()
    if row:
        print (panel_id + ' ' + row[0] + ' Survival score:' + str(row[1]))
        sql2 = ("SELECT panellist_id, player_id, score FROM panellists WHERE panel_id = '" + panel_id + "' ORDER BY panellist_id")
        my_cursor.execute(sql2)
        rows2 = my_cursor.fetchall()
        if rows2:
            for row2 in rows2:
                print ("  " + row2[0] + "  " + row2[1] + "  " + str(row2[2]))
        else:
            print ("**ERROR** Failed to retrieve panellists")
    else:
        print ("**ERROR** Failed to retrieve " + panel_id)
    print (' ')
    my_cursor.close()
    conn.close()

def get_panellist_info(panel_id):
    local_conn = dbu.get_conn()
    local_cursor = local_conn.cursor()
    sql = ("SELECT panellist_id, player_id, score FROM panellists WHERE panel_id = '" + panel_id + "' ORDER BY acceded")
    local_cursor.execute(sql)
    rows = local_cursor.fetchall()
    if rows:
        result = {}
        worst_score = 9999
        best_score = -9999
        for row in rows:
            panellist_id = row[0]
            player_id = row[1]
            score = row[2]
            if score < worst_score:
                result['WORST_PANELLIST_ID'] = panellist_id
                result['WORST_PLAYER_ID'] = player_id
                result['WORST_SCORE'] = score
                worst_score = score
            if score > best_score:
                result['BEST_PANELLIST_ID'] = panellist_id
                result['BEST_PLAYER_ID'] = player_id
                result['BEST_SCORE'] = score
                best_score = score
        local_cursor.close()
        local_conn.close()
        return result
    else:
        local_cursor.close()
        local_conn.close()
        return False

def create_initial_panel_data(desc='', size=0):  # creates initial panel full of robots
    conn = dbu.get_conn()
    my_cursor = conn.cursor()
    panel_id = id_generator.get_next_id('PANL',8)
    print ("Automatic panel ID is " + panel_id)
    if not desc:
        panel_desc = input("Panel Description: ")
    else:
        panel_desc = desc

    sql = ("INSERT INTO panels (panel_id, panel_desc) " +
           "VALUES ('" + panel_id + "','" + panel_desc + "')")
    my_cursor.execute(sql)
    conn.commit()
    print ("Panel " + panel_id + " created")

    if not size:
        panel_size = int(input("Enter no. of panellists: "))
    else:
        panel_size = int(size)

    sql_1 = ("SELECT robot_id, robot_instance FROM robots")
    result_1 = my_cursor.execute(sql_1)
    if result_1:
        robot_panellists = []
        rows = my_cursor.fetchall()
        for row in rows:
            robot_id = row[0]
            robot_instance = row[1]
            robot_panellists.append([robot_id, robot_instance])
        index = 0
        for i in range(panel_size):
            panellist_id = id_generator.get_next_id('PAST',8)
            robot_id = robot_panellists[index][0]
            blob = robot_panellists[index][1]
            sql_2 = ("INSERT INTO panellists (panel_id, panellist_id, player_id, acceded, player_instance) VALUES ('" +
                   panel_id + "', '" + panellist_id + "', '" + robot_id + "', NOW(), %s)")
            result_2 = my_cursor.execute(sql_2, (blob, ))
            index += 1
            if index >= len(robot_panellists):
                index = 0
        conn.commit()

        game_id = id_generator.get_next_id('GAME',8)
        game = c4game.Connect4Game(no_columns=parms.game_columns,
                                no_rows=parms.game_rows,
                                name=game_id,
                                winning_run=4)

        my_panel = Panel(panel_id)
        my_panel.link(game)

        survival_score = 99999

        for panellist_id in my_panel.panellists:
            player_id = my_panel.panellists[panellist_id]['ID']
            candidate = player.load_instance_from_database(player_id)
            result = my_panel.do_tests(candidate)
            if result and result['SUCCESS']:
                score = result['SCORE']
                #print (panellist_id + ' ' + player_id + ' Scored: ' + str(score))
                if score < survival_score:
                    survival_score = score
                blob = pickle.dumps(candidate, pickle.HIGHEST_PROTOCOL)
                sql = ("UPDATE panellists SET score = " + str(score) + ", player_instance = %s" +
                       " WHERE panellist_id = '" + panellist_id + "'")
                my_cursor.execute(sql, (blob, ))
                conn.commit()
            else:
                print (panellist_id + ' ** TEST ERROR **')

        sql = ("UPDATE panels SET survival_score = " + str(survival_score) + " WHERE panel_id = '" + panel_id + "'")
        my_cursor.execute(sql)

        result = {}
        result['PANEL_ID'] = panel_id
        result['PANEL_DESC'] = panel_desc
        result['SURVIVAL_SCORE'] = survival_score
        conn.commit()
        my_cursor.close()
        conn.close()
        return result
    else:
        print ("**ERROR** Could not retrieve robots")
        my_cursor.close()
        conn.close()
        return False
    my_cursor.close()
    conn.close()
    print ("**ERROR** not implemented")
    return False

def clone_panel_data(parent_panel_id, parent_desc, parent_survival_score,
                     change_panellist_id, new_player_id, new_player_instance):
    clone_panel_id = id_generator.get_next_id('PANL',8)
    conn = dbu.get_conn()
    my_cursor = conn.cursor()
    sql1 = ("INSERT INTO panels (panel_id, panel_desc, survival_score) VALUES ('"
           + clone_panel_id + "', '" + parent_desc + "', '" + str(parent_survival_score) + "')")
    my_cursor.execute(sql1)
    conn.commit()

    sql2 = ("SELECT panellist_id, player_id, acceded, player_instance FROM panellists WHERE panel_id = '" + parent_panel_id + "'")
    my_cursor.execute(sql2)
    rows = my_cursor.fetchall()
    for row in rows:
        panellist_id = row[0]
        player_id = row[1]
        acceded = row[2]
        player_instance = row[3]
        clone_panellist_id = id_generator.get_next_id('PAST',8)
        if panellist_id == change_panellist_id:     # substitute new panellist for old
            blob = pickle.dumps(new_player_instance, pickle.HIGHEST_PROTOCOL)
            sql4 = ("INSERT INTO panellists (panel_id, panellist_id, player_id, acceded, player_instance) " +
                   "VALUES ('" + clone_panel_id + "', '" + clone_panellist_id + "', '" + new_player_id + "', NOW(), %s)")
            sql3 = "UPDATE nets SET panellist = 1, keep = 'T' WHERE net_id = '" + new_player_id + "'"
            my_cursor.execute(sql3)
            sql3 = "UPDATE nets SET panellist = 0, keep = ' ' WHERE net_id = '" + player_id + "'"
            my_cursor.execute(sql3)
        else:   # copy old panellist
            blob = player_instance
            sql4 = ("INSERT INTO panellists (panel_id, panellist_id, player_id, acceded, player_instance) " +
                   "VALUES ('" + clone_panel_id + "', '" + clone_panellist_id + "', '" + player_id + "', '" + str(acceded) + "', %s)")
            #print (sql4)
        my_cursor.execute(sql4, (blob, ))
    conn.commit()

    my_cursor.close()
    conn.close()
    return clone_panel_id
    
class Panel():
    'Panel of opponents'

    def __str__(self):
        text_string = 'Panel ' + self.panel_id
        if self.panellist_count < 1:
            text_string += "\nNo Panellists Found"
        else:
            text_string += "\nPanellists:"
            for panellist in self.panellists:
                text_string += ("\n" + self.panellists[panellist]['ID'] + " ")
            text_string += "\n"
        return text_string

    def __init__(self, panel_id='NEXT_ONE'):    # Loads panel from database
        if panel_id == 'NEXT_ONE':
            self.panel_id = id_generator.get_next_id('PANL',8)
        else:
            self.panel_id = panel_id

        self.recording = False   ##################################

        conn = dbu.get_conn()
        my_cursor = conn.cursor()

        sql = 'SELECT panel_desc, survival_score, lowest_acceptable_score FROM panels WHERE panel_id = \'' + self.panel_id + '\''
        my_cursor.execute(sql)
        data_row = my_cursor.fetchone()
        if data_row is not None:
            self.panel_desc = data_row[0]
            self.survival_score = data_row[1]
            self.lowest_acceptable_score = data_row[2]
        else:
            self.panel_desc = 'No Description'
            self.survival_score = 0
        #print ('Initialising panel ' + self.panel_id + ' ' + self.panel_desc)

        sql = 'SELECT panellist_id, player_id, score, player_instance FROM panellists WHERE panel_id = \'' + self.panel_id + '\''
        my_cursor.execute(sql)
        data_rows = my_cursor.fetchall()
        self.panellist_count = 0
        self.game = None
        self.panellists = {}
        self.panel_index = []
        for data_row in data_rows:
            panellist_id = data_row[0]
            player_id = data_row[1]
            score = data_row[2]
            instance = data_row[3]
            self.panel_index.append(panellist_id)
            self.panellists[panellist_id] = {}
            self.panellists[panellist_id]['SCORE']    = score
            self.panellists[panellist_id]['ID']       = player_id
            self.panellists[panellist_id]['INSTANCE'] = pickle.loads(instance)
            if 'RBOT' == player_id[0:4]:  # it's a robot
                self.panellists[panellist_id]['TYPE']     = 'ROBOT'
            else:  # it's a neural network
                self.panellists[panellist_id]['TYPE']     = 'NETWORK'
            self.panellist_count += 1
            
        my_cursor.close()
        conn.close()
        self.next_panellist = 0
        if self.panellist_count < 1:
            print ('No panellists found')
            self.panel_ok = False
        else:
            self.panel_ok = True

    def add(self, panellist_id):
        conn = dbu.get_conn()
        my_cursor = conn.cursor()
        sql = ('INSERT INTO panellists (panel_id, panellist_id) VALUES (\'' +
               self.panel_id + '\', \'' + panellist_id + '\')')
        my_cursor.execute(sql)
        conn.commit()
        my_cursor.close()
        conn.close()

    def link(self, game):
        self.game = game

    def get_next_panellist(self):
        self.next_panellist += 1
        if self.next_panellist >= len(self.panellists):
            self.next_panellist = 0
        panellist_id = self.panel_index[self.next_panellist]
        return self.panellists[panellist_id]['INSTANCE']

    def play_panellist(self, player, panellist_id):
        panellist = self.panellists[panellist_id]['INSTANCE']
        return panellist.propose_column(self.game.game_state, player, self.game.winning_run)
        
    def save_game_moves(self, player_name, opponent_name, winner, game_moves):
        if not self.recording:
            return False
        conn = dbu.get_conn()
        my_cursor = conn.cursor()
        sql = ('INSERT INTO results (result_id, winner, loser, who_winner, game_moves) VALUES ('
               '\'' + id_generator.get_next_id('RSLT',8) +'\',\'' + player_name + '\',\'' +
               opponent_name + '\',' + str(winner) + ',\'' + game_moves + '\')')
        my_cursor.execute(sql)
        conn.commit()
        my_cursor.close()
        conn.close()
        return True 

    def print_panellist_data(self):
        print (self.panel_id)
        print (str(self.panellist_count) + " panellists")
        for panellist_id in self.panellists:
            print (panellist_id + " " + str(self.panellists[panellist_id]))

    def do_tests(self, candidate, recording=False, printing=False):
        result = {}
        result['SUCCESS'] = False
        self.candidate_wins_as_2 = 0
        self.candidate_wins_as_1 = 0
        self.candidate_draws = 0
        self.candidate_losses = 0
        game_moves = ''
        self.recording = recording
        for i in range(self.panellist_count):  # play each panellist
            opponent = self.get_next_panellist()
            player_name = candidate.id
            opponent_name = opponent.id
            for j in range(2): # alternate whether the candidate plays first or second
                self.game.reset()
                max_iterations = int((self.game.no_columns * self.game.no_rows) / 2)
                game_result = False
                which_move = 0
                for k in range(max_iterations):
                    if j==0 or k>0:  # Candidate plays
                        which_move += 1
                        proposed_column = candidate.propose_column(self.game.game_state, j, self.game.winning_run)
                        game_moves += str(proposed_column)
                        if proposed_column == 0:
                            self.game.skip_move()
                        else:
                            sub_result = self.game.play_in(proposed_column)
                            if sub_result['SUCCESS']:
                                if sub_result['WON']:
                                    self.save_game_moves(player_name, opponent_name, which_move % 2, game_moves)
                                    game_result = True
                                    if j==1:
                                        self.candidate_wins_as_2 += 1
                                    else:
                                        self.candidate_wins_as_1 += 1
                                    break

                    # Panellist plays
                    which_move += 1
                    proposed_column = opponent.propose_column(self.game.game_state, 1-j, self.game.winning_run)
                    game_moves += str(proposed_column)
                    if proposed_column == 0:
                        self.game.skip_move()
                    else:
                        sub_result = self.game.play_in(proposed_column)
                        if sub_result['SUCCESS']:
                            if sub_result['WON']:
                                self.save_game_moves(player_name, opponent_name, which_move % 2, game_moves)
                                game_result = True
                                self.candidate_losses += 1
                                break
                if not game_result:
                    self.candidate_draws += 1

        result['WINS_AS_1'] = self.candidate_wins_as_1
        result['WINS_AS_2'] = self.candidate_wins_as_2
        result['LOSSES'] = self.candidate_losses
        result['DRAWS'] = self.candidate_draws
        candidate_score = game_utils.get_score(self.candidate_wins_as_2, self.candidate_wins_as_1, self.candidate_draws, self.candidate_losses)
        result['SCORE'] = candidate_score
        result['SUCCESS'] = True
        return result
