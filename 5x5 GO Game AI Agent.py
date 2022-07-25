import copy

#Finds dead counters if we place a counter on any location on the board. This functions logic is refered from host.py
def find_dead_counter(latest_board_copy, opp_turn_col):
    count_dead=0
    dead_counter = []
    #Traverses the whole board to check
    for q in range(0,5):
        for w in range(0,5):
            # When an opponents counter is on the board, and it does not have any liberty and dead_counter is empty then append to a list.
            if latest_board_copy[q][w] == opp_turn_col:
                if not liberty_count(latest_board_copy, q, w):
                    if (q,w) not in dead_counter:
                        count_dead=count_dead+1
                        dead_counter.append((q, w))
    return dead_counter


# For a given coordinate function finds all the adjacent counters to it. This functions logic is refered from host.py
def search_adj_counter(latest_board_copy, q, w):
    count_neigh=0
    latest_board_copy = remove_dead_counter(latest_board_copy, (q, w))
    adj_nb=[]
    if q > 0: adj_nb.append((q-1, w))
    if q < len(latest_board_copy) - 1: adj_nb.append((q+1, w))
    if w > 0:adj_nb.append((q, w-1))
    if w < len(latest_board_copy) - 1:adj_nb.append((q, w+1))
    
    return adj_nb

# For a player, removes the dead counters. This functions logic is refered from host.py
def remove_dead_counter(latest_board_copy, opp_turn_col):
    dead_counter = find_dead_counter(latest_board_copy, opp_turn_col)
    #print(dead_counter)
    if not dead_counter:
        #print("not present")
        return latest_board_copy
    # Remove the counters now.
    new_latest_board = remove_counters(latest_board_copy, dead_counter)
    return new_latest_board


#Removes specified coordinates counters. This functions logic is refered from host.py
def remove_counters(latest_board_copy, spot):
    #counter_rmv= counter_rmv+1
    #print(counter_rmv)
    for counter in spot:
        latest_board_copy[counter[0]][counter[1]] = 0
    return latest_board_copy

#Checks which neighbor is of same color, if it then it appends to a list. This functions logic is refered from host.py
def search_neighbors_allies(latest_board_copy, q, w):
    #Initialise ally list for storing all ally.
    ally = []
    # Get neighboring nodes
    nbs= search_adj_counter(latest_board_copy, q, w)
    # Go through all the nodes and check color
    for dot in nbs:
        if latest_board_copy[dot[0]][dot[1]] == latest_board_copy[q][w]:
            ally.append(dot)
    return ally

# Calulates how much liberty does a coordinate has. This functions logic is refered from host.py
def liberty_count(latest_board_copy, q, w):
    #Initialise the liberty to be zero as it is taken a fresh for every coordinate.
    total_liberty = 0
    #Copying for reference
    latest_board_v2 = copy.deepcopy(latest_board_copy)
    #print(latest_board_v2)
    # Get all the same color nodes using DFS.
    friendly_memb=find_friends_group(latest_board_copy, q, w)
    # For every same color node in a group calculate its adjacent nodes.
    #print(friendly_memb)
    #print("Inside liberty count now got the neighbor ally nodes")
    for pt in friendly_memb:
        friendly_neigh=search_adj_counter(latest_board_copy,  pt[0], pt[1])
        # For every adjacent coordinate check if 0 then it has some liberty and add that to the total_liberty.
        for dot in friendly_neigh:
            # If the friends have unplayed node nearby increase total liberty.
            if latest_board_copy[dot[0]][dot[1]] == 0:
                total_liberty = total_liberty + 1

    return total_liberty

# Using DFS, we search for all the same color counter in a group. This functions logic is refered from host.py
def find_friends_group(latest_board_copy, q, w):
    #Place the first element on the stack
    stack = [(q, w)]
    # Create an empty list friends.
    friends = []
    # Loop till the stack is not empty
    while stack:
        # Remove the first element and append.
        pcs = stack.pop()
        friends.append(pcs)
        neigh_friends = search_neighbors_allies(latest_board_copy,pcs[0], pcs[1])
        # Append all the neighbors in the stack if not already in stack and not in friends.
        for frn in neigh_friends:
            if frn not in stack and frn not in friends:
                stack.append(frn)
    return friends

#This checks if we have violated the ko rule by playing a move by placing a counter on the board. This functions logic is refered from host.py
def check_if_ko(last_board, latest_board_copy):
    #For all moves check if last and latest board are exactly the same for every counter on the board.
    for q in range(0,5):
        for w in range(0,5):
            # Compare with the previous move board after removing counters.
            if last_board[q][w] != latest_board_copy[q][w]:
                return False
    # Ko rule detected. Wrong move. So, dont play
    return True


# To get the input from the input file in the same folder. get_input is defined with the reference to input file from read file from vocareum.
def get_input():
    with open("input.txt", 'r') as read_file:
        ly=read_file.readlines()
        all_inp = []
        fi=[]
        no_of_lines=0
        for stream in ly:
            ip=stream.strip()
            no_of_lines=no_of_lines+1
            all_inp.append(ip)

    #line_items = list(map(int, file.readline().strip().split()))
    #Takes in the last board, latest board and turn of player from the input file and store them in list of tuples for easy access.
    last_board = [[int(numbers) for numbers in stream] for stream in all_inp[1:6]]
    latest_board = [[int(numbers) for numbers in stream] for stream in all_inp[6:11]]
    turn_of_player = int(all_inp[0])
    #print(last_board)
    #print(latest_board)
    #print(turn_of_player)
    #print(no_of_lines)

    return last_board, latest_board, turn_of_player


# This function evaluates all the legal moves for going through all the tokens and checking if ko & liberty rules.
def find_legit_moves(last_board, latest_board, turn_of_player):
    legit_mvs = []
    dsp=0
    #For comparison after remove dead counters. If there were any
    latest_board_v3 = copy.deepcopy(latest_board)
    #print(latest_board_v3)
    #Looping through all the possible coordinates and check for legitimate moves possible.
    for q in range(0,5):
        for w in range(0,5):
            #Checks for any moves have been played yet
            is_blank = False
            if latest_board[q][w] != 0:
                is_blank = True
            if not is_blank:
                dsp=dsp+1
                latest_board_copy = copy.deepcopy(latest_board)
                #Putting our counter on the board.
                latest_board_copy[q][w] = turn_of_player
                latest_board_compare = copy.deepcopy(latest_board)
                #Finding all the dead counters of opponent after playing our move
                rev_player= 3 - turn_of_player
                dead_counter = find_dead_counter(latest_board_copy, rev_player)
                # Then remove all opponents dead counters
                len(latest_board_compare)
                #print(dsp)
                latest_board_copy = remove_dead_counter(latest_board_copy, rev_player)
                #Checks that there should be no ko violation and dead counters
                if not (check_if_ko(last_board, latest_board_copy) and dead_counter):
                    if liberty_count(latest_board_copy, q, w) > 0:
                        #If there is some liberty then append it to the set of legit moves
                        legit_mvs.append((q,w))

    #print(legit_mvs)
    return legit_mvs

# Calculate heuristic utilizing no of counters on board, liberty and komi score.
def estimated_hr(clr, played_state, latest_board_duplicate):
    # Variables for total tokens on the board
    play_token,opo_token = 0,0
    # Variables for total evaluation
    total_play,total_opo=0,0
    
    for q in range(0,5):
        for w in range(0,5):
            # if score is low add avoid edges heuristic.
            #Calculate liberty and no. of tokens for the oponent 
            if played_state[q][w] == 3 - turn_of_player:
                # Discourages if the move is played on the edge of the board.
                edge_heur= weigh_edge(q,w)
                opo_liberty = liberty_count(played_state, q, w)
                opo_token = opo_token + 1
                #print(opo_liberty)
                #print(opo_token)
                # Calculate total score by adding both
                total_opo += opo_token + opo_liberty + (0.1*edge_heur)

            #Calculate liberty and no. of tokens for us
            elif played_state[q][w] == turn_of_player:
                # Discourages if the move is played on the edge of the board.
                edge_heur2= weigh_edge(q,w)
                play_liberty = liberty_count(played_state, q, w)
                #print(play_liberty)
                play_token = play_token + 1
                # Calculate total score by adding both
                total_play +=play_token + play_liberty + (0.1*edge_heur2)
    
    # Calculate total difference in tokens on board and liberty. 
    heuristic = total_play - total_opo
    komi_score=2.5
    # Return heuristic with komi added if white.
    if clr == turn_of_player and clr==2:
        return komi_score+heuristic
    elif clr == turn_of_player:
        return heuristic
    return -1 * heuristic

# Heuristic that discourages to move on edges. Give one additional point if not on edges. Got the idea from the research paper from Erik Van Der Werf- AI Techniques for the game GO in reference of HW 2.
def weigh_edge(q,w):
    # Tests if it is on edge of the board.  
    if 0 < q < 4 and 0 < w < 4:
        # If not then award one point.
        edge_pow=1
    else:
        # If it is then no penalty.
        edge_pow=0
    return edge_pow



# Calls itself recursively.
def ab_MIN_max(latest_board, opp_turn_col, alph, bet, est_hr, last_board, depth):
    latest_board_duplicate = copy.deepcopy(latest_board)
    # Check depth doesnt get altered as it sets base case.
    check_dep=depth
    #played_state = copy.deepcopy(latest_board)
    condition2=1
    # If the depth is 0, then the heuristic calculation ends and send the heuristic value back.
    if check_dep == 0:
        return est_hr
    # Initialising, to count and check pruned nodes
    condition3=1
    # Setting in new variable so that we can update it in pruining stage
    tillnow_bestmv = est_hr
    # Find all the legit moves 
    legit_moves2=find_legit_moves(last_board, latest_board, opp_turn_col)
    len(legit_moves2)
    run_count=0
    # Iterate all the legit moves one by one
    for action in legit_moves2:
        run_count=+1
        # Create a copy of the most updated version of the board.
        played_state = copy.deepcopy(latest_board)
        #print(len(played_state))
        #print(run_count)
        # Played a legit move in played state array.
        played_state[action[0]][action[1]] = opp_turn_col
        # Remove the dead stones of the opponent after playing a turn in a legit coordinate.
        rev_player3= 3 - opp_turn_col
        played_state = remove_dead_counter(played_state, rev_player3)
        # Created a copy of played_state for the ability to compare later.
        newest_state = copy.deepcopy(played_state)
        len(newest_state)
        #print(newest_state)
        # Calculate heuristic utilizing no of counters on board, liberty, edge score and and komi score.
        est_hr = estimated_hr(rev_player3, newest_state, latest_board_duplicate)
        # Recursively call ab_MIN_max to evaluate score heuristic till it reaches base case of 0.
        score_heur1 = -1 * ab_MIN_max(newest_state, rev_player3, alph, bet, est_hr, latest_board_duplicate, depth-1)
        
        # Comparing the new calculation is more than the best till now calculation
        if score_heur1 > tillnow_bestmv:
            # Verify which is coming out to be max. Decomplicate by putting max rather than checking.
            tillnow_bestmv = max(score_heur1,tillnow_bestmv)
        
        #Pruining for minimiser i.e. opponent
        if opp_turn_col == gl_opp_clr:
            #Revise beta if no pruining 
            if tillnow_bestmv > bet:
                bet = max(tillnow_bestmv,bet)
                
            # See if pruining is a possibiity
            if alph > (-1 * tillnow_bestmv):
                #Checks no of pruned nodes
                condition2=condition2+1
                return tillnow_bestmv
        
        #Pruining for maximiser i.e. us
        elif opp_turn_col == gl_clr:
            #Revise alpha if no pruining
            if tillnow_bestmv > alph:
                alph = max(tillnow_bestmv,alph)
                
            # See if pruining is a possibiity
            if bet > (-1 * tillnow_bestmv):
                #Checks no of pruned nodes
                condition3=condition3+1
                return tillnow_bestmv

    return tillnow_bestmv

# Minimax starts from this function.
def ab_min_MAX(latest_board,alph, bet, turn_of_player, last_board, depth):
    score_till_now = 0
    #alph = float('-inf')
    #bet = float('-inf')
    condition1=1
    best_action=[]
    #To calculate the number of legit moves or number of loops
    no_of_moves=1
    latest_board_duplicate = copy.deepcopy(latest_board)
    #played_state = copy.deepcopy(latest_board)
    legit_moves1=find_legit_moves(last_board, latest_board, turn_of_player)
    # If board empty, then starting as black has to be 2,2 condition can add here
    if len(legit_moves1)==25:
        # Best possible move for black color
        return [(2,2)]
    for action in legit_moves1:
        played_state = copy.deepcopy(latest_board)
        # Played a legit move in played state array.
        played_state[action[0]][action[1]] = turn_of_player
        # Remove the dead stones of the opponent after playing a turn in a legit coordinate.
        no_of_moves=no_of_moves+1
        rev_player2= 3 - turn_of_player
        #print(no_of_moves)
        played_state = remove_dead_counter(played_state, rev_player2)
        # Created a copy of played_state for the ability to compare later.
        newest_state = copy.deepcopy(played_state)
        # Majority of the assignment is done till here just complete alpha beta.
        
        # Calculate heuristic utilizing no of counters on board, liberty, edge score and komi score.
        est_hr = estimated_hr(rev_player2, newest_state, latest_board_duplicate)
        len(newest_state)
        arr_action=[action]
        #print(est_hr)
        # Recursively call ab_MIN_max to evaluate score heuristic
        score_heur = -1 * ab_MIN_max(newest_state,rev_player2, alph, bet, est_hr, latest_board_duplicate,depth)
        # To figure out if we have a better move.
        if (not best_action) or score_heur > score_till_now:
            condition1=condition1+1
            score_till_now = score_heur
            # update action
            best_action = arr_action
            # Update alpha
            alph = score_till_now
        
        # If some other move then just append  
        elif score_heur == score_till_now:
            condition1=condition1-1
            best_action.append(action)
    
    return best_action


# Fetches a good move by using ab minimax from the valid moves.
def fetch_good_move(last_board, latest_board, turn_of_player):
    # Set global variables for minimax
    alph = float('-inf')
    bet = float('-inf')
    # Try different depths if sufficient time.
    depth=2
    # Depth 4 is exceeding 3.5 sec. So, finalised 2.
    best_action=ab_min_MAX(latest_board,alph, bet, turn_of_player, last_board, depth)
    #print(best_action)
    
    return best_action

# Declaring some global variables
output_loc='output.txt'
prw=""
counter_rmv=0

# Get Input
last_board, latest_board, turn_of_player=get_input()

# Globally set color for checking condition in alpha beta 
gl_clr=turn_of_player
gl_opp_clr=3-gl_clr

# Get a move
play_move=fetch_good_move(last_board, latest_board, turn_of_player)
#print(len(play_move))

# Write output file here. Referenced from write.py from vocareum 
with open(output_loc, 'w') as write_fl:
    if len(play_move)==0:
        # Play pass move
        write_fl.write("PASS")
        
    else:
        final_move=play_move[0]
        # Take out first move from the list and write it in output.
        loc_ele1=str(final_move[0])
        loc_ele2=str(final_move[1])
        write_fl.write(loc_ele1+","+loc_ele2)