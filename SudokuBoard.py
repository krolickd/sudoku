import numpy
class SudokuBoard:
    def __init__(self):
        #known values
        self.board = []
        #possible values
        self.options = {}

    def load_board(self, number_matrix):
        self.board = number_matrix

    def remaining_spaces(self):
        # return total unfilled squares
        total = 0
        for row in self.board:

            total += row.count(0)
        return total


    def get_quad_range(self, val):
        # return quadrant indices based on position
        if val <= 2:
            return (0, 1, 2)
        elif val <= 5:
            return (3, 4, 5)
        else:
            return (6, 7, 8)

    def get_unused_vals(self, row, col):
        #for an empty square
        # return set of unused values based on populated values in relatives (row,column,quadrant)
        all_vals = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        # return all populated values in the row
        row_used_vals = set(self.board[row])

        # return all populated values in the column
        col_used_vals = set(row[col] for row in self.board)

        # return all populated values in the 3x3 quadrant
        quad_used_vals = set()

        for y in self.get_quad_range(row):
            for x in self.get_quad_range(col):
                quad_used_vals.add(self.board[y][x])


        remaining_vals = all_vals - row_used_vals - col_used_vals - quad_used_vals

        remaining_vals.discard(0)

        return list(remaining_vals)
    
    def get_row_relatives(self,target_key):
        # return list of unpopulated row relatives
        relative_list = []
        row = target_key[0]

        for key in self.options.keys():
            if row == key[0] and key != target_key:
                relative_list.append(key)

        return relative_list

    def get_col_relatives(self,target_key):
        # return list of unpopulated column relatives
        relative_list = []
        col = target_key[1]

        for key in self.options.keys():
            if col == key[1] and key != target_key:
                relative_list.append(key)

        return relative_list


    def get_quad_relatives(self,target_key):
        # return list of unpopulated quadrant relatives

        row = target_key[0]
        col = target_key[1]
        quad_keys = []

        for y in self.get_quad_range(int(row)):
            for x in self.get_quad_range(int(col)):
                quad_keys.append(str(y) + str(x))

        relative_list = []

        for key in self.options.keys():
            if key in quad_keys and key != target_key:
                relative_list.append(key)

        return relative_list

    def is_unique_in_relatives(self,val,target_key):
        # check if value is unique within an individual relative type
        
        #check row
        for rel_key in self.get_row_relatives(target_key):
            if val  in self.options[rel_key]:
                break
        else:
            return True

        #check col
        for rel_key in self.get_col_relatives(target_key):
            if val  in self.options[rel_key]:
                break
        else:
            return True

        #check quadrant
        for rel_key in self.get_quad_relatives(target_key):
            if val  in self.options[rel_key]:
                break
        else:
            return True

        return False


    def solve(self):
        improvement = 1
        trip = 1

        # evaluate until no improvement
        while improvement > 0:
            improvement = 0

            print(f'\nTrip {trip}')

            # traverse populated board
            for y in range(9):
                for x in range(9):
                    val = self.board[y][x]

                    # find possible values for empty space
                    if val == 0:
                        possibilities = self.get_unused_vals(y, x)
                        print(f"{y},{x}: {possibilities}")

                        # update board if only one possible value
                        if len(possibilities) == 1:
                            self.board[y][x] = int(possibilities[0])
                            if str(y)+str(x) in self.options.keys():
                                self.options.pop(str(y)+str(x))
                            improvement += 1
                        else:
                            #update options list with possibilities
                            self.options[str(y)+str(x)] = possibilities
            
            #evaluate possibilities once populated
            if improvement == 0:
                #check for unique values in unpopulated relatives
                pop_list = []
                for key in self.options.keys():
                    for val in self.options[key]:
                        if self.is_unique_in_relatives(val,key):
                            self.board[int(key[0])][int(key[1])] = int(val)
                            pop_list.append(key)
                            improvement += 1
                            break
                [self.options.pop(k) for k in pop_list]
            
            trip += 1

        # relation based evaluation
        # implement backtracking for puzzles where there are squares with more than one possible value

    def is_board_valid(self):
        all_vals = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

        #rows
        for row in self.board:
            if all_vals != set(row):
                return False

        # columns
        for col in range(9):
            if all_vals != set([row[col] for row in self.board]):
                return False
        grid = numpy.array(self.board)
        
        #quadrants
        for y in range(0,9,3):
            for x in range(0,9,3):
                quad_vals = set()
                quad = grid[y:y+3,x:x+3]

                for x in quad:
                    quad_vals.update(x)
                
                if all_vals != quad_vals:
                    return False

        return True


    def print_board(self):
        # print board to console
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
                print('-----|-----|-----', end='')

            y_count += 1

        print()
