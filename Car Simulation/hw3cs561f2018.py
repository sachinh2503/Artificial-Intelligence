from copy import copy, deepcopy
import collections
import time
import numpy as np
import math

class Grid:

    def __init__(self):
        self.grid_size = 0
        self.num_cars = 0
        self.num_obstacles = 0
        self.obstacle_locations = []
        self.car_start_locations = []
        self.car_end_locations = []
        self.utility_matrix = []
        self.reward_matrix = []
        self.final_utility_matrix = []
        self.policy = []
        self.res = []
        self.val = 0
        self.reward_matrix_2 = []
        self.ans = []

    def myfunc(self, file_name):
        input_file = open(file_name, "r")
        output_file = open("output.txt", "w")

        i = 1
        temp_num_cars = 0
        temp_num_obstacles = 0
        for x in input_file:
            x = x.rstrip('\n\r')
            if i == 1:
                self.grid_size = int(x)
                i += 1
            elif i == 2:
                self.num_cars = int(x)
                temp_num_cars = int(x)
                i += 1
            elif i == 3:
                self.num_obstacles = int(x)
                temp_num_obstacles = int(x)
                i += 1
            elif i == 4:
                self.obstacle_locations.append(x)
                temp_num_obstacles -= 1
                if temp_num_obstacles == 0:
                    i += 1
                    continue
            elif i == 5:
                self.car_start_locations.append(x)
                temp_num_cars -= 1
                if temp_num_cars == 0:
                    i += 1
                    temp_num_cars = self.num_cars
                    continue
            elif i == 6:
                self.car_end_locations.append(x)
                temp_num_cars -= 1
                if temp_num_cars == 0:
                    i += 1
                    continue

        # print(self.grid_size)
        # print(self.num_cars)
        # print(self.num_obstacles)
        # print("CAR START LOC: ", self.car_start_locations)
        # print("CAR END LOC: ", self.car_end_locations)
        # print("OBSTACLE LOC: ", self.obstacle_locations)

        ans = self.computeValue()
        for item in ans:
            output_file.write(str(item) + "\n")

        input_file.close()
        output_file.close()

    def computeValue(self):
        for i in range(self.num_cars):
            self.calculate_reward_policy(i)
            self.res = []
            for j in range(10):
                self.val = 0
                pos = self.car_start_locations[i]

                if pos == self.car_end_locations[i]:
                    self.val += 100
                    self.res.append(self.val)
                    continue

                np.random.seed(j)
                swerve = np.random.random_sample(1000000)
                k = 0
                while pos != self.car_end_locations[i]:
                    indices = pos.split(",")
                    m = indices[1]
                    n = indices[0]
                    #print(m, n)
                    move = self.policy[int(m)][int(n)]
                    if swerve[k] > 0.7:
                        if swerve[k] > 0.8:
                            if swerve[k] > 0.9:
                                move = self.turn_right(self.turn_right(move))
                            else:
                                move = self.turn_right(move)
                        else:
                            move = self.turn_left(move)
                    x, y = self.getNextCoordinates(move, m, n)
                    self.val += self.reward_matrix_2[x][y]
                    pos = str(y) + "," + str(x)
                    k += 1
                self.res.append(self.val)
            total = sum(self.res)
            #total = total // 10
            total = np.floor(total/10)
            print(int(total))
            self.ans.append(int(total))
        return self.ans

    def turn_left(self, current_move):
        if current_move == "NORTH":
            return "WEST"
        elif current_move == "EAST":
            return "NORTH"
        elif current_move == "SOUTH":
            return "EAST"
        else:
            return "SOUTH"

    def turn_right(self, current_move):
        if current_move == "NORTH":
            return "EAST"
        elif current_move == "EAST":
            return "SOUTH"
        elif current_move == "SOUTH":
            return "WEST"
        else:
            return "NORTH"

    def getNextCoordinates(self, current_move, i, j):
        if current_move == "NORTH":
            if int(i) == 0:
                return int(i), int(j)
            else:
                temp_str = str(int(i) - 1) + "," + str(j)
                if temp_str[::-1] in self.obstacle_locations:
                    return int(i) - 1, int(j)
                else:
                    return int(i) - 1, int(j)
        elif current_move == "EAST":
            if int(j) == self.grid_size - 1:
                return int(i), int(j)
            else:
                temp_str = str(i) + "," + str(int(j) + 1)
                if temp_str[::-1] in self.obstacle_locations:
                    return int(i), int(j) + 1
                else:
                    return int(i), int(j) + 1
        elif current_move == "SOUTH":
            if int(i) == self.grid_size - 1:
                return int(i), int(j)
            else:
                temp_str = str(int(i) + 1) + "," + str(j)
                if temp_str[::-1] in self.obstacle_locations:
                    return int(i) + 1, int(j)
                else:
                    return int(i) + 1, int(j)
        else:
            if int(j) == 0:
                return int(i), int(j)
            else:
                temp_str = str(i) + "," + str(int(j) - 1)
                if temp_str[::-1] in self.obstacle_locations:
                    return int(i), int(j) - 1
                else:
                    return int(i), int(j) - 1

    def calculate_reward_policy(self, car):
        self.utility_matrix = [[0 for m in range(self.grid_size)] for n in range(self.grid_size)]
        self.reward_matrix = [[-1 for m in range(self.grid_size)] for n in range(self.grid_size)]
        #print("UTILITY MATRIX: ", self.utility_matrix)
        # print(self.reward_matrix)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                temp = str(i) + "," + str(j)
                if temp in self.obstacle_locations:
                    self.reward_matrix[i][j] = -101
                if temp == self.car_end_locations[car]:
                    self.reward_matrix[i][j] = 99

        #print("REWARD MATRIX: ", self.reward_matrix)
        self.reward_matrix_2 = np.transpose(self.reward_matrix)
        #print(self.reward_matrix_2)

        gamma = 0.9
        self.final_utility_matrix = []
        self.utility_matrix = np.asfarray(self.reward_matrix, 'Float64')
        while True:
            temp_utility = copy(self.utility_matrix)
            delta = 0
            diff = 0
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if str(i) + "," + str(j) == self.car_end_locations[car]:
                        continue
                    t1 = i
                    t2 = j + 1
                    t3 = i + 1
                    t4 = j
                    t5 = i
                    t6 = j - 1
                    t7 = i - 1
                    t8 = j
                    if t2 >= self.grid_size:
                        t2 = j
                    if t3 >= self.grid_size:
                        t3 = i
                    if t6 < 0:
                        t6 = j
                    if t7 < 0:
                        t7 = i
                    self.utility_matrix[i][j] = self.reward_matrix[i][j] + gamma * max((np.float64(0.7) * temp_utility[t7][
                        t8] + np.float64(0.1) * temp_utility[t3][t4] + np.float64(0.1) * temp_utility[t1][t2] + np.float64(0.1) * temp_utility[t5][t6]), (
                        np.float64(0.1) *
                                                                                               temp_utility[t7][
                                                                                                   t8] + np.float64(0.7) *
                                                                                               temp_utility[t3][
                                                                                                   t4] + np.float64(0.1) *
                                                                                               temp_utility[t1][
                                                                                                   t2] + np.float64(0.1) *
                                                                                               temp_utility[t5][
                                                                                                   t6]), (np.float64(0.1) *
                                                                                                          temp_utility[
                                                                                                              t7][
                                                                                                              t8] + np.float64(0.1) *
                                                                                                          temp_utility[
                                                                                                              t3][
                                                                                                              t4] + np.float64(0.7) *
                                                                                                          temp_utility[
                                                                                                              t1][
                                                                                                              t2] + np.float64(0.1) *
                                                                                                          temp_utility[
                                                                                                              t5][
                                                                                                              t6]),
                                                                                       (np.float64(0.1) * temp_utility[t7][
                                                                                           t8] + np.float64(0.1) * temp_utility[t3][
                                                                                            t4] + np.float64(0.1) *
                                                                                        temp_utility[t1][t2] + np.float64(0.7) *
                                                                                        temp_utility[t5][t6]))
                    delta = max(delta, abs(self.utility_matrix[i][j] - temp_utility[i][j]))

            if delta < 0.1:
                self.final_utility_matrix = np.transpose(temp_utility)
                break

        self.policy = [[0 for m in range(self.grid_size)] for n in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                t1 = i
                t2 = j + 1
                t3 = i + 1
                t4 = j
                t5 = i
                t6 = j - 1
                t7 = i - 1
                t8 = j
                if t2 >= self.grid_size:
                    t2 = j
                if t3 >= self.grid_size:
                    t3 = i
                if t6 < 0:
                    t6 = j
                if t7 < 0:
                    t7 = i
                east = self.final_utility_matrix[t1][t2]
                south = self.final_utility_matrix[t3][t4]
                west = self.final_utility_matrix[t5][t6]
                north = self.final_utility_matrix[t7][t8]
                maxi = max(north, south, east, west)
                if maxi == north:
                    self.policy[i][j] = "NORTH"
                elif maxi == south:
                    self.policy[i][j] = "SOUTH"
                elif maxi == east:
                    self.policy[i][j] = "EAST"
                else:
                    self.policy[i][j] = "WEST"

        #print("POLICY: ", self.policy)


g1 = Grid()
start_time = time.time()
g1.myfunc("input.txt")

print("--- %s seconds ---" % (time.time() - start_time))
