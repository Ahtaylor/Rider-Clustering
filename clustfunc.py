#!/usr/bin/env python3

# adjaceancy.py
# Functions to cluster people together based on distance.

import numpy as np

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

def buildcluster(adj):
    clusters = []
    
    short = np.nanargmin(adj)
    loc = (short//5, short%5)

    
    return loc
