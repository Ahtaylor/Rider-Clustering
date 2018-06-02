#!/usr/bin/env python3

import numpy as np
from numpy.random import random as rng
import os
import matplotlib.pyplot as plt

################### Get Input and Clear Old Data (TempDat) ###################

riders=int( input("\nThe purpose of this is to generate random points\n" \
	"How many points do you want? (keep 26 and under for now): "))

pickup= int(input("\nHow many pickup locations do you want? (26 and under): "))

os.system("rm TempDat* -f")

##############################################################################
################          Creating Rider File              ###################
##############################################################################


riders_file = 'TempDatRiders.csv'


riders_name = []
for i in range(riders):
	riders_name.append(chr(i+97))
riders_x = 10*rng(riders)
riders_y = 10*rng(riders)


for i in range(riders):

	newline = 'echo '+str(riders_name[i])+','+str(riders_x[i])+','+str(riders_y[i])+' >> '+riders_file
	os.system(newline)

##############################################################################
################         Creating Pickup File              ###################
##############################################################################

pickup_file = 'TempDatPickup.csv' 

pickup_name = []
for i in range(pickup):
        pickup_name.append(chr(i+65))
pickup_x = 10*rng(pickup)
pickup_y = 10*rng(pickup)


for i in range(pickup):

        newline = 'echo '+str(pickup_name[i])+','+str(pickup_x[i])+','+str(pickup_y[i])+' >> '+pickup_file
        os.system(newline)


print("\nData files have been saved in this directory. \nShowing Plot (Plot not saved automatically) ")

##############################################################################
################              Creating Plot                ###################
##############################################################################

plt.plot(riders_x,riders_y,color='blue',marker='.',linestyle='None')
plt.plot(pickup_x,pickup_y,color='orange',marker='o',linestyle='None')

plt.show()

#### To Be Continued

