'''
Created on Nov 2, 2017

@author: ebrifol
'''

import os

class Git_interface(object):
    '''
    classdocs
    '''
    
    def __init__(self, destination):
        self.destination = destination
        os.chdir(destination)
    

    def clone(self, Repository):
        return os.system('git clone ' + Repository)
    
    def addAll(self):
        return os.system('git add . ')
    
    def commit(self, commitMessage):
        return os.system('git commit -a -m "' + commitMessage + '" ')
    
    def push(self):
        return os.system('git push')
    
    def pull(self):
        return os.system('git pull')