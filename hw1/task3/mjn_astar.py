# task 2 ai hw matt nemeth

import sys
from copy  import deepcopy
from queue import PriorityQueue
from re    import search

class State:
    def __init__(self, id: str, parentid: str, board_copy: list, gn: int, hn: int):
        self.id =         id
        self.parentid =   parentid
        self.board_copy = board_copy
        self.fn = gn + hn
        self.gn = gn
        self.hn = hn

    def __lt__(self, other):
        return self.id < other.id

def parse_input(arg1: str, arg2: str) -> list:
    startState = search(r"\[([0-9,]+)]", arg1).group(1).split(',')
    goalState =  search(r"\[([0-9,]+)]", arg2).group(1).split(',')
    return [startState, goalState, len(goalState)]

def swapPos(list: list, empty_block: int, offset: int):
    #Swap positions of elements in a list
    pos2 = empty_block + offset
    list[empty_block], list[pos2] = list[pos2], list[empty_block]

def getLvl(currState: State) -> int:
    return int(currState.id.split('_')[0])

def getLvlID(currState: State) -> int:
    return int(currState.id.split('_')[1])

def addOpenLst(openLst: PriorityQueue, expandedBrds: list, index: int):
    for i in range(len(openLst.queue)):
        if openLst.queue[i][index][0].board_copy not in expandedBrds:
            expandedBrds.append(openLst.queue[i][index][0].board_copy)

def printState(closedLst: list, index: int, isastar: bool):
    if index == 0:
        print("Root")
    elif index > 0 and closedLst[index][0].parentid != closedLst[index - 1][0].parentid:
        print("Parent ID: " + closedLst[index][0].parentid)

    print("State ID: " + closedLst[index][0].id)
    print("Board State: " + "[" + ', '.join(closedLst[index][0].board_copy) + "]")
    print("Movement: " + closedLst[index][1])

    if isastar:
        print("g(n) = " + str(closedLst[index][0].gn))
        print("h(n) = " + str(closedLst[index][0].hn))
        print("f(n) = " + str(closedLst[index][0].fn) + '\n')

def printOutput(closedLst: list, expandedBrds: list, isastar: bool):
    #print entire path from start state to goal state
    print("Path: ")
    for i in range(len(closedLst)):
        printLvl(closedLst, i)
        printState(closedLst, i, isastar)

    #print number of nodes visited
    print("\nTotal number of nodes")
    print("Open list: " + str(len(expandedBrds)))
    print("Closed list: " + str(len(closedLst)))

def expand_all(currState: State, goalState: list, brdLen: int, expandedBrds: list, isastar: bool, h_type: int = 1) -> list:
    #expand states underneath current state and return them in a list
    #initialize board copies and variables
    empty_block = currState.board_copy.index('0')
    right_board = currState.board_copy.copy()
    left_board =  currState.board_copy.copy()
    up_board =    currState.board_copy.copy()
    down_board =  currState.board_copy.copy()
    currLvl = getLvl(currState) + 1
    id = 0
    hn = 0
    gn = 0
    expansions = []

    # go left
    if empty_block % 3 != 0:
        swap_index = -1
        swapPos(left_board, empty_block, swap_index)
        if left_board not in expandedBrds:
            if isastar:
                hn = getHN(left_board, goalState, brdLen, h_type)
                gn = getGN(currState, empty_block, swap_index)
            left_state = State(str(currLvl) + '_' + str(id), currState.id, left_board, gn, hn)
            expansions.append((left_state, "Left"))
            id += 1
    # go up
    if empty_block > 2:
        swap_index = -3
        swapPos(up_board, empty_block, swap_index)
        if up_board not in expandedBrds:
            if isastar:
                hn = getHN(up_board, goalState, brdLen, h_type)
                gn = getGN(currState, empty_block, swap_index)
            up_state = State(str(currLvl) + '_' + str(id), currState.id, up_board, gn, hn)
            expansions.append((up_state, "Up"))
            id += 1
    # go right
    if empty_block % 3 != 2:
        swap_index = 1
        swapPos(right_board, empty_block, swap_index)
        if right_board not in expandedBrds:
            if isastar:
                hn = getHN(right_board, goalState, brdLen, h_type)
                gn = getGN(currState, empty_block, swap_index)
            right_state = State(str(currLvl) + '_' + str(id), currState.id, right_board, gn, hn)
            expansions.append((right_state, "Right"))
            id += 1
    # go down
    if empty_block < brdLen - 3:
        swap_index = 3
        swapPos(down_board, empty_block, swap_index)
        if down_board not in expandedBrds:
            if isastar:
                hn = getHN(down_board, goalState, brdLen, h_type)
                gn = getGN(currState, empty_block, swap_index)
            down_state = State(str(currLvl) + '_' + str(id), currState.id, down_board, gn, hn)
            expansions.append((down_state, "Down"))
    return expansions

def getHN(targetState: list, goalState: list, brdLen: int, h_type: int) -> int:
    heuristic = 0
    for i in range(brdLen):
        if targetState[i] != goalState[i]:
            if h_type == 1:
                heuristic += 1
            else:
                goal_offset = abs(i - goalState.index(targetState[i]))
                while goal_offset % 3 != 0:
                    heuristic += 1
                    goal_offset -= 1
                while goal_offset > 1:
                    heuristic += 1
                    goal_offset /= 3
    return heuristic

def getGN(currState: State, empty_block: int, offset: int) -> int:
    swap_val = int(currState.board_copy[empty_block + offset])
    gn = currState.gn

    if swap_val < 6:
        gn += 1
    elif swap_val < 16:
        gn += 3
    else:
        gn += 5
    return gn

def printLvl(closedLst: list, index: int):
    currLvl = getLvl(closedLst[index][0])
    prevLvl = getLvl(closedLst[index - 1][0])

    if index == 0 or currLvl - prevLvl != 0:
        print("Level: " + str(currLvl)+'\n')

def astar(openLst: PriorityQueue, closedLst: list, currState: State, goalState: list, brdLen: int, expandedBrds: list, h_type: int) -> bool:
    #if our level is bigger than 30 end the search.
    level = getLvl(currState)
    if level > 30:
        return False

    addOpenLst(openLst, expandedBrds, 3)
    expansions = expand_all(currState, goalState, brdLen, expandedBrds, True, h_type)
    closedLst.append(openLst.get()[3])
    
    for i in range(len(expansions)):
        openLst.put((expansions[i][0].fn, getLvl(expansions[i][0]), getLvlID(expansions[i][0]), deepcopy(expansions[i])))
    if closedLst[-1][0].board_copy == goalState:
        return True
    currState = openLst.queue[0][3][0]
    #call recursively until we hit goal state or too many levels
    return astar(openLst, closedLst, currState, goalState, brdLen, expandedBrds, h_type)


def astarWrap(h_type: int, arg1: str, arg2: str):
    inputLst =     parse_input(arg1, arg2)
    startState =   inputLst[0]
    goalState =    inputLst[1]
    brdLen =       inputLst[2]
    closedLst =    []
    expandedBrds = []

    # check to make sure we are not at the goal state already
    if startState != goalState:
        h = getHN(startState, goalState, brdLen, h_type)
        currState = State("0_0", "", startState, 0, h)
        #initialize priority queue
        openLst = PriorityQueue()
        openLst.put((currState.fn, getLvl(currState), getLvlID(currState), deepcopy((currState, "Start"))))

        if astar(openLst, closedLst, currState, goalState, brdLen, expandedBrds, h_type):
            print("Goal state was found.\n")
        else:
            print("After 30 levels, no solution was found. Ending search...\n")
        printOutput(closedLst, expandedBrds, True)
    else:
        print("Start state = Goal state. No search to be done.")

if __name__ == "__main__":
    astarWrap(2, sys.argv[1], sys.argv[2])
