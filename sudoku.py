
import time
def puzzle_load():
    global board
    print ("Choose a puzzle:") #input to choose a puzzle
    print("1. Puzzle 1")
    print("2. Puzzle 2")
    print("3. Puzzle 3")
    choice = input("Enter your choice (1-3): ")
    if choice == "1":
        filename = "puzzle1.txt"
    elif choice == "2":
        filename = "puzzle2.txt"
    elif choice == "3":
        filename = "puzzle3.txt"
    else:
        print("error: choose a valid puzzle (1-3)")
        return False
    try: 
        with open (filename, "r") as file: 
            lines = file.readlines()
        if len(lines)!=9: 
            print("error: puzzle must have 9 rows")
            return False
        newboard=[]

        for line in lines: 
            line = line.strip()#removes the witespace from the beginning and end of the line
            parts = line.split()#cuts the line into parts based on whitespace
            if len(parts)!=9:
                print("error: each row must contain 9 values (0-9) separated by spaces")
                return False
            row=[]
            for digit in parts:
                if not digit.isdigit() or int(digit) < 0 or int(digit) > 9:
                    print("error: each value must be a digit between 0 and 9")#checks condition if the digit is not a digit or less than 0 or greater than 9
                    return False
                row.append(int(digit))
            newboard.append(row)
        board = newboard
        print("puzzle loaded successfully")
        return True
    except FileNotFoundError:
        print("error: file not found")
        return False

#display
def displayBoard():
    for i in range (9):
        for j in range (9):
            print(board[i][j], end = "")
            if (j+1)%3 ==0 and j!=8:
                print("|", end= "")
        print()
        if (i+1)%3==0 and i != 8:
            print("-"*21)

#sudoku-logic (to find the empty cells)
def findEmpty():
    for i in range(9):
        for j in range (9):
            if board[i][j]==0: #if row and column is 0 (empty)
                return i, j
    return None 
#constraints
def isvalid(num, row, col):

    for j in range(9):
        if board[row][j] == num: #for row
            return False
    for i in range(9):
        if board[i][col] == num: #for column
            return False
    #checks the 3 x 3 grid 
    box_row = (row//3)*3 
    box_col = (col//3)*3

    for i in range(box_row, box_row + 3):
        for j in range (box_col, box_col+3):
            if board[i][j]==num: 
                return False

    return True
search_steps = 0
backtracks = 0 
execution_time = 0
#-----------------------------------------------------------------
#                    puzzle solve
#-----------------------------------------------------------------
def solve():
    global search_steps, backtracks
    empty= findEmpty() #to find empty cell
    if empty is None: #if there is no empty cell left
        return True #cell solved

    row, col = empty #get cell position
    for  num in range (1, 10):
        search_steps +=1 #search counter
        if isvalid(num, row, col): #constraints
            board[row][col]=num
            if solve():
                return True
            backtracks +=1 #backtrack counter
            board[row][col]=0 #resets to undo
    return False
#-----------------------------------------------------------
#                               menu 
#-----------------------------------------------------------
puzzle_loaded = False
puzzle_solved = False 
solve_attempted = False
ogboard = None
board=[]

def menu():
    global puzzle_loaded, puzzle_solved, solve_attempted
    global search_steps, backtracks, board, ogboard, execution_time
    while True: 
        print("\n======= SUDOKU SOLVER =======")
        print ("1. Load puzzle")
        print ("2. Display puzzle")
        print ("3. Solve puzzle")
        print ("4. Display search statistics")
        print ("5. Exit")

        op = input ("Enter your option: ")

        if op == "1":
            if puzzle_load():
                ogboard = []
                for i in range(9):
                    row = []
                    for j in range(9):
                        row.append(board[i][j])
                    ogboard.append(row)
                puzzle_loaded = True
                puzzle_solved = False
                solve_attempted = False
                search_steps = 0
                backtracks = 0
                execution_time = 0
                time.sleep(1)
             
        elif op == "2":
            if not puzzle_loaded: print ("error: load the puzzle first")
            else: displayBoard()
            time.sleep(1)
        elif op == "3":
            if not puzzle_loaded: print ("error: load the puzzle first")
            else: 
                board=[]
                for i in range(9):
                    row = []
                    for j in range(9):
                        row.append(ogboard[i][j])
                    board.append(row)

                search_steps = 0
                backtracks = 0
                solve_attempted = True

                start_timer = time.perf_counter()
                result = solve()
                end_timer = time.perf_counter()
                execution_time = end_timer - start_timer

                if result:
                    puzzle_solved = True
                    print ("Solved successfully")
                    displayBoard()
                else: 
                    puzzle_solved = False
                    print("No solution found")
                time.sleep(1)
        elif op == "4":
            if not puzzle_loaded: print ("error: load the puzzle first")
            elif not solve_attempted: print("error: solve the puzzle first")
            else:
                print("Sudoku Statistics: ")
                print("search steps: ", search_steps)
                print("backtracks: ", backtracks)
                print("puzzle solved: ", puzzle_solved)
                print(f"execution time: {execution_time:.2f} seconds")
                time.sleep(1)

        elif op == "5":
            print ("Exiting Sudoku Solver.")
            break
        else: print("Invalid choice. Please enter 1 to 5")
menu()
                
