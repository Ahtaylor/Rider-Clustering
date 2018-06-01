#!/usr/bin/env python3

# cluster.py

import numpy as np
import clusterfunc as cf

class Cluster
    riders = []
    location = ''
    driver = ''
    full = False

    def add_rider(self, newrider):
        if len(riders) >= 3:
            print("No more space for riders in this group")
        else:
            riders.append(newrider)
            print("There are now %r in %r" % (len(riders),self.name()))
            if len(riders) >= 3:
                full = True
    
    def has_driver(self):
        

    def is_full(self):
        return full
    
    def draw(self):
        plt.scatter()
        plt.plot()
