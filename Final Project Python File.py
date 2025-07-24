#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Project Template
DS 542

My Name: Adwoa N.
My Cuisine: African
"""

import pandas as pd

# What is your cuisine?

my_cuisine = 'African'

data_url = 'https://data.cityofnewyork.us/resource/43nn-pn8j.csv'

# Fetch dataset with a single API call (limit to max records SODA 2.0 allows)
limit = 50000
query_url = f"{data_url}?$limit={limit}"

try:
    food_data = pd.read_csv(query_url)
except Exception as e:
    print(f"Error fetching data: {e}")


def handleNanString(item):
    if(pd.isna(item)):
        return "Unknown"
    else:
        return item

"""
Answer all questions asked in the prompt.
Put your code to answer each question inside the comments that represent that question.
Print to the screen when you are asked for an answer.
"""

# Question 1 

class Citation:
    
    # Initializer
    def __init__(self, camis, dba, boro,street, action, cuisine_description, violation_code, violation_description, critical_flag, latitude, longitude):
        self.camis = handleNanString(camis)
        self.dba = handleNanString(dba)
        self.boro = handleNanString(boro)
        self.cuisine_description = handleNanString(cuisine_description)
        self.action = handleNanString(action)
        self.violation_code = handleNanString(violation_code)
        self.violation_description = handleNanString(violation_description)
        if critical_flag == 'Critical':
            self.critical_flag = True
        else:
            self.critical_flag = False
        self.latitude = handleNanString(latitude)
        self.longitude = handleNanString(longitude)
        self.street = handleNanString(street)
    
    # Tell Python how to print
    def __repr__(self):
        return(f'Key:{self.camis},Business Name: {self.dba}, Cuisine:{self.cuisine_description}')
    
    # Does the restaurant have mice?
    def has_mice(self):
        evidence_string = 'live mice'
        # is the evidence string inside the violation description?
        return(evidence_string in self.violation_description)
            
    # Does the restaurant have rats?
    def has_rats(self):
        evidence_string = 'live rats'
        return(evidence_string in self.violation_description)

    # Does the restuarant have roaches? 
    def has_roaches(self):
        evidence_string = 'Live roaches'
        return(evidence_string in self.violation_description)
    
    # Did the restaurant close as a result of the inspection?
    def is_closed(self):
        return ("closed" in self.action.lower())
            
        

        
# We need to create a dictionary
camis_dictionary = dict()
for i in range(len(food_data)):
    # Check if the row is for my cuisine
    if food_data['cuisine_description'][i] == my_cuisine:
        citation_instance = Citation(food_data['camis'][i], food_data['dba'][i], food_data['boro'][i], food_data['street'][i], food_data['action'][i], food_data['cuisine_description'][i], food_data['violation_code'][i], food_data['violation_description'][i], food_data['critical_flag'][i], food_data['latitude'][i], food_data['longitude'][i])
        #store in dictionary
        
        #if the camis key already exists in the dictionary, append the new list to the key
        if food_data['camis'][i] in camis_dictionary.keys():
            camis_dictionary[food_data['camis'][i]].append(citation_instance)
        else: #if the key doesn't already exist:
            camis_dictionary[food_data['camis'][i]] = []  # Initialize a new list if the key doesn't exist
            camis_dictionary[food_data['camis'][i]].append(citation_instance)  # Append the citation
   
    

# Question 2: Counting violations
rodent_violations = 0
roach_violations = 0

for citations in camis_dictionary.values():
    for citation in citations:
        if citation.has_mice() or citation.has_rats():
            rodent_violations += 1
        if citation.has_roaches():
            roach_violations += 1
            
# Calculate ratio
if roach_violations > 0:
    rodent_to_roach_ratio = rodent_violations//roach_violations
else:
    rodent_to_roach_ratio = "Undefined (no roach violations)"

#print results
print(f"Total rodent violations: {rodent_violations}")
print(' ')
print(f"Total roach violations: {roach_violations}")
print(' ')
print(f"Rodent to roach violation ratio: {rodent_to_roach_ratio}")
print(' ')


# Question 3

bronx_violation = 0
brooklyn_violation = 0
manhattan_violation = 0
queens_violation = 0
si_violation = 0

for citations in camis_dictionary.values():
    for citation in citations:
        if citation.critical_flag:
            if citation.boro == "Manhattan":
                manhattan_violation +=1
            if citation.boro == "Bronx":
                bronx_violation+=1
            if citation.boro == "Queens":
                queens_violation+=1
            if citation.boro == "Brooklyn":
                brooklyn_violation +=1
            if citation.boro == "Staten Island":
                si_violation+=1

# Find which borough has the most violations
borough_counts = dict()
borough_counts = {
    "Bronx": bronx_violation,
    "Brooklyn": brooklyn_violation,
    "Manhattan": manhattan_violation,
    "Queens": queens_violation,
    "Staten Island": si_violation
}

#borough with the most violations
max_violations_borough= max(borough_counts, key = borough_counts.get)
print(f"The borough with the most violations is {max_violations_borough} with {borough_counts[max_violations_borough]} violations.")
print(' ')



#restaurant with the most violations                      
restaurant_violations = {}
distinct_restaurants = set()

for citations in camis_dictionary.values():
    for citation in citations:
        distinct_restaurants.add(citation.camis)
        
camis_count = {camis: 0 for camis in distinct_restaurants}

# Count violations for each restaurant (CAMIS)
for citations in camis_dictionary.values():
    for citation in citations:
        camis_count[citation.camis] += 1  # Increase count for that restaurant

# Find the restaurant with the most violations and the number of times it has closed. 
most_violations_camis = max(camis_count, key=camis_count.get)
most_violations_count = camis_count[most_violations_camis]

# Get restaurant details
worst_restaurant_name = ""
worst_restaurant_borough = ""
worst_restaurant_street = ""
closure_count = 0


for citation in camis_dictionary[most_violations_camis]:  # Get details from any citation entry
    worst_restaurant_name = citation.dba
    worst_restaurant_borough = citation.boro
    worst_restaurant_street = citation.street
    if citation.is_closed(): #did the restaurant close?
        closure_count += 1

# Print results
print(f"The restaurant with the most violations is {worst_restaurant_name} located in {worst_restaurant_street}, {worst_restaurant_borough} "
      f"with {most_violations_count} violations and it has closed {closure_count} times.")

print(' ')

# Extra Credit
import matplotlib.pyplot as plt

bronx_rat_violation = 0
brooklyn_rat_violation= 0
queens_rat_violation=0
manhattan_rat_violation=0
si_rat_violation=0


for citations in camis_dictionary.values():
    for citation in citations:
        if citation.has_rats():
            if citation.boro == "Manhattan":
                manhattan_rat_violation +=1
            if citation.boro == "Bronx":
                bronx_rat_violation+=1
            if citation.boro == "Queens":
                queens_rat_violation+=1
            if citation.boro == "Brooklyn":
                brooklyn_rat_violation +=1
            if citation.boro == "Staten Island":
                si_rat_violation+=1

rat_violations_per_borough = {
    "Bronx": bronx_rat_violation,
    "Brooklyn": brooklyn_rat_violation,
    "Manhattan": manhattan_rat_violation,
    "Queens": queens_rat_violation,
    "Staten Island": si_rat_violation
    }

#the pie chart
plt.figure(figsize=(8, 8))
colors = ['orange', 'green', 'red', 'purple', 'blue']  # Define custom colors for each borough

# Remove boroughs with zero violations
filtered_rat_violations = {boro: count for boro, count in rat_violations_per_borough.items() if count > 0}
plt.pie(
    filtered_rat_violations.values(),
    labels=filtered_rat_violations.keys(),
    autopct='%1.1f%%',
    startangle=140,
    colors=colors,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1}
)
plt.title("Rat Only Violations by Borough (Excluding Queens, Manhattan and SI with 0% 'rat' violations)")
plt.show()


