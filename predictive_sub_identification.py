# -*- coding: utf-8 -*-
"""
Innocentive Challenge: Predictive Subgroup Identification 
@author: Nate Evans 
Creation Date: 4/6/16
project description and necessary .csv files available at: https://www.innocentive.com/ar/workspace/challengeDetail?challenge=9933623
"""

import csv
import numpy as np
import time

# CSV files stored under the Downloads folder
data_pathname_WORK = "C:\\Users\\Administrator\\Downloads\\Innocentive_9933623_Data.csv" 
data_pathname_HOME = "C:\\Users\\Nate\\Downloads\\InnoCentive_9933623_Data.csv" 
example_submit_pathname_HOME = "C:\\Users\\Nate\\Downloads\\InnoCentive_9933623_example_submit.csv" 
training_data_pathname = "C:\\Users\\Nate\\Downloads\\InnoCentive_9933623_Training_Data.csv" 
truth_subjects_pathname = "C:\\Users\\Nate\\Downloads\\InnoCentive_9933623_Training_Data_truth_subjects.csv" 

output_work = 'C:\\Users\\Administrator\\Documents\\subgroup_output\\subgroup_treatment.csv'
output_home = 'C:\\Users\\Nate\\Desktop\\subgroup_csv\\subgroup_treatment.csv'

output_path = '' 

patient_groups = {} # groups of 240 patients relevant to eachother 
# this is a set with the dataset_id as a key and the set being a list of tuples (treatment(y/n), patient id, y_response)
dataset_treatment_set = {} 


class Patient: 
    '''
    unique_id = 0 # this might be unnecessary since the datasets are unrelated... I think? 
    dataset = "" 
    data_id = "" # this is a the count within a dataset, not unique
    y_response = 0.0 # more negative values showing a better treatment effect :: "meaningfully better" is anything less then -0.6
    gen_char = [] # vals can be 0,1,2, called x1 through x20 in the description
    patient_char = [] # these values are continuous
    '''
    
    def __init__ (self, data, d_id, treatment, y, gen, pat): 
        self.dataset = data 
        self .id = d_id 
        self.trt = treatment
        self.y_response = y 
        self.gen_char = gen 
        self.patient_char = np.array(pat)     
    
        self.v0 = np.array(list(map(lambda x: (x == 0.0)*1, self.gen_char)))
        self.v1 = np.array(list(map(lambda x: (x == 1.0)*1, self.gen_char)))
        self.v2 = np.array(list(map(lambda x: (x == 2.0)*1, self.gen_char)))       
        
        self.v0_1 = np.add(self.v0,self.v1) 
        self.v0_2 = np.add(self.v0,self.v2) 
        self.v1_2 = np.add(self.v1,self.v2) 
    
class Subgroup :
    ''' 
    contains similarities between all patients in this subgroup 
    
    '''             
#    
    # initialize with two patients
    def __init__ (self, p1, p2) :   
        self.last_id = p2.id

        self.subgroup_ids = [p1.id, p2.id]
        self.y_treatment = [p1.y_response,p2.y_response]
        
        self.v0 = p1.v0 * p2.v0
        self.v1 = p1.v1 * p2.v1
        self.v2 = p1.v2 * p2.v2
        self.v0_1 = p1.v0_1 * p2.v0_1
        self.v0_2 = p1.v0_2 * p2.v0_2
        self.v1_2 = p1.v1_2 * p2.v1_2
        
        # continuous traits 
        self.v_max = np.maximum((p1.patient_char), (p2.patient_char)) # all patients in this subgroup have trait x_i less than max[i]
        self.v_min = np.minimum((p1.patient_char), (p2.patient_char)) # all patients in this subgroup have trait x_i greater than min[i]
        
        # how to handle treatments? exclude non-treated patients? without exclusion this alg. looks for traits that make everyone react better to disease
        # exclude all non-treatment before subgroup recursion alg. 
        
        
    def add_patient(self, p): 
        self.last_id = p.id
        self.subgroup_ids.append(p.id)
        self.y_treatment.append(p.y_response)   
                
        self.v0 = p.v0 * self.v0
        self.v1 = p.v1 * self.v1
        self.v2 = p.v2 * self.v2
        self.v0_1 = p.v0_1 * self.v0_1
        self.v0_2 = p.v0_2 * self.v0_2
        self.v1_2 = p.v1_2 * self.v1_2
        
                # continuous traits 
        self.v_max = np.maximum(self.v_max, p.patient_char) # all patients in this subgroup have trait x_i less than max[i]
        self.v_min = np.minimum(self.v_min, p.patient_char) # all patients in this subgroup have trait x_i greater than min[i]
        
class dataset_calculation: 

    
    def __init__ (self, data_id):
        
        self.index = 0
        self.dataset_id = data_id 
        self.patient_set = list(patient_groups[data_id]) 
        #self.treated_patients = np.array((filter(lambda x,y,z: x == 1, dataset_treatment_set[data_id])))
        self.y_response_all = []
        self.y_response_treated = []
        for p in self.patient_set: 
            self.y_response_all.append(p.y_response)
            if (p.trt == 1): 
                self.y_response_treated.append(p.y_response)
        
        self.y_response_all = np.array(self.y_response_all)
        self.y_response_treated = np.array(self.y_response_treated)
        
        self.y_response_sum = np.sum(self.y_response_treated)
        self.num_patients = len(self.y_response_treated)
        
        self.response_vector= np.zeros(1000000) # not sure how to size this. use this for now
        
    # get the treatment response for a specific subgroup
    def get_treatment_response(self, s1): 
        sub_sum = sum(s1.y_treatment)
        not_subgroup_sum = self.y_response_sum - sub_sum
        num_in_sub = len(s1.y_treatment)
        num_not_in_sub = self.num_patients - num_in_sub
        avg_diff = (sub_sum / num_in_sub) - (not_subgroup_sum / num_not_in_sub)
        return avg_diff
        
    def subgroup_combination(self): 
        
        # i is the number of patients in subgroup (1 corresponds to 2 patients)
        # generates all the patients
        
        for i in range(self.num_patients-1):
            for n in range(self.num_patients - 1):
                if (n > i and self.index < 10000): 
                    subgroup = Subgroup(self.patient_set[i], self.patient_set[n])
                    self.response_vector[self.index] = self.get_treatment_response(subgroup)
                    self.index = self.index + 1
                    self.recursive_gen(subgroup)
                
    def recursive_gen(self, subgroup): 
        # exit test 
        global output_path
        if (len(subgroup.subgroup_ids)  == self.num_patients or self.index > 10000): 
            print("wow it made it!")
            print(subgroup.subgroup_ids)
#            myfile = open('C:\\Users\\Nate\\Desktop\\subgroup_csv\\subgroup_treatment.csv', 'wb')
#            wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
#            wr.writerow(list(self.response_vector))
            np.savetxt(output_path, self.response_vector, delimiter=',')
            return 0 
        
        else: 
            for i in range(subgroup.last_id + 1, self.num_patients-1,1): 
                if (self.index <= 10000): 
                    subgroup.add_patient(self.patient_set[i])
                    self.response_vector[self.index] = self.get_treatment_response(subgroup)
                    self.index = self.index + 1 
                    self.recursive_gen(subgroup)

        
          
def main() : 
    path_in = input("Which pathname to use (work/home)")
    path = ""
    global output_path
    if (path_in == "work"): 
        path = data_pathname_WORK 
        output_path = output_work
    elif (path_in == "home"): 
        path = data_pathname_HOME 
        output_path = output_home
    else : 
        print("Not a valid path option")
    
    start_time = time.clock()
    data_file = list(csv.reader(open(path)))
    
    for i,patient in enumerate(data_file): 
        gen_list = [] 
        pat_list = []
        dataset = ""
        data_id = "" 
        treatment = -1 
        y_response = 0.0
        if(i != 0):  
            dataset = int(patient[0]) 
            data_id = int(patient[1])
            treatment = int(patient[2]) 
            y_response = float(patient[3]) 
            for i, x in enumerate(patient): 
                x = float(x)
                if (i > 3) :
                    if (i <24): 
                        gen_list.append(x)
                    else: 
                        pat_list.append(float(x))
          
            p =  Patient(dataset,data_id,treatment,y_response,gen_list,pat_list)  
            if (dataset not in patient_groups) : 
                   patient_groups[dataset] = [p] 
            else : 
                patient_groups[dataset].append(p)
#            if (dataset not in dataset_treatment_set): 
#                dataset_treatment_set[dataset] = [(treatment, data_id, y_response)]
#            else: 
#                dataset_treatment_set[dataset].append((treatment, data_id, y_response))
                
      
      
      
    #print ("Patient length check " + str(len((patient_groups.keys()))))
#    p1 = patient_groups[1][0] 
#    p2 = patient_groups[1][1] 
#    
#    p3 = patient_groups[1][2]
#    p4 = patient_groups[1][3]
#    
#    s1 = Subgroup(p1,p2)
#    s2 = Subgroup(p3,p4)
#    
#    d1 = dataset_calculation(1)
#    trt = d1.get_treatment_response(s1)
#    print(str(trt))
    
#    print("patient init")
#    print(str(p1.gen_char))
#    print(str(p1.v0))
#    print(str(p1.v1))
#    print(str(p1.v2))
#    print(str(p1.v0_1))
#    print(str(p1.v0_2))
#    print(str(p1.v1_2))
#    print("end patient init")
#    
#    print("patient init")
#    print(str(p2.gen_char))
#    print(str(p2.v0))
#    print(str(p2.v1))
#    print(str(p2.v2))
#    print(str(p2.v0_1))
#    print(str(p2.v0_2))
#    print(str(p2.v1_2))
#    print("end patient init")
#
#    print(s1.subgroup_ids)
#    print(np.array(list(map(lambda x: int(x), p1.gen_char))))
#    print(np.array(list(map(lambda x: int(x), p2.gen_char))))
#    print(str(s1.v0))
#    print(str(s1.v1))
#    print(str(s1.v2))
#    print(str(s1.v0_1))
#    print(str(s1.v0_2))
#    print(str(s1.v1_2))
#    print(str(s1.v_max))
#    print(str(s1.v_min))
#    
#    print()
#    
#    print(s2.subgroup_ids)
#    print(p3.gen_char)
#    print(p4.gen_char)
#    print(str(s2.v0))
#    print(str(s2.v1))
#    print(str(s2.v2))
#    print(str(s2.v0_1))
#    print(str(s2.v0_2))
#    print(str(s2.v1_2))
#    print(str(s2.v_max))
#    print(str(s2.v_min))
#    
    print("made it here")
       
    data_1 = dataset_calculation(1)
    data_1.subgroup_combination()
    end_time = time.clock()
    print("Time Elapsed: " + str((end_time - start_time)))    
    
main() 