'''
Created on Mar 7, 2018

@author: ebrifol
'''

from datetime import datetime

class Print_formatter(object):

    def __init__(self):
        self.PINK = '\033[95m'
        self.BLUE = '\033[94m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
    
    def Green(self, message, end):
        self._printMessage(self.GREEN + self.BOLD, message, end)
    
    def White(self, message, end):
        self._printMessage(self.BOLD, message, end)
        
    def Yellow(self, message, end):
        self._printMessage(self.YELLOW + self.BOLD, message, end)
    
    def Pink(self, message, end):
        self._printMessage(self.PINK + self.BOLD, message, end)
    
    def Blue(self, message, end):
        self._printMessage(self.BLUE + self.BOLD, message, end)
    
    def Red(self, message, end):
        self._printMessage(self.RED + self.BOLD, message, end)
    
    def _printMessage(self, format, message, end):
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print format + time + '' + message
        if end:
            print self.ENDC
        
        