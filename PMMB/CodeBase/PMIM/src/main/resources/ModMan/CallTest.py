'''
Created on 20 Feb 2018

@author: xarjsin
'''

class Call_Testware(object):
    '''
    Calls the testware methods which will run tests on the input model
    '''
    Input ={'blah'}


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    
    def getInputs(self):
        return self.Input
    
    def runBackground(self,params):
        print __name__
        