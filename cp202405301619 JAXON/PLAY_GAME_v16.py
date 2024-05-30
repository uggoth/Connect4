from tkinter import *
import pickle
import neural_network_v18 as nn
import time
import game_v09 as c4g
import parameters_v35 as parms
import robots_v07 as robot
import panel_v12 as panel
import database_utils_v04 as dbu
mysql = dbu.mariadb
#import ioif_v32 as ioif

class MyButton():
    def __init__(self, master, dtext, dx, dy, dwidth, dheight):
        b = Button(master, text=dtext, command=self.callback,
                   width=dwidth, height=dheight)
        b.place(x=dx, y=dy, anchor=NW)
        self.dx = dx
        self.dy = dy
        self.dwidth = dwidth
        self.dheight = dheight
        self.instance = b
        self.dtext = dtext
    def callback(self): # MUST OVERRIDE
        print ('**ERROR**')

class QuitButton(MyButton):
    def __init__(self, display, dx, dy):
        dtext = 'QUIT'
        dwidth = 4
        dheight = 2
        self.display = display
        MyButton.__init__(self, display.frame, dtext, dx, dy, dwidth, dheight)
        self.instance.config(background='#DD4455')
        self.instance.config(foreground='#FFFF55')
        self.instance.config(font=('Helvetica',15,'bold'),justify='left')
    def callback(self):
        display.root.destroy()

class ResetButton(MyButton):
    def __init__(self, display, dx, dy):
        dtext = 'RESET'
        dwidth = 5
        dheight = 2
        self.display = display
        MyButton.__init__(self, display.frame, dtext, dx, dy, dwidth, dheight)
        self.instance.config(background='#883344')
        self.instance.config(foreground='#FFFF55')
        self.instance.config(font=('Helvetica',15,'bold'),justify='left')
    def callback(self):
        self.display.game.reset()
        self.display.show_game()
        self.display.game.player = 1
        self.display.show_player()
        for i in range(len(self.display.status_display)):
            self.display.show_status(i,' ')

class AutoplayContinuous(MyButton):
    def __init__(self, display, dx, dy, player):
        self.player = player
        self.display = display
        self.set = False
        MyButton.__init__(self, display.frame, dtext= 'AUTOPLAY ALL', dx=dx, dy=dy, dwidth=10, dheight=1)
        self.set_colour()
    def set_colour(self):
        if self.set:
            self.instance.config(foreground=self.display.colours['BLACK'])
            self.instance.config(background=self.display.colours['GREEN'])
        else:
            self.instance.config(foreground=self.display.colours['BLACK'])
            self.instance.config(background=self.display.colours['GREY'])
    def callback(self):
        self.set = not self.set
        self.set_colour()
        self.display.root.update_idletasks()

class AutoplayButton(MyButton):
    def __init__(self, display, dx, dy, player):
        self.player = player
        self.display = display
        MyButton.__init__(self, display.frame, dtext= 'AUTOPLAY ONCE', dx=dx, dy=dy, dwidth=10, dheight=1)
        self.instance.config(background=self.display.colours['GREY'])
        self.instance.config(foreground=self.display.colours['BLACK'])
    def callback(self):
        if self.player != self.display.game.next_player:
            self.display.show_status(1,'** Not your turn **')
            return
        if self.display.game.game_over:
            self.display.show_status(1,'** Game Over **')
            return
        this_player = self.display.players[self.player]
        player_type = this_player.type_var.get()
        player_name = this_player.name_var.get()[0:12]
        opponent_player = self.display.players[1 - self.player]
        opponent_type = opponent_player.type_var.get()
        opponent_name = opponent_player.name_var.get()[0:12]
        #print ('Playing ' + player_name + ' ' + player_type)
        if player_type == 'HUMAN':
            text_string = 'Human opponent selected. Can\'t autoplay'
            print (text_string)
            self.display.show_status(1,text_string)
            return
        elif player_type == 'PANELLIST':     
            player_id = this_player.panellist_var.get()[0:12]
            panellist_id = self.display.panellist_index[player_id]
            column = self.display.my_panel.play_panellist(self.player,panellist_id)
        elif player_type == 'NETWORK':     
            net_id = this_player.network_var.get()[0:12]
            instance = self.display.best_nets[net_id]['INSTANCE']
            whoami = 2 - self.player
            winning_run = 4
            game_state  = self.display.game.game_state
            column = instance.propose_column(game_state, whoami, winning_run)
        else:
            self.display.show_status(1,'No opponent selected')
            return
        if column == 0:
            text_string = 'Player ' + player_name + ' has no idea'
            print (text_string)
            self.display.show_status(1,text_string)
            return
        self.display.make_a_move(column, player_name, opponent_name)
        if not self.display.game.game_over:
            if opponent_player.all_button.set:   # play his turn as well
                opponent_player.once_button.callback()

class ColumnButton(MyButton):
    def __init__(self, display, column):
        self.display = display
        self.column = column
        dtext = str(self.column)
        dx = ((self.column - 1) * self.display.h_spacing) + self.display.game_h_offset + 20
        dy = 670
        dwidth = 3
        dheight = 1
        MyButton.__init__(self, self.display.frame, dtext, dx, dy, dwidth, dheight)
        self.instance.config(background='#114455')
        self.instance.config(foreground='#DDFFEE')
        self.instance.config(font=('Helvetica',22,'bold'),justify='left')
    def callback(self):
        which_player = self.display.game.next_player
        this_player = self.display.players[which_player]
        player_name = this_player.name_var.get()[0:12]
        opponent_player = self.display.players[1 - which_player]
        opponent_type = opponent_player.type_var.get()
        opponent_name = opponent_player.name_var.get()[0:12]
        self.display.root.update_idletasks()

        self.display.make_a_move(self.column, player_name, opponent_name)
        time.sleep(0.3)
        self.display.root.update_idletasks()
        if not self.display.game.game_over:
            opponent_player = self.display.players[1 - which_player]
            if opponent_player.all_button.set:   # play his turn as well
                time.sleep(1.5)
                opponent_player.once_button.callback()
            time.sleep(0.1)
            self.display.root.update_idletasks()

class ConsecutivesButton(MyButton):        
    def __init__(self, display, column):
        self.display = display
        self.column = column
        dtext = 'C' + str(self.column)
        dx = ((self.column - 1) * self.display.h_spacing) + self.display.game_h_offset + 40
        dy = 700
        dwidth = 1
        dheight = 1
        MyButton.__init__(self, self.display.frame, dtext, dx, dy, dwidth, dheight)
        self.instance.config(background='#114455')
        self.instance.config(foreground='#FFFF55')
        self.instance.config(font=('Helvetica',12,'bold'),justify='left')
    def callback(self):
        game = self.display.game
        player = game.next_player
        free_row = game.free_row(self.column)
        if free_row > 0:
            sub_result = game.consecutive_count(player,free_row,self.column)
            self.display.show_status(0,'Consecutives ' + str(sub_result))
        else:
            self.display.show_status(0,'Can\'t play in that column')

class Player_UI():
    def __init__(self, display, which_player, x_offset, y_offset):
        self.display = display
        self.which_player = which_player
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.panellist_list = []
        self.display.panellist_index = {}

        for panellist_id in display.my_panel.panellists:
            player = display.my_panel.panellists[panellist_id]['ID']
            score = display.my_panel.panellists[panellist_id]['SCORE']
            if score:
                score_string = ' Score {:3d}'.format(int(score))
            else:
                score_string = ' Score 000'
            panellist_string = player + score_string
            self.panellist_list.append(panellist_string)
            self.display.panellist_index[player] = panellist_id

        self.net_list = []
        self.display.net_index = {}

        for net_id in display.best_nets:
            score = display.best_nets[net_id]['SCORE']
            if score:
                score_string = ' Score {:3d}'.format(int(score))
            else:
                score_string = ' Score 000'
            net_string = net_id + score_string
            self.net_list.append(net_string)
            self.display.net_index[player] = net_id

        default_name = 'Player_' + str(which_player+1)
        self.name_var = StringVar(self.display.frame, value=default_name)
        self.name_entry = Entry(self.display.frame,width=20,textvariable=self.name_var)
        self.name_entry.place(x=x_offset,y=y_offset)

        self.type_var = StringVar(self.display.frame, value='HUMAN')

        y_offset += 50
        entry_offset = 95
        self.radion = Radiobutton(self.display.frame, text='Panellist',
                                    variable=self.type_var, value='PANELLIST', command=self.panellist_type_selector_pressed)
        self.radion.place(x=x_offset,y=y_offset)

        self.panellist_var = StringVar(self.display.frame)
        self.panellist_selector = OptionMenu(self.display.frame, self.panellist_var, self.panellist_list[0], *self.panellist_list)
        self.panellist_var.set(self.panellist_list[0])
        self.panellist_selector.place(x=x_offset + entry_offset,y=y_offset)

        y_offset += 50
        entry_offset = 95
        self.radio2 = Radiobutton(self.display.frame, text='Network',
                                    variable=self.type_var, value='NETWORK', command=self.network_type_selector_pressed)
        self.radio2.place(x=x_offset,y=y_offset)

        self.network_var = StringVar(self.display.frame)
        self.network_selector = OptionMenu(self.display.frame, self.network_var, self.net_list[0], *self.net_list)
        self.network_var.set(self.net_list[0])
        self.network_selector.place(x=x_offset + entry_offset,y=y_offset)

        y_offset += 50
        self.human_radio = Radiobutton(self.display.frame, text='Human',
                                    variable=self.type_var, value='HUMAN', command=self.human_type_selector_pressed)
        self.human_radio.place(x=x_offset,y=y_offset)

        self.human_var = StringVar(self.display.frame)
        self.human_entry = Entry(self.display.frame,width=15,textvariable=self.human_var)
        self.human_entry.place(x=x_offset+77,y=y_offset)

        y_offset += 50
        self.once_button = AutoplayButton(self.display, dx=x_offset, dy=y_offset, player=which_player)
        x_offset = x_offset + 150
        self.all_button = AutoplayContinuous(self.display, dx=x_offset, dy=y_offset, player=which_player)

    def set_game_over(self):
        self.name_entry.config(background=self.display.colours['GREY'])

    def set_yellow(self):
        self.name_entry.config(background=self.display.colours['YELLOW'])

    def set_red(self):
        self.name_entry.config(background=self.display.colours['RED'])

    def human_type_selector_pressed(self):
        self.type = 'HUMAN'
        self.name = self.human_var.get()
        self.name_var.set(self.name)

    def network_type_selector_pressed(self):
        self.type = 'NETWORK'
        self.name = self.network_var.get()
        self.name_var.set(self.name)

    def panellist_type_selector_pressed(self):
        self.type = 'PANELLIST'
        self.name = self.panellist_var.get()
        self.name_var.set(self.name)

class Display():

    def make_a_move(self, column, player_name, opponent_name):
        result = self.game.play_in(column)
        if result['SUCCESS']:
            print (player_name + ' plays in ' + str(column))
            self.game_moves += str(column)
            row = result['ROW']
            self.show_status(0,'Consecutives ' + str(result['CONSECUTIVES']))
            self.show_status(1,'Dropping counter for ' + player_name + ' in column ' + str(column))
            self.show_status(2,'Counter went in row ' + str(row) + ' of column ' + str(column))
            self.show_game()
            if result['WON']:
                winner = result['WINNER']
                print (winner)
                conn = dbu.get_conn()
                my_cursor = conn.cursor()
                sql = ('INSERT INTO results (result_id, winner, loser, who_winner, game_moves) VALUES ('
                       '\'' + dbu.get_next_id('RSLT',8) +'\',\'' + player_name + '\',\'' +
                       opponent_name + '\',' + str(winner) + ',\'' + self.game_moves + '\')')
                my_cursor.execute(sql)
                conn.commit()
                my_cursor.close()
                conn.close()
                win_string = player_name + ' ******* WON ********'
                print (win_string)
                status_line = 1
                self.show_status(status_line, win_string)
                self.flash_status(status_line, winner)
                self.game_moves = ''
            self.show_player()
        else:
            self.show_status (0,'** ERROR CAN\'T PLAY IN ' + str(column) + ' **')
        

    def load_net(self, net_name):
        conn = dbu.get_conn()
        my_cursor = conn.cursor()
        sql = 'SELECT filename FROM nets WHERE net_id = \'' + net_name + '\''
        my_cursor.execute(sql)
        row = my_cursor.fetchone()
        if row is not None:
            filename = row['filename']
            with open(filename,'rb') as infile:
                my_net = pickle.load(infile)
                return my_net
        return False

    def link_net(self, this_net, game):
        this_net.game = game

#######################

    def __init__(self, root, game):
        self.root = root
        self.game = game
        current_panel = parms.current_panel
        self.my_panel = panel.Panel(current_panel)
        self.my_panel.link(self.game)
        self.my_panel.print_panellist_data()
        #ioif.print_dictionary (panel.get_panellist_info(current_panel))
        self.frame_width = 1600
        self.frame_height = 1000
        self.frame = Frame(root, width=self.frame_width, height=self.frame_height, background='#DDDDDD')
        self.frame.pack()
        self.game_h_offset = 440
        self.game_v_offset = 30
        canvas_height = 650
        canvas_width = 800
        self.game_canvas = Canvas(self.frame, width=canvas_width, height=canvas_height, background='#DDDDDD')
        self.game_canvas.place(x=self.game_h_offset, y=self.game_v_offset, anchor=NW)
        self.game_canvas.create_rectangle(0,0,715,615,fill='#0000CC')
        self.game_moves = ''

        self.colours = {}
        self.colours['GREY'] = '#EEEEEE'
        self.colours['RED'] = '#FF2222'
        self.colours['YELLOW'] = '#CCCC00'
        self.colours['GREEN'] = '#00FFFF'
        self.colours['BLACK'] = '#000000'
        self.colours['PINK'] = '#EEDDCC'
        self.colour_display = None
        self.h_offset = 20
        self.h_spacing = 100
        self.v_offset = -80
        self.v_spacing = 100
        self.diameter = 75

###########################################

        generation = parms.species
        print ('Generation:', generation)

###########################################

        conn = dbu.get_conn()
        my_cursor = dbu.get_cursor(conn)

        self.best_nets = {}
        sql = ("SELECT net_id, score, instance FROM nets " +
               "WHERE species='" + generation + "' " +
               "ORDER BY score DESC LIMIT 10")
        my_cursor.execute(sql)
        no_best_nets = 0
        for row in my_cursor:
            net_id = row['net_id']
            score = row['score']
            instance = pickle.loads(row['instance'])
            self.best_nets[net_id] = {}
            self.best_nets[net_id]['SCORE'] = score
            self.best_nets[net_id]['INSTANCE'] = instance
            no_best_nets += 1
        if no_best_nets < 1:
            print ("** NO NETS FOUND **")

        self.column_buttons = []
        for i in range(game.no_columns):
            self.column_buttons.append(ColumnButton(self,i+1))

        self.reset_button = ResetButton(self, dx=440, dy=850)
        self.quit_button  = QuitButton (self, dx=1100, dy=850)
        self.opponent_neural_move = 4

################################################################

        self.players = []
        self.players.append(Player_UI(self, which_player=0, x_offset=50, y_offset=300))
        self.players.append(Player_UI(self, which_player=1, x_offset=1230, y_offset=300))

################################################################

        self.next_player = 0
        x_offset = 620
        y_offset = 750
        spacing = 30
        self.status_display = []
        for i in range(3):
            self.status_display.append(Entry(self.frame, width=45))
            status_y = y_offset + (spacing * i)
            self.status_display[i].place(x=x_offset,y=status_y,anchor=NW)
        my_cursor.close()
        conn.close()
        self.show_game()

    def show_player(self):
        next_player = self.game.next_player
        if self.game.game_over:
            self.show_status (0,'Game Over')
            self.players[0].set_game_over()
            self.players[1].set_game_over()
        elif next_player == 1:
            self.show_status (0,'Yellow to Play')
            self.players[0].set_game_over()
            self.players[1].set_yellow()
        else:
            self.show_status (0,'Red to Play')
            self.players[0].set_red()
            self.players[1].set_game_over()

    def show_status(self, which, message):
        if which < 0:
            return False
        if which > len(self.status_display):
            return False
        self.status_display[which].delete(0,END)
        self.status_display[which].insert(0, message)

    def flash_status(self, status_line, winner):
        if status_line < 0:
            return False
        if status_line > len(self.status_display):
            return False
        for i in range(7 + winner):
            if i%2 == 0:
                self.status_display[status_line].config(background = self.colours['RED'])
            else:
                self.status_display[status_line].config(background = self.colours['YELLOW'])
            self.root.update_idletasks()
            time.sleep(0.3)
        
    def show_game(self):
        for y in range(self.game.no_rows):
            for x in range(self.game.no_columns):
                dx = self.h_offset + (x * self.h_spacing)
                dy = self.v_offset + ((self.game.no_rows - y) * self.v_spacing)
                state = self.game.game_state[x][y]
                if state == 0:
                    filling = '#DDDDDD'
                elif state == 1:
                    filling = self.colours['RED']
                elif state == 2:
                    filling = self.colours['YELLOW']
                else:
                    filling = self.colours['BLACK']
                self.game_canvas.create_oval(dx,dy,dx+self.diameter,dy+self.diameter, fill=filling)
        self.show_player()

game = c4g.Connect4Game(no_columns=7, no_rows=6, name='CONNECT_4_GAME', winning_run=4)

root = Tk()

display = Display(root, game)

root.mainloop()
