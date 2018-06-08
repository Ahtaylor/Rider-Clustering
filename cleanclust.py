#!/usr/bin/env python3

import numpy as np
import numpy.ma as ma

adj = [[np.nan,1,1,50,50,50,100,100,100,100],[1,np.nan,1,50,50,50,100,100,100,100],[1,1,np.nan,50,50,50,100,100,100,100],[50,50,50,np.nan,1,1,100,100,100,100],[50,50,50,1,np.nan,1,100,100,100,100],[50,50,50,1,1,np.nan,100,100,100,100],[100,100,100,100,100,100,np.nan,1,100,100],[100,100,100,100,100,100,1,np.nan,100,100],[100,100,100,100,100,100,100,100,np.nan,1],[100,100,100,100,100,100,100,100,1,np.nan]]
adj = np.asarray(adj)

num_rid = len(adj[0])
num_ungrp = num_rid

clustered = False
clusters = []
clus_ind = []

adj = ma.masked_array(adj)
maskarr = ma.getmaskarray(adj)

print(adj)
print(maskarr)

for i in range(num_rid):
    clus_ind.append([i])
    adj[i,i] = ma.masked
    maskarr[i,i] = True


adjprime = np.copy(adj)
indprime = clus_ind.copy()
print(indprime)
#print(adj)
#print(maskarr)

#adj.mask = ma.nomask
#print(adj)

#adj.mask = maskarr
#print(adj)

while not clustered:
    print(maskarr)
    print(maskarr.all())
    semiclustered = maskarr.all()

    if not semiclustered:
        short = ma.argmin(adj)
        A = int(short//num_ungrp)
        B = int(short%num_ungrp)
        first = np.maximum(A,B)
        second = np.minimum(A,B)
    
        temp = []
        for i in clus_ind[A]:
            temp.append(i)
    
        for i in clus_ind[B]:
            temp.append(i)
        clus_ind.pop(first)
        clus_ind.pop(second)

        combined = []
        maskcomb = []
        adj.mask = ma.nomask
        for i in range(num_ungrp):
            combined.append(np.maximum(adj[A][i],adj[B][i]))
            maskcomb.append(maskarr[A][i] or maskarr[B][i])
        combined.pop(first)
        combined.pop(second)
        maskcomb.pop(first)
        maskcomb.pop(second)
#        print(combined)
        combined = np.asarray(combined)
        maskcomb = np.asarray(maskcomb)

#        print(combined)
#        print(maskcomb)
#        print(adj)
        
        adj = np.delete(adj,first,axis=0)
        adj = np.delete(adj,first,axis=1)
        adj = np.delete(adj,second,axis=0)
        adj = np.delete(adj,second,axis=1)
        maskarr = np.delete(maskarr,first,axis=0)
        maskarr = np.delete(maskarr,first,axis=1)
        maskarr = np.delete(maskarr,second,axis=0)
        maskarr = np.delete(maskarr,second,axis=1)

        if len(temp) < 3:
            clus_ind.insert(0,temp)
            adj = np.insert(adj, 0, combined, axis=0)
            maskarr = np.insert(maskarr, 0, maskcomb, axis=0)
            combined = np.insert(combined,0,np.nan,axis=0)
            maskcomb = np.insert(maskcomb,0,True,axis=0)
            adj = np.insert(adj,0,combined.transpose(),axis=1)
            maskarr = np.insert(maskarr,0,maskcomb.transpose(),axis=1)
        else:
            clusters.append(temp)
            temp.sort(reverse=True)
            print(temp)
            for i in temp:
                print(indprime)
                loc = np.argwhere(np.asarray(indprime) == i)[0][0]
                print(loc)

                indprime.pop(loc)
                adjprime = np.delete(adjprime,loc,axis=0)
                adjprime = np.delete(adjprime,loc,axis=1)
            num_ungrp -= 1

        adj.mask = maskarr
        num_ungrp -= 1
        print(adj)

        if num_ungrp <= 1:
            clustered = True
            if len(clus_ind) != 0:
                clusters.append(clus_ind[0])
                print(clusters)

        for i in range(num_ungrp):
            for j in range(num_ungrp):
                if (len(clus_ind[i]) + len(clus_ind[j])) > 3:    
                    maskarr[i,j] = True
                    maskarr[j,i] = True
        adj.mask = maskarr

    else:
        print('Entered semicluster step')
        num_ungrp = len(indprime)
        print(num_ungrp)
        short = np.nanargmin(adjprime)
        A = int(short//num_ungrp)
        B = int(short%num_ungrp)
        first = np.maximum(A,B)
        second = np.minimum(A,B)
        
        temp = []
        for i in indprime[A]:
            temp.append(i)

        for i in indprime[B]:
            temp.append(i)

        indprime.pop(first)
        indprime.pop(second)

        combined = []
        for i in range(num_ungrp):
            combined.append(np.maximum(adjprime[A][i],adjprime[B][i]))
        combined.pop(first)
        combined.pop(second)
        combined = np.asarray(combined)

        adjprime = np.delete(adjprime,first,axis=0)
        adjprime = np.delete(adjprime,first,axis=1)
        adjprime = np.delete(adjprime,second,axis=0)
        adjprime = np.delete(adjprime,second,axis=1)
        
        num_ungrp -= 2

        while (len(temp) < 3 and len(indprime) > 1):
            print(temp)
            print(indprime)
            print(combined)
            short = np.nanargmin(combined)
            ele = int(short%num_ungrp)
            
            temp.append(indprime[ele][0])

            indprime.pop(ele)
            combined = np.delete(combined,ele,axis=0)
            adjprime = np.delete(adjprime,ele,axis=0)
            adjprime = np.delete(adjprime,ele,axis=1)

        clusters.append(temp)

        if len(indprime) == 1:
            clusters.append(indprime[0][0])
            clustered = True
        elif len(indprime) == 0:
            clustered = True

        print('Exited semicluster section')
       
print(clusters)
