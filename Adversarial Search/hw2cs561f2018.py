from copy import copy, deepcopy
import collections
import time


class Grid:

    def __init__(self):
        self.bed_spaces = 0
        self.num_parking_lots = 0
        self.num_applicants_chosen_SPLA = 0
        self.temp_num_applicants_chosen_SPLA = 0
        self.num_applicants_chosen_LAHSA = 0
        self.temp_num_applicants_chosen_LAHSA = 0
        self.applicants_chosen_SPLA = []
        self.applicants_chosen_LAHSA = []
        self.num_applicants = 0
        self.applicants_info = []
        self.SPLA_ONLY = []
        self.LAHSA_ONLY = []
        self.SPLA_LAHSA = []
        self.unallocated_applicants = []
        self.d_SPLA = {"M":0,"T":0,"W":0,"Th":0,"F":0,"Sat":0,"Sun":0}
        self.d_LAHSA = {"M": 0, "T": 0, "W": 0, "Th": 0, "F": 0, "Sat": 0, "Sun": 0}
        self.total_beds = 0
        self.total_parking_slots = 0
        self.max_score = 0
        self.SPLA = []
        self.LAHSA = []
        self.plus_inf = 10000000000
        self.minus_inf = -10000000000
        self.accAll = True
        self.week_list = {0:[0,0], 1:[0,0], 2:[0,0], 3:[0,0], 4:[0,0], 5:[0,0], 6:[0,0]}
        self.common_temp = []
        self.spla_only_temp = []
        self.lahsa_only_temp = []

    def myfunc(self, file_name):
        input_file = open(file_name, "r")
        output_file = open("output.txt", "w")

        i = 1
        tot = 0
        scooter_coord = []
        for x in input_file:
            x = x.rstrip('\n\r')
            if i == 1:
                self.bed_spaces = int(x)
                i += 1
            elif i == 2:
                self.num_parking_lots = int(x)
                i += 1
            elif i == 3:
                self.num_applicants_chosen_LAHSA = int(x)
                self.temp_num_applicants_chosen_LAHSA = int(x)
                if self.num_applicants_chosen_LAHSA == 0:
                    i += 2
                else:
                    i += 1
            elif i == 4:
                self.applicants_chosen_LAHSA.append(x)
                self.temp_num_applicants_chosen_LAHSA -= 1
                if self.temp_num_applicants_chosen_LAHSA == 0:
                    i += 1
                    continue
            elif i == 5:
                self.num_applicants_chosen_SPLA = int(x)
                self.temp_num_applicants_chosen_SPLA = int(x)
                if self.num_applicants_chosen_SPLA == 0:
                    i += 2
                else:
                    i += 1
            elif i == 6:
                self.applicants_chosen_SPLA.append(x)
                self.temp_num_applicants_chosen_SPLA -= 1
                if self.temp_num_applicants_chosen_SPLA == 0:
                    i += 1
                    continue
            elif i == 7:
                self.num_applicants = int(x)
                i += 1
            elif i >= 8:
                self.applicants_info.append(x)

        self.total_beds = int(self.bed_spaces) * 7
        self.total_parking_slots = int(self.num_parking_lots) * 7

        # print("------------------------------------------INITIAL INFO--------------------------------------")
        # print(self.bed_spaces)
        # print(self.num_parking_lots)
        # print(self.num_applicants_chosen_LAHSA)
        # print(self.applicants_chosen_LAHSA)
        # print(self.num_applicants_chosen_SPLA)
        # print(self.applicants_chosen_SPLA)
        # print(self.num_applicants)
        # print(self.applicants_info)
        # print("---------------------------------------------------------------------------------------------")

        for x in self.applicants_info:
            if x[0:5] in self.applicants_chosen_LAHSA:
                self.d_LAHSA["M"] += int(x[13])
                self.d_LAHSA["T"] += int(x[14])
                self.d_LAHSA["W"] += int(x[15])
                self.d_LAHSA["Th"] += int(x[16])
                self.d_LAHSA["F"] += int(x[17])
                self.d_LAHSA["Sat"] += int(x[18])
                self.d_LAHSA["Sun"] += int(x[19])

        for x in self.applicants_info:
            if x[0:5] in self.applicants_chosen_SPLA:
                self.d_SPLA["M"] += int(x[13])
                self.d_SPLA["T"] += int(x[14])
                self.d_SPLA["W"] += int(x[15])
                self.d_SPLA["Th"] += int(x[16])
                self.d_SPLA["F"] += int(x[17])
                self.d_SPLA["Sat"] += int(x[18])
                self.d_SPLA["Sun"] += int(x[19])

        # print("Dict LAHSA:  ", self.d_LAHSA)
        # print("Dict SPLA:   ", self.d_SPLA)

        for x in self.d_LAHSA:
            if self.d_LAHSA[x] == 1:
                self.total_beds -= 1
        for x in self.d_SPLA:
            if self.d_SPLA[x] == 1:
                self.total_parking_slots -= 1

        # print("Total LAHSA:  ", self.total_beds)
        # print("Total SPLA:   ", self.total_parking_slots)

        for x in self.applicants_info:
            if x[0:5] in self.applicants_chosen_SPLA or x[0:5] in self.applicants_chosen_LAHSA:
                continue
            else:
                self.unallocated_applicants.append(x)
            if x[5] == 'F' and int(x[6:9]) > 17 and x[9] == 'N' and x[10] == 'N' and x[11] == 'Y' and x[12] == 'Y':
                self.SPLA_LAHSA.append(x)
                self.common_temp.append(x)
            if x[5] == 'F' and int(x[6:9]) > 17 and x[9] == 'N':
                if x not in self.SPLA_LAHSA:
                    self.LAHSA_ONLY.append(x)
                    self.lahsa_only_temp.append(x)
            if x[10] == 'N' and x[11] == 'Y' and x[12] == 'Y':
                if x not in self.SPLA_LAHSA:
                    self.SPLA_ONLY.append(x)
                    self.spla_only_temp.append(x)

        for x in self.unallocated_applicants:
            if x in self.SPLA_ONLY or x in self.SPLA_LAHSA:
                self.SPLA.append(x)
            if x in self.LAHSA_ONLY or x in self.SPLA_LAHSA:
                self.LAHSA.append(x)

        #print("SPLA: ", self.SPLA)
        #print("LAHSA: ", self.LAHSA)


        # print("------------------------------------------REQUIRED LISTS--------------------------------------")
        # print("UNALLOCATED: ", self.unallocated_applicants)
        # print("COMMON: ", self.SPLA_LAHSA)
        # print("LAHSA_ONLY: ", self.LAHSA_ONLY)
        # print("SPLA_ONLY: ", self.SPLA_ONLY)
        # print("-----------------------------------------------------------------------------------------------")

        for applicant in self.applicants_info:
            if applicant[:5] in self.applicants_chosen_SPLA:
                self.addToWeekList(applicant, True)
            elif applicant[:5] in self.applicants_chosen_LAHSA:
                self.addToWeekList(applicant, False)
            else:
                if applicant in self.SPLA_ONLY:
                    self.addToWeekList(applicant, True)
                if applicant in self.LAHSA_ONLY:
                    self.addToWeekList(applicant, False)

        #print(self.week_list)

        for x,y in self.week_list.values():
            if x > self.bed_spaces or y > self.num_parking_lots:
                self.accAll = False


        answer = 0
        if len(self.SPLA) == 1 and len(self.LAHSA) == 0:
            answer = self.SPLA[0]
            print("ANSWER: ", answer[0:5])
            output_file.write(str(answer[0:5]))
            return answer[0:5]
        if len(self.SPLA) == 2 and len(self.LAHSA) == 0:
            app1 = self.SPLA[0]
            app2 = self.SPLA[1]
            if (self.total_parking_slots - (int(app1[13:].count("1")) + int(app2[13:].count("1")))) >= 0:
                if int(app1[0:5]) < int(app2[0:5]):
                    answer = app1[0:5]
                else:
                    answer = app2[0:5]
            else:
                if int(app1[13:].count("1")) > int(app2[13:].count("1")):
                    maxi = app1
                    mini = app2
                else:
                    maxi = app2
                    mini = app1
                if self.total_parking_slots - int(maxi[13:].count("1")) >= 0:
                    answer = maxi[0:5]
                else:
                    answer = mini[0:5]
            print("ANSWER: ", answer)
            output_file.write(str(answer))
            return answer

        self.common_temp = sorted(self.common_temp, key=lambda app: int(app[13:].count("1")), reverse=True)
        max_common = int(self.common_temp[0][13:].count("1"))
        answer_common = int(self.common_temp[0][0:5])
        answer1 = self.common_temp[0][0:5]
        sorted(self.spla_only_temp, key=lambda app: int(app[13:].count("1")), reverse=True)
        max_spla = int(self.spla_only_temp[0][13:].count("1"))
        answer_spla = int(self.spla_only_temp[0][0:5])
        answer2 = self.spla_only_temp[0][0:5]

        if self.accAll == True:
            if len(self.common_temp) > 0:
                i = 1
                while i < len(self.common_temp) and int(self.common_temp[i][13:].count("1")) == max_common:
                    if int(self.common_temp[i][0:5]) < answer_common:
                        answer1 = self.common_temp[i][0:5]
                    i += 1
                print("ANSWER: ", answer1)
                output_file.write(str(answer1))
                return

            elif len(self.spla_only_temp) > 0:
                i = 1
                while i < len(self.spla_only_temp) and int(self.spla_only_temp[i][13:].count("1")) == max_spla:
                    if int(self.spla_only_temp[i][0:5]) < answer_spla:
                        answer2 = self.spla_only_temp[i][0:5]
                    i += 1
                print("ANSWER: ", answer2)
                output_file.write(str(answer2))
                return

        answer = self.chooseNext(self.SPLA, self.LAHSA, True)
        answer = self.SPLA[int(self.max_score)][0:5]
        print("ANSWER: ", answer)
        # print("ANSWER: ", answer)
        # print("INDEX: ", self.max_score)
        output_file.write(str(answer))

        input_file.close()
        output_file.close()

    def addToWeekList(self, applicant, fromSPLA):
        schedule = applicant[13:]
        if fromSPLA:
            for i in range(7):
                if schedule[i] == "1":
                    self.week_list[i][1] += 1
        else:
            for i in range(7):
                if schedule[i] == "1":
                    self.week_list[i][0] += 1


    def chooseNext(self, spla, lahsa, maxPlayer):
        #print("SPLA values: ", spla)
        #print("LAHSA values: ", lahsa)

        li = []
        #for temp in range(len(pool)):
        if maxPlayer:
            if len(spla) == 0:
                return 0
            if len(lahsa) != 0:
                best_spla = 0
                for item in spla:
                    #pool_copy = copy(pool)
                    #if item in self.SPLA_LAHSA or item in self.SPLA_ONLY:
                    if item in self.applicants_chosen_SPLA:
                         continue
                    applicant_val = int(item[13:].count('1'))
                    if self.total_parking_slots - applicant_val < 0:
                        #print("spla total parking invalid")
                        continue

                    i = 0
                    flag = True
                    for x in self.d_SPLA:
                        if self.d_SPLA[x] + int(item[13+i]) > self.num_parking_lots:
                            flag = False
                            break
                        i += 1
                    if flag == False:
                        #print(self.d_SPLA)
                        #print("spla day wise parking invalid")
                        continue

                    i = 0
                    for x in self.d_SPLA:
                        self.d_SPLA[x] += int(item[13+i])
                        i += 1

                    #print("spla picked")
                    lahsa_flag = False
                    index1 = spla.index(item)
                    spla.remove(item)
                    if item in lahsa:
                        index2 = lahsa.index(item)
                        lahsa.remove(item)
                        lahsa_flag = True

                    self.total_parking_slots -= applicant_val
                    val = applicant_val
                    best_spla = max(best_spla, val + best_spla)
                    self.applicants_chosen_SPLA.append(item[0:5])
                    li.append(val + self.chooseNext(spla, lahsa, False))
                    self.applicants_chosen_SPLA.remove(item[0:5])
                    #print("SPLA: ", li)
                    spla.insert(index1, item)
                    if lahsa_flag:
                        lahsa.insert(index2, item)
                    i = 0
                    for x in self.d_SPLA:
                        self.d_SPLA[x] -= int(item[13 + i])
                        i += 1
                    self.total_parking_slots += applicant_val

                #return li.index(max(li))
                if len(li) == 0:
                    return 0
                self.max_score = li.index(max(li))
                return max(li)

            else:
                total = 0
                for x in spla:
                    temp = int(x[13:].count('1'))
                    total += temp
                return total


        else:
            #print("else")
            if len(lahsa) == 0:
                total = 0
                for x in spla:
                    temp = int(x[13:].count('1'))
                    total += temp
                return total
            if len(spla) != 0:
                best_lahsa = 0
                for item in lahsa:
                    #pool_copy = copy(pool)
                    #if item in self.SPLA_LAHSA or item in self.LAHSA_ONLY:
                    if item in self.applicants_chosen_LAHSA:
                         continue
                    applicant_val = int(item[13:].count('1'))
                    if self.total_beds - applicant_val < 0:
                        continue

                    i = 0
                    flag = True
                    for x in self.d_LAHSA:
                        if self.d_LAHSA[x] + int(item[13 + i]) > self.bed_spaces:
                            flag = False
                            break
                        i += 1
                    if flag == False:
                        #print("hi")
                        continue

                    i = 0
                    for x in self.d_LAHSA:
                        self.d_LAHSA[x] += int(item[13 + i])
                        i += 1

                    spla_flag = False
                    index1 = lahsa.index(item)
                    lahsa.remove(item)
                    if item in spla:
                        index2 = spla.index(item)
                        spla.remove(item)
                        spla_flag = True
                    #print(spla_flag)

                    self.total_beds -= applicant_val
                    val = applicant_val
                    best_lahsa = max(best_lahsa, val + best_lahsa)
                    self.applicants_chosen_LAHSA.append(item[0:5])
                    li.append(self.chooseNext(spla, lahsa, True))
                    self.applicants_chosen_LAHSA.remove(item[0:5])
                    #print("LAHSA: ", li)
                    lahsa.insert(index1, item)
                    if spla_flag:
                        spla.insert(index2, item)
                    i = 0
                    for x in self.d_LAHSA:
                        self.d_LAHSA[x] -= int(item[13 + i])
                        i += 1
                    self.total_beds += applicant_val

                #return li.index(min(li))
                if len(li) == 0:
                    return 0
                return min(li)

            else:
                return 0

g1 = Grid()
start_time = time.time()
g1.myfunc("input.txt")

print("--- %s seconds ---" % (time.time() - start_time))
