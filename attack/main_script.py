__author__ = 'Phreak'
"""
I am addicted to the way I feel when I think of YoU.
I wish I could do EvrYthNG on Earth with YoU.
"""

# !/usr/bin/env python
from core.global_variable import Global
from core.get_url_data import GetUrlData
from os import walk,path
from core.find_source_sink import FindSourceSink
from attack.selenium_test import SeleniumTest


class MainScript(Global):
    def __init__(self, url):
        self.url = url

####################################################################################
    def attack(self):
        self.first_time()

        find_source_sink_object = FindSourceSink()
        selenium_test_object = SeleniumTest()

        for dirName, subDir, files in walk(Global.create_current_result_dir):
            for file in files:
                file_path = path.join(Global.create_current_result_dir, file)
                try:
                    if file_path.split('.')[-1] == "js":
                        find_source_sink_object.analysis_js(file_path)

                except:
                    pass

            for file in files:
                #print file
                file_path = path.join(Global.create_current_result_dir, file)
                try:
                    if file_path.split('.')[-1] == "html":
                        find_source_sink_object.analysis_html(file_path)
                        #find_source_sink_object.inserting_alert(file_path)
                        print "Testing for DOM XSS through Selenium...MaSter"
                        selenium_test_object.selenium_test(file_path)
                        break

                except:
                    pass

            break
        return 0


####################################################################################
    def first_time(self):
        get_url_data_object = GetUrlData()
        get_url_data_object.first_time(self.url)
        get_url_data_object.fetch_js_file_data()
        del get_url_data_object