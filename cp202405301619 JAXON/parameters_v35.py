import mysql.connector as mariadb
import pickle

species = 'GENERATION_52'

if species in ['GENERATION_52',
               'GENERATION_53']:
    # General parms
    session_id = 'SESS00000002'
    net_folder = 'Nets'
    save_to_folder = False
    win_as_1_score = 2
    win_as_2_score = 4
    draw_score = 1
    loss_score = 0
    current_panel = 'PANL00000006'
    # Testing parms
    test_state_selector = 'A'
    game_columns = 7
    game_rows = 6
    game_winning_run = 4
    # Randomiser parms
    sessions_count = 99
    trials_count = 9999
    lowest_acceptable_score = 23
    min_nets_per_session = 1
    max_nets_per_trial = 7
    max_nets_per_session = 17
    warn_interval = 200
    # Variegator parms
    iterations = 999
    attempts = 53
    min_successes = 2
    max_successes = 9
    max_deterioration = 6
    logic_threshold_low_low = 0.1
    logic_threshold_low_high = 55
    logic_threshold_high_low = logic_threshold_low_low * 1.1
    logic_threshold_high_high = logic_threshold_low_high * 4
    logic_weight_low_low = -10
    logic_weight_low_high = 0.1
    logic_weight_high_low = 1
    logic_weight_high_high = 10
    motor_threshold_low_low = 0.1
    motor_threshold_low_high = 55
    motor_threshold_high_low = motor_threshold_low_low * 1.1
    motor_threshold_high_high = motor_threshold_low_high * 6
    motor_weight_low_low = -10
    motor_weight_low_high = -0
    motor_weight_high_low = 1
    motor_weight_high_high = 10
    logic_count_low = 3
    logic_count_high = 25
    memory_count_low = 0
    memory_count_high = 0
