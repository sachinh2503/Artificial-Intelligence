from copy import copy, deepcopy
import collections
import time


class Grid:

    def __init__(self):
        self.dict = {}
        self.scooter_initial_pos = []
        self.final_value = 0
        self.max_value = 0
        self.grid_size = 0
        self.num_police = 0
        self.num_scooters = 0
        self.grid = []
        self.track_grid = []
        self.prev_value = 0
        self.grid_list = []
        self.main_dict = {}
        self.main_dict2 = {}
        self.max_sum = []

    def myfunc(self, file_name):
        input_file = open(file_name, "r")
        output_file = open("output.txt", "w")

        i = 1
        scooter_coord = []
        for x in input_file:
            x = x.rstrip('\n\r')
            if i == 1:
                self.grid_size = int(x)
            elif i == 2:
                self.num_police = int(x)
            elif i == 3:
                self.num_scooters = int(x)
            else:
                y = x.strip("\n\r")
                scooter_coord.append(y)
                if y in self.dict.keys():
                    self.dict[y] += 1
                else:
                    self.dict[y] = 1
            i += 1

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                temp = str(i) + "," + str(j)
                if temp in self.dict:
                    continue
                else:
                    self.dict[temp] = 0

        if self.grid_size == self.num_police:
            valid_cols = {i for i in range(self.grid_size)}
            tracking = [-1 for i in range(self.grid_size)]

            self.compute_for_equalpolice_as_gridsize(self.grid_size, tracking, 0, valid_cols)

            max = 0
            for i in range(len(self.max_sum)):
                c = 0
                sum = 0
                for j in self.max_sum[i]:
                    temp = str(c) + "," + str(j)
                    sum += self.dict[temp]
                    c += 1
                if sum > max:
                    max = sum
            #print("Answer", max)
            output_file.write(str(max))
        else:
            #track = [[0 for x in self.grid_size] for y in self.grid_size]
            a = self.recur_func(self.dict, self.num_police)
            #print("Answer", a)
            output_file.write(str(a))

        input_file.close()
        output_file.close()

    def calc_valid(self, position):
        police_pos = []
        police_pos.append(position)
        # for t in range(grid_size * grid_size):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                temp = police_pos[0].split(",")
                if str(i) == temp[0] or str(j) == temp[1] or (abs(i - int(temp[0])) == abs(j - int(temp[1]))):
                    continue
                else:
                    val = str(i) + "," + str(j)
                    police_pos.append(val)

        police_pos.pop(0)
        #print(police_pos)
        return police_pos

    def recur_func(self, d, num_police):
        if num_police == 0:
            return 0

        if not bool(d) and num_police != 0:
            return 0

        for item in d.keys():
            inv_i = int(item.split(",")[0])
            inv_j = int(item.split(",")[1])

            taken = copy(d)
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if i == inv_i or j == inv_j or i + j == inv_i + inv_j or i - j == inv_i - inv_j:
                        temp = str(i) + "," + str(j)
                        if temp in taken:
                            del taken[temp]
                    else:
                        continue
            not_taken = copy(d)
            del not_taken[item]

            return max(self.recur_func(not_taken, num_police), self.recur_func(taken, num_police - 1) + d[item])

    def compute_for_equalpolice_as_gridsize(self, grid_size, tracking, row_number, cols):
        if row_number == grid_size:
            combinations = []
            i = 0
            while i < grid_size:
                x = ["." for m in range(grid_size)]
                for j in range(grid_size):
                    if tracking[i] == j:
                        x[j] = "-"
                combinations.append(x.index("-"))
                i += 1
            self.max_sum.append(combinations)
            return

        for not_row in range(grid_size):
            valid = True
            if ((not_row > tracking[row_number - 1] + 1) or (row_number == 0) or (not_row < tracking[row_number - 1] - 1)) and (not_row in cols):
                if row_number > 0:
                    for m in range(row_number - 1):
                        if abs(not_row - tracking[m]) == (row_number - m):
                            valid = False
                            break
            else:
                valid = False

            if valid:
                tracking[row_number] = not_row
                cols.remove(not_row)
                self.compute_for_equalpolice_as_gridsize(
                    grid_size, tracking, row_number + 1, cols)
                cols.add(not_row)


g1 = Grid()
#start_time = time.time()
g1.myfunc("input.txt")
#print("--- %s seconds ---" % (time.time() - start_time))
