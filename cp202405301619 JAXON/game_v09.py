class Connect4Game():

    # column is usually from 1 to 7. In which case 1 is the left column
    # and the game_state column index (x) is from 0 to 6
    # row is usually from 1 to 6. In which case 1 is the bottom row
    # and the game_state row index (y) is from 0 to 5
    # game_state[x][y] is the state of row(y+1) of column(x+1)
    # state is 0 for empty, 1 for red, 2 for yellow
    # next_player is 0 for red, 1 for yellow
    # after playing in a position, state = next_player + 1
    # a winning run is usually 4 consecutive counters

    def __init__(self, name, no_columns=7, no_rows=6, winning_run=4):
        self.name = name
        self.no_columns = no_columns
        self.no_rows = no_rows
        self.winning_run = winning_run
        self.reset()

    def reset(self):
        self.last_x = 0
        self.last_y = 0
        self.game_over = False
        self.next_player = 0
        self.consecutives = []
        for i in range(2):
            self.consecutives.append([])
            for j in range(self.no_columns):
                self.consecutives[i].append([])
                for k in range(self.no_rows):
                    self.consecutives[i][j].append(-1)
        self.game_state = []
        for x in range(self.no_columns):
            self.game_state.append([])
            for y in range(self.no_rows):
                self.game_state[x].append(0)

    def whats_in(self, column, row):    # returns 0,1,2
        x = column - 1
        y = row - 1
        return self.game_state[x][y]

    def skip_move(self):
        self.next_player = 1 - self.next_player

    def play_in(self, column):
        result = {}
        result['SUCCESS'] = False
        if self.game_over:
            return result
        if ((column > self.no_columns) or (column < 1)):
            result['SUCCESS'] = False
            return result
        row = self.free_row(column)
        if row:
            this_player = self.next_player
            new_state = this_player + 1
            x = column - 1
            y = row - 1
            self.game_state[x][y] = new_state
            self.last_x = x
            self.last_y = y
            result['SUCCESS'] = True
            result['ROW'] = row
            for i in range(2): # A move has been made. Counts are now invalid
                for j in range(self.no_columns):
                    for k in range(self.no_rows):
                        self.consecutives[i][j][k] = -1
            consecutives = self.consecutive_count(this_player, row, column)
            result['CONSECUTIVES'] = consecutives
            if consecutives >= self.winning_run:
                result['WON'] = True
                result['WINNER'] = this_player
                self.game_over = True
            else:
                result['WON'] = False
            self.next_player = 1 - self.next_player
            return result
        else:
            result['SUCCESS'] = False
            return result

    def free_row(self, column):
        x = column - 1
        for y in range(self.no_rows):
            if self.game_state[x][y] == 0:
                return y+1
        return 0

    def what_if(self, player, column): # returns the number of consecutive counters of player colour if player plays in column
        row = self.free_row(column)
        if row:
            return self.consecutive_count(player, row, column)
        else:
            return 0

    def consecutive_count(self, player, row, column, test_state=None):     # returns the number of consecutive counters of player colour if
                                            # player plays in row, column
        play_x = column - 1
        play_y = row - 1
        play_state = player + 1
        if test_state is None:
            game_state = self.game_state
        else:
            game_state = test_state

        best_run = 0

        if self.consecutives[player][play_x][play_y] != -1: # see if have saved value
            return self.consecutives[player][play_x][play_y]

        # East West
        consecutive = 1 # number of counters in line; starting with the counter to be played
        for check_x in range(play_x + 1, self.no_columns):
            if game_state[check_x][play_y] == play_state:
                consecutive += 1
            else:
                break
        for check_x in range(play_x - 1, -1, -1):
            if game_state[check_x][play_y] == play_state:
                consecutive += 1
            else:
                break
        if consecutive > best_run:
            best_run = consecutive

        # North South
        consecutive = 1
        for check_y in range(play_y + 1, self.no_rows):
            if game_state[play_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        for check_y in range(play_y - 1, -1, -1):
            if game_state[play_x][check_y] == play_state:
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
            if game_state[check_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        check_x = play_x
        for check_y in range(play_y - 1, -1, -1):
            check_x -= 1
            if check_x < 0:
                break
            if game_state[check_x][check_y] == play_state:
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
            if game_state[check_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        check_x = play_x
        for check_y in range(play_y - 1, -1, -1):
            check_x += 1
            if check_x >= self.no_columns:
                break
            if game_state[check_x][check_y] == play_state:
                consecutive += 1
            else:
                break
        if consecutive > best_run:
            best_run = consecutive

        self.consecutives[player][play_x][play_y] = best_run  # save value in case asked again        
        return best_run
