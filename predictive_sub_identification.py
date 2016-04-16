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


patient_groups = {} # groups of 240 patients relevant to eachother 
dataset_treatment_true = {} 
dataset_treatment_false = {} 

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
        self.patient_char = pat     
    
    
class Subgroup :
    ''' 
    contains similarities between all patients in this subgroup 
    
    '''             
    subgroup_ids = [] 
    
    # discrete genetic traits (x1:x20)        
    v0 = np.zeros(20)
    v1 = np.zeros(20)
    v2 = np.zeros(20)
    v0_1 = np.zeros(20)
    v0_2 = np.zeros(20)
    v1_2 = np.zeros(20)
    
    # continuous traits 
    v_max = np.zeros(20)
    v_min = np.zeros(20)
    treatment = []
    
    # initialize with two patients
    def __init__ (self, p1, p2) :   
        Subgroup.subgroup_ids = [int(p1.id), int(p2.id)] 
        
        # discrete genetic traits (x1:x20)        
#        Subgroup.v0 = 1*np.array(list(map(lambda x,y: x == '0' and x == y, p1.gen_char, p2.gen_char)))
#        Subgroup.v1 = 1*np.array(list(map(lambda x,y: x == '1' and y == '1', p1.gen_char, p2.gen_char)))
#        Subgroup.v2 = 1*np.array(list(map(lambda x,y: x == '2' and y == '2', p1.gen_char, p2.gen_char)))
        i = 0
        for x,y in zip(p1.gen_char, p2.gen_char): 
            if (i == 0) : 
                print("THIS SHIT " + str(x) +  "  " + str(y))
            if (x == 0.0 and x == y): 
                Subgroup.v0[i] = 1
                print("happening " + str(i))
            else: 
                Subgroup.v0[i] = 0
            if (x == 1 and x == y): 
                Subgroup.v1[i] = 1
            else: 
                Subgroup.v1[i] = 0
            if (x == 2 and x == y): 
                Subgroup.v2[i] = 1
            else: 
                Subgroup.v2[i] = 0
            i = i + 1
            
        
        Subgroup.v0_1 = Subgroup.v0 + Subgroup.v1 
        Subgroup.v0_2 = Subgroup.v0 + Subgroup.v2
        Subgroup.v1_2 = Subgroup.v1 + Subgroup.v2
        
        # continuous traits 
        Subgroup.v_max = np.maximum(np.array(p1.patient_char), np.array(p2.patient_char)) # all patients in this subgroup have trait x_i less than max[i]
        Subgroup.v_min = np.minimum(np.array(p1.patient_char), np.array(p2.patient_char)) # all patients in this subgroup have trait x_i greater than min[i]
        
        # how to handle treatments? exclude non-treated patients? without exclusion this alg. looks for traits that make everyone react better to disease
        # exclude all non-treatment before subgroup recursion alg. 
        Subgroup.treatment = [p1.trt,p2.trt] 
    
class Subgroup2(Subgroup):
    # initialize with two subgroups
    def __init__ (self, s1, s2): 
        Subgroup.subgroup_ids = s1.subgroup_ids.append(s2.subgroup_ids)
        
        Subgroup2.v0 = s1.v0 * s2.v0 
        Subgroup2.v1 = s1.v1 * s2.v1
        Subgroup2.v2 = s1.v2 * s2.v2 
        Subgroup2.v0_1 = s1.v0_1 * s2.v0_1 
        Subgroup2.v0_2 = s1.v0_2 * s2.v0_2 
        Subgroup2.v1_2 = s1.v1_2 * s2.v1_2         
        
        Subgroup2.max = np.maximum(s1.v_max, s2.v_max)
        Subgroup2.min = np.minimum(s1.v_min, s2.v_min)
        
        Subgroup2.treatment = s1.treatment.append(s2.treatment)
        
    
def main() : 
    path_in = input("Which pathname to use (work/home)")
    path = ""
    if (path_in == "work"): 
        path = data_pathname_WORK 
    elif (path_in == "home"): 
        path = data_pathname_HOME 
    else : 
        print("Not a valid path option")
    
    time.clock
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
                
      
      
      
    #print ("Patient length check " + str(len((patient_groups.keys()))))
    p1 = patient_groups[1][1] 
    p2 = patient_groups[1][2] 
    
    p3 = patient_groups[1][3]
    p4 = patient_groups[1][4]
    
    s1 = Subgroup(p1,p2)
    s2 = Subgroup(p3,p4)
    s3 = Subgroup2(s1,s2)
    print(s1.subgroup_ids)
    print(np.array(list(map(lambda x: int(x), p1.gen_char))))
    print(np.array(list(map(lambda x: int(x), p2.gen_char))))
    print(str(s1.v0))
    print(str(s1.v1))
    print(str(s1.v2))
    print(str(s1.v0_1))
    print(str(s1.v0_2))
    print(str(s1.v1_2))
    print(str(s1.v_max))
    print(str(s1.v_min))
    
    print()
    
    print(s2.subgroup_ids)
    print(p3.gen_char)
    print(p4.gen_char)
    print(str(s2.v0))
    print(str(s2.v1))
    print(str(s2.v2))
    print(str(s2.v0_1))
    print(str(s2.v0_2))
    print(str(s2.v1_2))
    print(str(s2.v_max))
    print(str(s2.v_min))
    
    
    print () 
    #s1.combine(s2)
    print(s3.subgroup_ids)
    print(str(s3.v0))
    print(str(s3.v1))
    print(str(s3.v2))
    print(str(s3.v0_1))
    print(str(s3.v0_2))
    print(str(s3.v1_2))
    print(str(s3.v_max))
    print(str(s3.v_min))    
    
    end_time = time.clock
    print("Time Elapsed: " + str(end_time))    
    
main() 