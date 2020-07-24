import random
# we need a matrix of 4 X 4. There will be multiples of 2

#initialise the matrix with 0. 0 means it is an empty position.

# This function will be called whenever we start the game. It will create a matrix of 4 X 4 and initialise it with 0
def start_game():
    matrix = []
    for i in range(4):
        matrix.append([0] * 4)  # this will make a matrix as [[0000],[0000],[0000],[0000]]
    return matrix



#we will add new 2 in the matrix
def add_new_two(matrix):
    # we need a random integer from 0 to 3 for row and again random integer from 0 to 3 for column to get the location.
    #Now, if there is 0 present at this position or not. If yes, then generate 2 here.
    # we will generate a random value for row and for column each using random module in python
    
    row = random.randint(0, 3)
    col = random.randint(0, 3)
    
    #we will keep on generating new location untill we dont get an empty location
    while(matrix[row][col] != 0):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        
    matrix[row][col] = 2


def compress(matrix):
    # make a new matrix
    changed = False
    new_matrix = []
    for i in range(4):
        new_matrix.append([0]*4)
        
    for row in range(4):
        # at each row, this will intially be 0, and we will increment it by one once we have an element in the next_position col.
        next_position = 0
        for col in range(4):
            if(matrix[row][col] != 0):
                new_matrix[row][next_position] = matrix[row][col]
                next_position += 1 
                changed = True
                
    return new_matrix, changed


def merge(matrix):
    
    #LEFT MOVEMENT
    changed = False
    for row in range(4):
        for col in range(3):
            # we just have to compare first col with second, second with third, third with fourth.
            if(matrix[row][col] == matrix[row][col + 1] and matrix[row][col] != 0): # the value is equal and not zero
                matrix[row][col] = matrix[row][col] * 2
                matrix[row][col + 1] = 0
                changed = True
                
    return matrix, changed



# Current state of the game.
    # Won
    #lost
    #game not over.
    
# At current state, we will be given a matrix and we have to check what is our current state.


# 1. Won state is easy, if at any position the value is 2048, we have won.
def get_current_state(matrix):
    # won
    for row in range(0, 4):
        for col in range(0, 4):
            if(matrix[row][col] == 2048):
                return 'WON'
            
    
#If there is an empty place, i.e., we have 0 present at any place, then it means that we are still in the game, the game is not over
    for row in range(4):
        for col in range(4):
            if(matrix[row][col] == 0):
                return 'GAME NOT OVER'

#FOR EVERY ROW AND COLUMN EXCEPT LAST ROW AND LAST COLUMN
            
# if at some consecutive boxes, we have equal numbers, then we are still in the game.
    for row in range(0, 3): #we are checking only for the first three rows and first three columns, not for last row and last column
        # because that can go out of bound by adding 1.
        for col in range(0, 3):
            if(matrix[row][col] == matrix[row + 1][col] or matrix[row][col] == matrix[row][col + 1]):
                return 'GAME NOT OVER'
            
    # LAST ROW. -> row is fixed here, we are checking only in last row.
    for col in range(0, 3):
        if(matrix[3][col] == matrix[3][col + 1]):
            return 'GAME NOT OVER'
    
    #LAST COLUMN -> column is fixed here as last col and rows are varying
    for row in range(0, 3):
        if(matrix[row][3] == matrix[row + 1][3]):
            return 'GAME NOT OVER'
        
    return 'LOST' # we dont have any empty position, no 2048 anywhere, cannot move anywhere.






# REVERSING A MATRIX AND TRANSPOSING A MATRIX

#REVERSING -> 
# [2,4,2,0,
# 0,4,4,2,
# 2,2,4,4
# 4,2,4,2] BECOMES
# [0,2,4,2,
# 2,4,4,0,
# 4,4,2,2,
# 2,4,2,4]

def reverse(matrix):
    new_matrix = []
    for row in range(4):
        new_matrix.append([])
        for col in range(4):
            new_matrix[row].append(matrix[row][4 - col - 1])
            
    return new_matrix


# TRANSPOSE A MATRIX
def transpose(matrix):
    new_matrix = []
    for row in range(4):
        new_matrix.append([])
        for col in range(4):
            new_matrix[row].append(matrix[col][row])  #in transpose, (i,j)th element becomes (j,i)th element.
            
    return new_matrix

# All possible moves in 2048 -> L, R, U, D

# 1. LEFT
    # a. Compress b. Merge c. Compress
# 2. RIGHT
    # a. Reverse b. Compress (Same as left traverse) c. Merge d. Compress e. Reverse
    
# 3. UP MOVEMENT
    #either we can build a logic for ith column and i+1th column or we can use left traverse only by using transpose.
    
    # a. Transpose b. Compess c. Merge d. Compress e. Transpose
    
# 4. DOWN MOVEMENT
    # a. Transpose b. Reverse c. Compress d. Merge e. Compress f. Reverse g. Transpose
    
    
def move_left(grid):
    # we have to check if there was some change or not in the state of the array. If yes, then we'll add new two, else, we'll not add it.
    
    new_grid, changed1 = compress(grid)
    new_grid, changed2 = merge(new_grid)
    changed = changed1 or changed2 # all the movement, whether happened or not, depends on compress and merge
    new_grid, temp = compress(new_grid) # this compress will only execute when above merge is executed.
    
    return new_grid, changed

def move_right(grid):
    reversed_grid = reverse(grid)
    new_grid, changed1 = compress(reversed_grid)
    new_grid, changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid, temp = compress(new_grid)
    final_grid = reverse(new_grid)
    return final_grid, changed

def move_up(grid):
    transposed_grid = transpose(grid)
    new_grid, changed1 = compress(transposed_grid)
    new_grid, changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid, temp = compress(new_grid)
    final_grid = transpose(new_grid)
    return final_grid, changed

def move_down(grid):
    transposed_grid = transpose(grid)
    reversed_grid = reverse(transposed_grid)
    new_grid, changed1 = compress(reversed_grid)
    new_grid, changed2 = merge(new_grid)
    changed = changed1 or changed2
    new_grid, temp = compress(new_grid)
    final_reversed_grid = reverse(new_grid)
    final_grid = transpose(final_reversed_grid)
    return final_grid, changed


