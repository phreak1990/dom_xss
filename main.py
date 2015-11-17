__author__ = 'Phreak'
"""
I am addicted to the way I feel when I think of YoU.
I wish I could do EvrYthNG on Earth with YoU.
"""
# !/usr/bin/env python

from os import system,path,mkdir
import sys
from core.global_variable import Global
from datetime import datetime
from attack.main_script import MainScript
from lib.file_functions import FileFunctions

class Main:
    def __init__(self, url):
        self.url = url

####################################################################################
    def manage_result_dir(self):

        Global.result_dir =  path.join(path.dirname(path.abspath(sys.argv[0])), "results")
        if not path.isdir(Global.result_dir):
            mkdir(Global.result_dir)

        current_time = "_".join(str(datetime.now()).split(" "))
        current_project_name =  current_time

        Global.create_current_result_dir = path.join(Global.result_dir, current_project_name)

        if not path.isdir(Global.create_current_result_dir):
            mkdir(Global.create_current_result_dir)

        result_file = path.join(Global.create_current_result_dir , "source_sink_result.txt")
        file_functions_object = FileFunctions()
        file_functions_object.writeFile("",result_file)


####################################################################################
    def main_script(self):
        main_script_object = MainScript(self.url)
        main_script_object.attack()



####################################################################################

if __name__ == '__main__':
    system("clear")
    if len(sys.argv) < 2:
        print "Usage: python main.py <url>"
        print ""
        sys.exit(1)

    x = Main(str(sys.argv[1]))
    x.manage_result_dir()
    x.main_script()