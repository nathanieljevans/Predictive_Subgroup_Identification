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
        self.patient_char = pat     
    
    
class Subgroup :
    ''' 
    contains similarities between all patients in this subgroup 
    
    '''             
#    
    # initialize with two patients
    def __init__ (self, p1, p2) :   

        self.subgroup_ids = [p1.id, p2.id]     
        
        # discrete genetic traits (x1:x20)        
        self.v0 = np.array(list(map(lambda x,y: (x == 0.0 and x == y)*1, p1.gen_char, p2.gen_char)))
        self.v1 = np.array(list(map(lambda x,y: (x == 1.0 and x == y)*1, p1.gen_char, p2.gen_char)))
        self.v2 = np.array(list(map(lambda x,y: (x == 2.0 and x == y)*1, p1.gen_char, p2.gen_char)))       
        
        self.v0_1 = self.v0 + self.v1 
        self.v0_2 = self.v0 + self.v2
        self.v1_2 = self.v1 + self.v2
        
        # continuous traits 
        self.v_max = np.maximum(np.array(p1.patient_char), np.array(p2.patient_char)) # all patients in this subgroup have trait x_i less than max[i]
        self.v_min = np.minimum(np.array(p1.patient_char), np.array(p2.patient_char)) # all patients in this subgroup have trait x_i greater than min[i]
        
        # how to handle treatments? exclude non-treated patients? without exclusion this alg. looks for traits that make everyone react better to disease
        # exclude all non-treatment before subgroup recursion alg. 
        self.treatment = [p1.trt,p2.trt] 
    
class Subgroup2:
    # initialize with two subgrou ps
    
    def __init__ (self, s1, s2): 
        self.subgroup_ids = s1.subgroup_ids + s2.subgroup_ids
        
        self.v0 = s1.v0 * s2.v0 
        self.v1 = s1.v1 * s2.v1
        self.v2 = s1.v2 * s2.v2 
        self.v0_1 = s1.v0_1 * s2.v0_1 
        self.v0_2 = s1.v0_2 * s2.v0_2 
        self.v1_2 = s1.v1_2 * s2.v1_2         
        
        self.v_max = np.maximum(s1.v_max, s2.v_max)
        self.v_min = np.minimum(s1.v_min, s2.v_min)
        
        Subgroup2.treatment = s1.treatment + s2.treatment 
        
class dataset_calculation: 
    
    def __init__ (self, data_id):
        self.dataset_id = data_id 
        self.patient_set = patient_groups[data_id] 
        self.treated_patients = filter(lambda x,y,z: x == 1, dataset_treatment_set[data_id])
        self.y_response_sum = sum(self.treated_patients)
        self.treatment_response = []
        
    def get_treatment_response(self,s1): 
        sub_sum = sum(s1.treatment)
        not_subgroup_sum = self.y_response_sum - sub_sum
        num_in_sub = len(s1.treatment)
        num_not_in_sub = len(self.treated_patients) - num_in_sub
        avg_diff = (sub_sum / num_in_sub) - (not_subgroup_sum / num_not_in_sub)
        return avg_diff
        
    def recursive_subgroup_generation(self, s1): 
        
        
    
def main() : 
    path_in = input("Which pathname to use (work/home)")
    path = ""
    if (path_in == "work"): 
        path = data_pathname_WORK 
    elif (path_in == "home"): 
        path = data_pathname_HOME 
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
            if (dataset not in dataset_treatment_set): 
                dataset_treatment_set[dataset] = [(treatment, data_id, y_response)]
            else: 
                dataset_treatment_set[dataset].append((treatment, data_id, y_response))
                
      
      
      
#    #print ("Patient length check " + str(len((patient_groups.keys()))))
#    p1 = patient_groups[1][0] 
#    p2 = patient_groups[1][1] 
#    
#    p3 = patient_groups[1][2]
#    p4 = patient_groups[1][3]
#    
#    s1 = Subgroup(p1,p2)
#    s2 = Subgroup(p3,p4)
#    s3 = Subgroup2(s1,s2)
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
#    
#    print () 
#    #s1.combine(s2)
#    print(s3.subgroup_ids)
#    print(str(s3.v0))
#    print(str(s3.v1))
#    print(str(s3.v2))
#    print(str(s3.v0_1))
#    print(str(s3.v0_2))
#    print(str(s3.v1_2))
#    print(str(s3.v_max))
#    print(str(s3.v_min))    
    
    end_time = time.clock()
    print("Time Elapsed: " + str((end_time - start_time)))    
    
main() 