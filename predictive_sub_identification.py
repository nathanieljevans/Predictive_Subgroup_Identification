# -*- coding: utf-8 -*-
"""
Innocentive Challenge: Predictive Subgroup Identification 
@author: Nate Evans 
Creation Date: 4/6/16
project description and necessary .csv files available at: https://www.innocentive.com/ar/workspace/challengeDetail?challenge=9933623
"""

import csv

# CSV files stored under the Downloads folder
data_pathname_WORK = "C:\\Users\\Administrator\\Downloads\\Innocentive_9933623_Data.csv" 
data_pathname_HOME = "C:\\Users\\Nate\\Downloads\\InnoCentive_9933623_Data.csv" 
example_submit_pathname_HOME = "C:\\Users\\Nate\\Downloads\\InnoCentive_9933623_example_submit.csv" 
training_data_pathname = "C:\\Users\\Nate\\Downloads\\InnoCentive_9933623_Training_Data.csv" 
truth_subjects_pathname = "C:\\Users\\Nate\\Downloads\\InnoCentive_9933623_Training_Data_truth_subjects.csv" 


patient_list = []

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
                    if (i <21): 
                        gen_list.append(x)
                    else: 
                        pat_list.append(x)
          
        p =  Patient(dataset,data_id,treatment,y_response,gen_list,pat_list)               
        patient_list.append(p)
      
    print ("Patient length check " + str(len(patient_list)))

main() 