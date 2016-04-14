# -*- coding: utf-8 -*-
"""
Innocentive Challenge: Predictive Subgroup Identification 
@author: Nate Evans 
Creation Date: 4/6/16
project description and necessary .csv files available at: https://www.innocentive.com/ar/workspace/challengeDetail?challenge=9933623
"""

import csv
import numpy as np

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
    subgroup_ids = [0] 
    
    # discrete genetic traits (x1:x20)        
    v0 = []
    v1 = []
    v2 = []
    v0_1 = []
    v0_2 = []
    v1_2 = []
    
    # continuous traits 
    v_max = []
    v_min = []
    treatment = [] 
    def __init__ (self, p1, p2) :   
        Subgroup.subgroup_ids = [p1.id, p2.id] 
        
        # discrete genetic traits (x1:x20)        
        Subgroup.v0 = 1*np.array(list(map(lambda x,y: x == '0' and y == '0', p1.gen_char, p2.gen_char)))
        Subgroup.v1 = 1*np.array(list(map(lambda x,y: x == '1' and y == '1', p1.gen_char, p2.gen_char)))
        Subgroup.v2 = 1*np.array(list(map(lambda x,y: x == '2' and y == '2', p1.gen_char, p2.gen_char)))
        Subgroup.v0_1 = self.v0 + self.v1 
        Subgroup.v0_2 = self.v0 + self.v2
        Subgroup.v1_2 = self.v1 + self.v2
        
        # continuous traits 
        Subgroup.v_max = np.maximum(np.array(p1.patient_char), np.array(p2.patient_char)) # all patients in this subgroup have trait x_i less than max[i]
        Subgroup.v_min = np.minimum(np.array(p1.patient_char), np.array(p2.patient_char)) # all patients in this subgroup have trait x_i greater than min[i]
        
        # how to handle treatments? exclude non-treated patients? without exclusion this alg. looks for traits that make everyone react better to disease
        # exclude all non-treatment before subgroup recursion alg. 
        Subgroup.treatment = [p1.trt,p2.trt] 
    
    def combine(self, Subgroup_2) :  
        Subgroup.subgroup_ids.append(Subgroup_2.subgroup_ids)
        
        Subgroup.v0 = Subgroup.v0 * Subgroup_2.v0 
        Subgroup.v1 = Subgroup.v1 * Subgroup_2.v1
        Subgroup.v2 = Subgroup.v2 * Subgroup_2.v2 
        Subgroup.v0_1 = Subgroup.v0_1 * Subgroup_2.v0_1 
        Subgroup.v0_2 = Subgroup.v0_2 * Subgroup_2.v0_2 
        Subgroup.v1_2 = Subgroup.v1_2 * Subgroup_2.v1_2 
        
        Subgroup.max = np.maximum(Subgroup.v_max, Subgroup_2.v_max)
        Subgroup.min = np.minimum(Subgroup.v_min, Subgroup_2.v_min)
        
        Subgroup.treatment = Subgroup.treatment.append(Subgroup_2.treatment)
        
    
def main() : 
    path_in = input("Which pathname to use (work/home)")
    path = ""
    if (path_in == "work"): 
        path = data_pathname_WORK 
    elif (path_in == "home"): 
        path = data_pathname_HOME 
    else : 
        print("Not a valid path option")
    
    data_file = list(csv.reader(open(path)))
    
    for i,patient in enumerate(data_file): 
        gen_list = [] 
        pat_list = []
        dataset = ""
        data_id = "" 
        treatment = -1 
        y_response = 0.0
        if(i != 0):  
            dataset = patient[0] 
            data_id = patient[1]
            treatment = patient[2] 
            y_response = patient[3] 
            for i, x in enumerate(patient): 
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
    p1 = patient_groups['1'][1] 
    p2 = patient_groups['1'][2] 
    
    p3 = patient_groups['1'][3]
    p4 = patient_groups['1'][4]
    
    s1 = Subgroup(p1,p2)
    s2 = Subgroup(p3,p4)
    print(s1.subgroup_ids)
    print(p1.gen_char)
    print(p2.gen_char)
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
    s1.combine(s2)
    print(s1.subgroup_ids)
    print(str(s1.v0))
    print(str(s1.v1))
    print(str(s1.v2))
    print(str(s1.v0_1))
    print(str(s1.v0_2))
    print(str(s1.v1_2))
    print(str(s1.v_max))
    print(str(s1.v_min))    
    
main() 