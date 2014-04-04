'''
Created on 4 avr. 2014

@author: Olivier Stroesser
'''

class DatabaseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)     