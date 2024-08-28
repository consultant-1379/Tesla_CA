'''
Created on Oct 10, 2017

@author: ebrifol
'''

from xml.etree.ElementTree import ElementTree

def fileToXMLObject(xmlfile):
    '''Convert File to XML Object'''
    return ElementTree(file=xmlfile) 

def escape(text):
    '''return text that is safe to use in an XML string'''
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        ">": "&gt;",
        "<": "&lt;",
    }   
    return "".join(html_escape_table.get(c,c) for c in str(text))

def unescape(s):
    '''change XML string to text'''
    if s is None:
        s = ''
    
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&apos;", "'")
    s = s.replace("&quot;", '"')
    s = s.replace("&amp;", "&")
    return s 