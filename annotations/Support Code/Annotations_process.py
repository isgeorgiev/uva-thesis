"""
Script for processing and cleaning the google drive annotations.
The output is a simple .csv file with the acronyms and expansions per document.
Date: 17-05-2022
"""
# dependencies
from email import charset
import os
import pandas as pd
import re
import csv

"""
train --> "acronym": 20, "expansion": "secrecy rate", "id": "TR-0", "tokens":[]
test --> "acronym": 34, "id": "TS-0", "tokens": ["Experiment", "2", ":"

To do's: create test and train sets 
"""

rootdir = 'D:/University/Thesis/annotations/code'
df = pd.DataFrame(columns=['acronym', 'expansion', 'language', 'type'])

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def cleaning_raw_annotation(df, rootdir):
    # Creating the file directories
    acronyms = {}
    unique_acronyms = {}
    bulgarian_acronyms = 0
    english_acronyms = 0
    other_acronyms = 0
    bulgarian_acronyms_check = 0
    english_acronyms_check = 0
    other_acronyms_check = 0
    in_expansion_acronyms = 0
    out_expansion_acronyms = 0
    bulgarian_in_expansion_acronyms = 0
    english_in_expansion_acronyms = 0
    other_in_expansion_acronyms = 0
    bulgarian_out_expansion_acronyms = 0
    english_out_expansion_acronyms = 0
    other_out_expansion_acronyms = 0
    with open('./clean_data/clean_annotations_without_duplicates.csv', newline='', encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile,skipinitialspace=True, delimiter=',', quotechar='|')
        next(csvreader)
        for row in csvreader:
            # print(row)
            if row[0] in acronyms:
                acronyms[row[0]] = acronyms[row[0]] + 1
            else:
                acronyms[row[0]] = 1    
            
            if row[0] not in unique_acronyms:
                unique_acronyms[row[0]] = {"expansion":row[1], "language":row[2]}

            if row[3] == 'in_expansion':
                in_expansion_acronyms += 1
            else:
                out_expansion_acronyms += 1
            if row[2] == 'bg':
                bulgarian_acronyms_check += 1
                if row[3] == 'in_expansion':
                    bulgarian_in_expansion_acronyms += 1
                if row[3] == 'out_expansion':
                    bulgarian_out_expansion_acronyms += 1
            if row[2] == 'en':
                english_acronyms_check += 1 
                if row[3] == 'in_expansion':
                    english_in_expansion_acronyms += 1
                if row[3] == 'out_expansion':
                    english_out_expansion_acronyms += 1
            if row[2] == 'other language' or row[2] == 'none_of_above':
                other_acronyms_check += 1 
                if row[3] == 'in_expansion':
                    other_in_expansion_acronyms += 1
                if row[3] == 'out_expansion':
                    other_out_expansion_acronyms += 1

    acronyms = dict(sorted(acronyms.items(), key=lambda item: item[1]))
    print("Total unique acronyms: " + str(len(acronyms)))
    print(unique_acronyms)
    
    # for acronym in acronyms:
    #         if has_cyrillic(acronym):
    #             bulgarian_acronyms += 1
    #         else: 
    #             english_acronyms += 1 

    for acronym in unique_acronyms:
        if unique_acronyms[acronym]['language'] == 'bg':
            bulgarian_acronyms += 1
        elif unique_acronyms[acronym]['language'] == 'en':
            english_acronyms += 1
        else:
            other_acronyms += 1

    print("Bulgarian acronyms: " + str(bulgarian_acronyms))
    print("English acronyms: " +str(english_acronyms))
    print("Other acronyms: " + str(other_acronyms))
    print("Bulgarian acronyms check: " + str(bulgarian_acronyms_check))
    print("English acronyms check: " + str(english_acronyms_check))
    print("Other acronyms check: " + str(other_acronyms_check))
    print ("In expansion: " + str(in_expansion_acronyms))
    print ("Out expansion: " + str(out_expansion_acronyms))
    print ("Bulgarian in expansion: " + str(bulgarian_in_expansion_acronyms))
    print ("English in expansion: " + str(english_in_expansion_acronyms))
    print ("Other in expansion: " + str(other_in_expansion_acronyms))
    print ("Bulgarian out expansion: " + str(bulgarian_out_expansion_acronyms))
    print ("English out expansion: " + str(english_out_expansion_acronyms))
    print ("Other out expansion: " + str(other_out_expansion_acronyms))
if __name__ == "__main__":
    cleaning_raw_annotation(df, rootdir)