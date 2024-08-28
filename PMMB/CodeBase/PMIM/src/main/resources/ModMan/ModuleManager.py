'''
Created on Mar 15, 2018

@author: ebrifol
'''

import inspect

class ModuleManager(object):
    
    def __init__(self):
        self.modules = ['Parsers']
    
    def describeModules(self, module_name=None):
        if module_name is not None:
            return self.describe(module_name)
        else:
            docs = {}
            for module in self.modules:
                docs[module] = self.describe(module)
            return docs
    
    def describe(self, module_name):
        docs = {}
        
        mod = __import__(module_name)
        for name, obj in inspect.getmembers(mod):
            if inspect.isclass(obj) and getattr(obj, '__module__').startswith(module_name):
                doc = getattr(obj, '__doc__')
                if doc is None:
                    doc = 'No documentation available'
                
                docs[name] = doc.strip() 
        
        return docs
    
    def executeMethod(self, class_name, method_name, params):
        for module in self.modules:
            mod = __import__(module)
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                if name == class_name:
                    return getattr(obj(params), method_name)()
    
