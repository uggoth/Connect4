
class Player():
    'Base class for Connect 4 playing objects'

    save_folder = 'Nets'

    def __init__(self):  # MUST OVERRIDE
        # Must set id and name
        print ('** ERROR in player class definition no init **')

    def __str__(self):  # MUST OVERRIDE
        print ('** ERROR in player class definition no str **')

    def save_self_to_database(self):  # MUST OVERRIDE
        print ('** ERROR in player class definition no save **')

    def propose_column(self, game_state, whoami, winning_run=4):
        # returns column to play in, or 0 if can't cope
        # MUST ADD TO (or override)
        # game_state is an array 7 columns by 6 rows.
        # element game_state[x][y] is row y+1 of column x+1 because array is zero-based
        # each element contains 0 - empty, or player
        # player is 1 for red or 2 for yellow
        # whoami is 0 for red or 1 for yellow (i.e. player - 1)
        # winning_run is 4 for Connect 4
        self.game_state = game_state # NOTE: any test states must be the same shape
        self.no_columns = len(game_state)
        self.no_rows = len(game_state[0])
        self.whoami = whoami
        self.winning_run = winning_run

    def export_self_to_file(self):  # MUST OVERRIDE
        print ('** ERROR in player class definition no save **')

