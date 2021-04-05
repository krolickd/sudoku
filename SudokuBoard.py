class SudokuBoard:
    def __init__(self):
        self.board = []

    def load_board(self,number_matrix):
        self.board = number_matrix
    
    def remaining_spaces(self):
        #return total unfilled squares
        total = 0
        for row in self.board:
            
            total += row.count(0)
        return total
    
    def get_row_numbers(self,row):
        #return all populated values in the row
        return set(self.board[row])

    def get_col_numbers(self,col):
        #return all populated values in the column
        return set(row[col] for row in self.board)
    
    def get_quad_numbers(self,row,col):
        #return all populated values in the 3x3 quadrant
        quad = set()
        
        for y in self.get_quad_range(row):
            for x in self.get_quad_range(col):
                quad.add(self.board[y][x])
        
        return quad

    def get_quad_range(self,val):
        #return quadrant indices based on position
        if val <= 2:
            return (0,1,2)
        elif val <= 5:
            return (3,4,5)
        else:
            return (6,7,8)
    
    def get_possible_numbers(self, row,col):
        #return set of possible values based on row,column, quadrant constraints
        total = {0,1,2,3,4,5,6,7,8,9}

        total = total - self.get_row_numbers(row) - self.get_col_numbers(col) - self.get_quad_numbers(row,col)

        total.discard(0)

        return total
    
    
    def solve(self):
        improvement = 1
        trip = 1

        #square based evaluation
        while improvement > 0:
            improvement = 0

            print(f'\nTrip {trip}')
            
            #traverse board
            for y in range(9):
                for x in range(9):
                    val = self.board[y][x]

                    #find possible vaues for empty space
                    if val == 0:
                        possibilities = self.get_possible_numbers(y,x)
                        print(f"{y},{x}: {possibilities}")
                        
                        #update board if only one possible value
                        if len(possibilities) == 1:
                            self.board[y][x] = int(possibilities.pop())
                            improvement += 1
            trip += 1
                    
        #NO IMPROVEMENT
        #relation based evaluation
        #implement backtracking for puzzles where there are squares with more than one possible value


    def print_board(self):
        #print board to console
        y_count = 0

        for row in self.board:
            print()
            x_count = 0
            for num in row:
                output = ''
                if num == 0:
                    output += '.'
                else:
                    output += str(num)
                
                if x_count == 2 or x_count == 5:
                    output += '|'
                else:
                    output += ' '

                print(output, end='')

                x_count += 1
            
            if y_count == 2 or y_count == 5:
                print()
                print('-----|-----|-----',end='')
            
            y_count +=1
                
        print()
    