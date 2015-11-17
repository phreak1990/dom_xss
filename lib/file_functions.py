#!/usr/bin/env python
from os import path
from sys import argv
import sys


class FileFunctions: 
    def __init__(self):
        pass

####################################################################################
    def readFile(self, file_path):
        if path.exists (file_path):
            fo = open(file_path,"r")
            data = fo.read()
            fo.close()
            return data
        else:
            return None
        
####################################################################################
    def writeFile(self, data, file_path):
        fo = open(file_path,"w")
        try:
            fo.write(data)
        except UnicodeEncodeError:
            fo.write(data.encode('utf-8'))
        fo.close()
            
####################################################################################
    def appendFile(self,data, file_path):
        if path.exists (file_path):
            fo = open(file_path,"a+")
            fo.write(data)
            fo.close()
        
####################################################################################
    def currentPath(self):
        pathname = path.dirname(argv[0])
        full_path = path.abspath(pathname)
        return full_path
    
####################################################################################
    def writeArrayToFile(self, array, file_path):
        if not path.exists (file_path):
            fo = open(file_path ,"w")
            save_stdout = sys.stdout
            sys.stdout = fo
            for line in array:
                print line
            fo.close()
            sys.stdout = save_stdout

####################################################################################
    def writeArrayToFileReplaceOld(self, array, file_path):
        fo = open(file_path ,"w")
        save_stdout = sys.stdout
        sys.stdout = fo
        for line in array:
            print line
        fo.close()
        sys.stdout = save_stdout
            
####################################################################################
    def appendArrayToFile(self, array, file_path):
        fo = open(file_path ,"a+")
        save_stdout = sys.stdout
        sys.stdout = fo
        for line in array:
            print line
        fo.close()
        sys.stdout= save_stdout

####################################################################################
    def readFileIntoArray(self, file_path):
        array = []
        if path.exists (file_path):
            with open(file_path) as fo:
                for line in fo:
                    line = line.replace("\n","")
                    array.append(line)
            fo.close()
            return array
        else:
            return None

####################################################################################
    def appendFileWithHashes(self,data, file_path):
        if path.exists (file_path):
            fo = open(file_path,"a+")
            save_stdout = sys.stdout
            sys.stdout = fo
            print ""
            print "############################################################################"
            print data
            sys.stdout = save_stdout
            fo.close()

####################################################################################
