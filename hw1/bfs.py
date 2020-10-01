#Matt Nemeth AI HW Task 1

import sys
from re    import search
from copy  import deepcopy
from queue import PriorityQueue

class State:
    def __init__(self, id, pid, cbrd, gn, hn):
        self.id =   id
        self.pid =  pid
        self.cbrd = cbrd
        self.gn =   gn
        self.hn =   hn
        self.fn =   gn + hn

    def __lt__(self, other):
        return self.id < other.id

def parse_input() -> list:
    start_state_brd = search(r"\[([0-9,]+)]", sys.argv[1]).group(1).split(',')
    goalState = search(r"\[([0-9,]+)]", sys.argv[2]).group(1).split(',')
    return [start_state_brd, goalState, len(goalState)]

def swap_positions(list: list, empty_block: int, offset: int):
    pos2 = empty_block + offset
    list[empty_block], list[pos2] = list[pos2], list[empty_block]

def expand_all(currState: State, goalState: list, board_length: int, expanded_boards: list) -> list:
    # Initialize empty block and possible board movements
    empty_block = currState.cbrd.index('0')
    left_board =  currState.cbrd.copy()
    right_board = currState.cbrd.copy()
    up_board =    currState.cbrd.copy()
    down_board =  currState.cbrd.copy()

    # Initialize current level and ID for specific state for level
    currLvl = get_level(currState) + 1
    id = 0

    # Initialize empty list of all expansion possibilities
    expansions = []

    # Move left
    if empty_block % 3 != 0:
        swap_positions(left_board, empty_block, -1)

        if left_board not in expanded_boards:
            lh = get_heuristic(left_board, goalState, board_length)
            left_state = State(str(currLvl) + '_' + str(id), currState.id, left_board, 0, lh)
            expansions.append((left_state, "Left"))
            id += 1

    # Move up
    if empty_block > 2:
        swap_positions(up_board, empty_block, -3)

        if up_board not in expanded_boards:
            uh = get_heuristic(up_board, goalState, board_length)
            up_state = State(str(currLvl) + '_' + str(id), currState.id, up_board, 0, uh)
            expansions.append((up_state, "Up"))
            id += 1

    # Move right
    if empty_block % 3 != 2:
        swap_positions(right_board, empty_block, 1)

        if right_board not in expanded_boards:
            rh = get_heuristic(right_board, goalState, board_length)
            right_state = State(str(currLvl) + '_' + str(id), currState.id, right_board, 0, rh)
            expansions.append((right_state, "Right"))
            id += 1

    # Move down
    if empty_block < board_length - 3:
        swap_positions(down_board, empty_block, 3)

        if down_board not in expanded_boards:
            dh = get_heuristic(down_board, goalState, board_length)
            down_state = State(str(currLvl) + '_' + str(id), currState.id, down_board, 0, dh)
            expansions.append((down_state, "Down"))
    return expansions

def get_heuristic(targetState: list, goalState: list, board_length: int) -> int:
    count = 0
    for i in range(board_length):
        if targetState[i] != goalState[i]:
            count += 1
    return count

def get_level(currState: State) -> int: #returns current level
    return int(currState.id.split('_')[0])

def get_id_on_level(currState: State) -> int: #returns id on level
    return int(currState.id.split('_')[1])

def print_level(closedLst: list, index: int): #print current level
    currLvl = get_level(closedLst[index][0])
    prevLvl = get_level(closedLst[index - 1][0])
    if index == 0 or currLvl - prevLvl != 0:
        print("Level: " + str(currLvl)+"\n")

def add_openLst_to_expanded(openLst: PriorityQueue, expandedBrds: list):
    for i in range(len(openLst.queue)):
        if openLst.queue[i][2][0].cbrd not in expandedBrds:
            expandedBrds.append(openLst.queue[i][2][0].cbrd)

def print_state_detailed_output(closedLst: list, index: int):
    if index == 0:
        print("Root")
    elif index > 0 and closedLst[index][0].pid != closedLst[index - 1][0].pid:
        print("Parent ID: " + closedLst[index][0].pid)

    print("State ID: " + closedLst[index][0].id)
    print("Board State: " + "[" + ', '.join(closedLst[index][0].cbrd) + "], Movement: " + closedLst[index][1] + "\n")

def bfs(openLst: PriorityQueue, closedLst: list, expand_state: State, goalState: list, brdLen: int, expandedBrds: list) -> bool:
    level = get_level(expand_state)

    if level > 30:
        return False

    expansions = expand_all(expand_state, goalState, brdLen, expandedBrds)

    for i in range(len(expansions)):
        openLst.put((level, get_id_on_level(expansions[i][0]), deepcopy(expansions[i])))

    add_openLst_to_expanded(openLst, expandedBrds)

    for i in range(len(openLst.queue)):
        closedLst.append(openLst.get()[2])
        if closedLst[-1][0].cbrd == goalState:
            return True

    next_expansion_index = [cl[0].cbrd for cl in closedLst].index(expand_state.cbrd) + 1
    expand_state = closedLst[next_expansion_index][0]

    return bfs(openLst, closedLst, expand_state, goalState, brdLen, expandedBrds)


if __name__ == "__main__":
    inList = parse_input()
    #inList = search_utils.parse_input()
    goalState =       inList[1]
    start_state_brd = inList[0]
    brdLen =          inList[2]

    #initialize empty lists for closed and expanded game boards
    closedLst =    []
    expandedBrds = []
    
    #check if start state is equal to goal state
    if start_state_brd != goalState:
        expand_state = State('0_0', None, start_state_brd, 0, 0)

        #create our priority queue
        openLst = PriorityQueue()
        openLst.put((get_level(expand_state), get_id_on_level(expand_state), deepcopy((expand_state, "Start"))))

        if bfs(openLst, closedLst, expand_state, goalState, brdLen, expandedBrds):
            print("Found the goal state.\n")
        else:
            print("After 30 levels, no solution was found. Ending search...\n")

        print("Path-")
        for i in range(len(closedLst)):
            print_level(closedLst, i)
            print_state_detailed_output(closedLst, i)

        print("\nTotal number of nodes\n" + "Open list: " + str(len(expandedBrds)) + "\nClosed list: " + str(len(closedLst)))
    else:
        print("Start state = Goal state. No moves made.")


