#!/usr/bin/env python3

# adjaceancy.py
# Functions to cluster people together based on distance.

import numpy as np
import numpy.ma as ma

def adjaceancy(riderlist):
    adj = np.empty((len(riderlist), len(riderlist)))
    for r1 in range(len(riderlist)):
        for r2 in range(r1 + 1):
            adj[r1,r2] = str(np.sqrt((riderlist[r1].get('x') - riderlist[r2].get('x'))**2 + ((riderlist[r1].get('y') - riderlist[r2].get('y'))**2)))
            adj[r2,r1] = adj[r1,r2]
            if r1 == r2:
                adj[r1,r2] = np.nan
    print(adj)
    return adj

def cluster(adj,riderlist):
    # initialize variables that will store cluster and keep track of clustering status
    num_rid = len(adj[0])
    num_ungrp = num_rid
    clus_size = 3
    clusters = []
    clus_ind = []
    clustered = False

    # Makes adj into a masked array so that elements can be masked and hidden for argmin search
    adj = ma.masked_array(adj)
    maskarr = ma.getmaskarray(adj)

    # intializes with each person in their own cluster, clus_ind follows the mutations of the
    # adjaceancy matrix
    for i in range(num_rid):
        clus_ind.append([i])
    
    # Additional variables that are used in the else case of the semiclustered conditional
    adjprime = np.copy(adj)
    indprime = clus_ind.copy()

    # Loop runs until all riders are in a cluster, ideally of more than 1 person
    while not clustered:
        semiclustered = maskarr.all()
        
        # By default nan are masked and any two clusters who sum of elements is greater than
        # 3 is masked. When all elements become masked then maskarr.all() returns true and 
        # then we move onto the else section of the loop.
        if not semiclustered:
            # finds the shortest distance, stores the coordinates, and constructs values for
            # what rows and columns to removed later
            short = np.nanargmin(adj)
            row = int(short//num_ungrp)
            column = int(short%num_ungrp)
            first = np.maximum(row,column)
            second = np.minimum(row,column)

            # Grouping indices in temp that correspond to specific riders, converts to names at
            # the end
            temp =[]
            for i in clus_ind[row]:
                temp.append(i)

            for i in clus_ind[column]:
                temp.append(i)

            # Removes lists that have been combined
            clus_ind.pop(first)
            clus_ind.pop(second)
   
            # creates array of values representing distance between new cluster and old clusters
            # Additionally, maskcomb is used to keep track of what values of combined should be
            # masked.
            combined = []
            maskcomb = []
            adj.mask = ma.nomask
            for i in range(num_ungrp):
                combined.append(np.maximum(adj[row][i],adj[column][i]))
                maskcomb.append(maskarr[row][i] or maskarr[column][i])
            combined.pop(first)
            combined.pop(second)
            maskcomb.pop(first)
            maskcomb.pop(second)
            combined = np.asarray(combined)
            maskcomb = np.asarray(maskcomb)

            # Deletes the old rows and columns of the recently combined clusters
            adj = np.delete(adj,first, axis=0)
            adj = np.delete(adj,first, axis=1)
            adj = np.delete(adj,second, axis=0)
            adj = np.delete(adj,second, axis=1)
            maskarr = np.delete(maskarr,first,axis=0)
            maskarr = np.delete(maskarr,first,axis=1)
            maskarr = np.delete(maskarr,second,axis=0)
            maskarr = np.delete(maskarr,second,axis=1)
    
            # If comdition is met then the cluster isn't full and it is put back into clus_ind
            # and adj. If it isn't met then temp is added to the cluster list and adjprime and
            # indprime are altered to account for those elements not being valid options if 
            # the semiclustered branch is entered.
            if len(temp) < clus_size:
                clus_ind.insert(0,temp)
                adj = np.insert(adj, 0, combined,axis=0)
                maskarr = np.insert(maskarr, 0, maskcomb, axis=0)
                combined = np.insert(combined,0, np.nan,axis=0)
                maskcomb = np.insert(maskcomb,0,True,axis=0)
                adj = np.insert(adj, 0, combined.transpose(),axis=1)
                maskarr = np.insert(maskarr, 0, maskcomb.transpose(), axis=1)
            else:
                clusters.append(temp)
                temp.sort(reverse=True)
                for i in temp:
                    loc = np.argwhere(np.asarray(indprime) == i)[0][0]
                    indprime.pop(loc)
                    adjprime = np.delete(adjprime,loc,axis=0)
                    adjprime = np.delete(adjprime,loc,axis=1)
                num_ungrp -= 1

            num_ungrp -= 1
    
            if num_ungrp <= 1:
                clustered = True
                if len(clus_ind) != 0: 
                    clusters.append(clus_ind[0])

            # Masks any values that represent connections between clusters with total number of
            # elements greater than clus_size (3)
            for i in range(num_ungrp):
                for j in range(num_ungrp):
                    if (len(clus_ind[i]) + len(clus_ind[j])) > clus_size:
                        maskarr[i,j] = True
                        maskarr[j,i] = True
            adj.mask = maskarr # Mask is reapplied for searching at the beginning of the loop
        
        else:
            print('Entered semicluster step')
            num_ungrp = len(indprime)
            
            # Search for shortest distance similary to before
            short = np.nanargmin(adjprime)
            row = int(short//num_ungrp)
            column = int(short%num_ungrp)
            first = np.maximum(row,column)
            second = np.minimum(row,column)
            
            # In this section each element of indprime will be a list of length 1 so a loop is
            # not necessary
            temp = []
            temp.append(indprime[row][0])
            temp.append(indprime[column][0])

            indprime.pop(first)
            indprime.pop(second)

            combined = []
            for i in range(num_ungrp):
                combined.append(np.maximum(adjprime[row][i],adjprime[column][i]))
            combined.pop(first)
            combined.pop(second)
            combined = np.asarray(combined)

            adjprime = np.delete(adjprime,first,axis=0)
            adjprime = np.delete(adjprime,first,axis=1)
            adjprime = np.delete(adjprime,second,axis=0)
            adjprime = np.delete(adjprime,second,axis=1)

            # Two are removed to accound for the two elements removed that will not be put back
            num_ungrp -= 2
            
            # Once two are clustered, a third or more depending on clus_size are clustered, so
            # long as the cluster is under the limit and there are elements left to cluster
            while (len(temp) < clus_size and len(indprime) > 0):
                short = np.nanargmin(combined)
                ele = int(short%num_ungrp)

                temp.append(indprime[ele][0])

                indprime.pop(ele)
                combined = np.delete(combined,ele,axis=0)
                adjprime = np.delete(adjprime,ele,axis=0)
                adjprime = np.delete(adjprime,ele,axis=1)

            clusters.append(temp)

            # Edge cases where indprime either has a leftover cluster of one person, or no one.
            if len(indprime) == 1:
                clusters.append(indprime[0][0])
                clustered = True
            elif len(indprime) == 0:
                clustered = True


    # converts list of list of indices, into list of list of names
    num_clus = len(clusters)
    
    print(clusters)
    for i in range(num_clus):
        for j in range(len(clusters[i])):
            clusters[i][j] = riderlist[clusters[i][j]]

    return clusters



def LocGrpMatch(Groups,PickupPoints):
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
    return Groups

            # Group is a list of lists (the original group of people from the
            # the clustering algorithm, plus the location)      
