#!/usr/bin/env python3

import csv
import numpy as np
from clustfunc import * 




##### STEP 1 #####

###################     Make Riders dictionary     ##########################
# Function: converts two csv files into two two separate lists of dictionaries
# These dictionaries are assigned to the variable name
# Input: two csv files stored in current directory
# Output: two lists of dictionaries, one is each rider
#   the other is each location
#       ex: [a,b,c,d,e,f,g]     [A,B,C,D]
#    rider names (lowercase)   Location names (Upper Case)
with open('going.csv') as f0:
	readCSV0 = csv.reader(f0,delimiter=',')

	going = []

	for line in readCSV0:
		if line[2]=='yes':
			going.append(line[1])

with open('MasterExample.csv') as f1:
	readCSV1 = csv.reader(f1,delimiter=',')

	riders = []
	
	for rider in readCSV1:
		if rider[1] in going:

			riders.append({'name':rider[2],'y':float(rider[3]),'x':float(rider[4]),'email':rider[1]})


	print("riders",riders)

	for rider in riders:
		name = rider['name']
		vars()[name] = rider
#	print(a)
#	print(a['x'],a['name'])
#	print(riders)	
### Very ugly, but it assigns the variable name of the dictionary to the dict.
###################     Make Pickup Point Dictionaries     ##################
with open('Locations.csv') as f2:
	readCSV2 = csv.reader(f2,delimiter=',')

	locations = []

	for location in readCSV2:
	
		locations.append({'name':location[0],'y':float(location[1]),'x':float(location[2])})

	for location in locations:
		name = location['name']
		vars()[name] = location


adj = adjaceancy(riders)

cluster = cluster(adj,riders)

Groups = LocGrpMatch(cluster,locations)

for Group in Groups:
	for i in Group:
		print(i['name'])
	print()


