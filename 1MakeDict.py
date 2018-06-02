#!/usr/bin/env python3

import csv

##### STEP 1 #####

###################     Make Riders dictionary     ##########################
# Function: converts two csv files into two two separate lists of dictionaries
# These dictionaries are assigned to the variable name
# Input: two csv files stored in current directory
# Output: two lists of dictionaries, one is each rider
#   the other is each location
#       ex: [a,b,c,d,e,f,g]     [A,B,C,D]
#    rider names (lowercase)   Location names (Upper Case)


with open('SampleRiders.csv') as f1:
	readCSV1 = csv.reader(f1,delimiter=',')

	riders = []
	
	for rider in readCSV1:

		riders.append({'name':rider[0],'x':rider[1],'y':rider[2]})



	for rider in riders:
		name = rider['name']
		vars()[name] = rider
#	print(a)
#	print(a['x'],a['name'])
#	print(riders)	
### Very ugly, but it assigns the variable name of the dictionary to the dict.
###################     Make Pickup Point Dictionaries     ##################
with open('SamplePickup.csv') as f2:
	readCSV2 = csv.reader(f2,delimiter=',')

	locations = []

	for location in readCSV2:
	
		locations.append({'name':location[0],'x':location[1],'y':location[2]})

	for location in locations:
		name = location['name']
		vars()[name] = location	
#	print(locations)


### The following is written independantly as LocGrpMatch.py
"""
########################################################################
###### Dictionaries made, match location to group########################
########################################################################

Groups = [[a,b,c],[d,e], [f,g]]

PickupPoints = [A,B,C,D]

for Group in Groups:
	xtot = 0
	ytot = 0
	for i in Group:	
		xtot += float(i['x'])
		ytot += float(i['y'])
		xcenter = xtot/len(Group)
		ycenter = ytot/len(Group)
								# The above finds the epicenter of the group
	FinalPickupDisp = [9999999]
	FinalPickupName = ['Filler']
								# "empty" lists, My strategy here was to find
								# find the net displacement of each possible
								# pickup point to the group's epicenter.
								# I needed both information, the total distance
								# and the actual name of the pickup point.
								# My strategy was to find the displacement for
								# each point, and if that was smaller than the
								# displacement of any other already in the list
								# then it will be appended (i.e. the last point
								# listed will always be the closest)
	for PickupPoint in PickupPoints:
		LocX = float(PickupPoint['x'])
		LocY = float(PickupPoint['y'])
		xdisp = LocX-xcenter
		ydisp = LocY-ycenter
		disp = xdisp**2 + ydisp**2
		if disp < min(FinalPickupDisp):
			FinalPickupDisp.append(disp)
			FinalPickupName.append(PickupPoint)
	Group.append(FinalPickupName[-1])
								# The closest point is the last item, so I
								# append that to the group of people. 
								# since 'name' is a common element to both the
								# people list and the location list, I print
								# the 'name' elements of all the items
	for i in Group:
		print (i['name'])
	print("\n\n\n")	


"""


# The following is scrap work, to be continued

"""

##############################################################################
########################### Plot at pickup location ##########################
##############################################################################	

from matplotlib.pyplot import *

figure, ax = subplots()

X_range = []
for Group in Groups:
	X_range.append(float(Group[-1]['x']))	

print (X_range)

Y_range = []
for Group in Groups:
	Y_range.append(float(Group[-1]['y']))
print (Y_range)
"""
