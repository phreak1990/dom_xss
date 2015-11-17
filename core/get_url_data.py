__author__ = 'Phreak'
"""
I am addicted to the way I feel when I think of YoU.
I wish I could do EvrYthNG on Earth with YoU.
"""

# !/usr/bin/env python
from core.global_variable import Global

from sys import exit
import requests
from lib.file_functions import FileFunctions
from os import path
from bs4 import BeautifulSoup
import jsbeautifier

class GetUrlData(Global):
    def __init__(self):
        self.file_functions_object = FileFunctions()

####################################################################################
    def first_time(self, url, current_file_name=None):
        r = requests.get(url)
        html_data = r.text

        if current_file_name:
            current_file_path = path.join(Global.create_current_result_dir, current_file_name)
        else:
            current_file_name = "main.html"
            current_file_path = path.join(Global.create_current_result_dir, current_file_name)

        all_variable_in_file = []
        Global.all_js_file_path = []

        soup = BeautifulSoup(html_data, 'html.parser')
        for javascript in soup.find_all('script'):

            if not javascript is None:
                value = javascript.get("src")
                if value:
                    if value not in Global.all_js_file_path:
                        Global.all_js_file_path.append(value)
                        file_name = value.split("/")[-1]
                        javascript["src"] = file_name


            oldest_data = javascript.string
            if oldest_data:
                #removed_space = oldest_data.strip()
                #all_lines_in_script_tag = removed_space.split(";")

                #new_formatted_data =  "\n" + ";\n".join(all_lines_in_script_tag)
                new_formatted_data = jsbeautifier.beautify(oldest_data)
                javascript.string = new_formatted_data

                for line in new_formatted_data.split("\n"):
                    line = str(line.strip())
                    if len(line) > 1:
                        try:
                            check_for_single_line_comment = line[0] + line[1]
                        except IndexError:
                            print "Error Found in checking single line comment"

                        if check_for_single_line_comment == "//":
                            for internal_line in line.split("\n"):
                                internal_line = internal_line.replace("\t", "").replace("\r", "")
                                if len(internal_line.strip()) > 1:
                                    check_for_single_line_comment = internal_line.strip()[0] + line.strip()[1]
                                    if not check_for_single_line_comment == "//":

                                        if "=" in internal_line:
                                            left_part = internal_line.split("=")[0]
                                            if "var" in left_part:
                                                try:
                                                    clear_keyword = left_part[left_part.index("var")+3:].strip()

                                                except ValueError:
                                                    print "error"
                                                    print line
                                                    continue

                                                finally:
                                                    for variable_name in clear_keyword.split(","):
                                                        if variable_name not in all_variable_in_file:
                                                            if len(variable_name) > 0:
                                                                    all_variable_in_file.append(clear_keyword)
                                    else:
                                        continue
                                else:
                                    continue
                        else:
                            if "=" in line:
                                line = line.strip().replace("\t", "").replace("\r", "")
                                left_part = line.split("=")[0]
                                if "var" in left_part:
                                    try:
                                        clear_keyword = left_part[left_part.index("var")+3:].strip()

                                    except ValueError:
                                        print "error"
                                        print line
                                        continue

                                    finally:
                                        for variable_name in clear_keyword.split(","):
                                            if variable_name not in all_variable_in_file:
                                                if len(variable_name) > 0:
                                                        all_variable_in_file.append(clear_keyword)


        #print len(all_variable_in_file)
        #raw_input()

        #print Global.all_js_file_path

        Global.all_javascript_variables[current_file_name] = all_variable_in_file
        #print Global.all_javascript_variables

        new_html_data = soup.prettify(formatter="html")
        #print current_file_path
        self.file_functions_object.writeFile(new_html_data, current_file_path)


        all_lines = new_html_data.split("\n")
        counter = 1
        for line in all_lines:
            Global.all_file_line_and_number[counter] = line + "\n"
            counter += 1

        return 0


####################################################################################
    def fetch_js_file_data(self):
        for url_path in Global.all_js_file_path:
            js_file_name = url_path.split("/")[-1]

            current_file_path = path.join(Global.create_current_result_dir, js_file_name)

            r = requests.get(url_path)
            js_data = r.text

            #print url_path

            new_formatted_data = jsbeautifier.beautify(js_data)


            all_variable_in_file = []

            #removed_space = js_data.strip()
            #all_lines_in_script_tag = removed_space.split(";")

            #new_formatted_data =  "\n" + ";\n".join(all_lines_in_script_tag)

            for line in new_formatted_data.split("\n"):
                try:
                    line = str(line.strip())
                except UnicodeEncodeError:
                    line = line.encode('utf-8').strip()

                if len(line) > 1:
                    try:
                        check_for_single_line_comment = line[0] + line[1]
                    except IndexError:
                        print "Error Found in checking single line comment"

                    if check_for_single_line_comment == "//":
                        for internal_line in line.split("\n"):
                            internal_line = internal_line.replace("\t", "").replace("\r", "")
                            if len(internal_line.strip()) > 1:
                                check_for_single_line_comment = internal_line.strip()[0] + line.strip()[1]
                                if not check_for_single_line_comment == "//":

                                    if "=" in internal_line:
                                        left_part = internal_line.split("=")[0]
                                        if "var" in left_part:
                                            try:
                                                clear_keyword = left_part[left_part.index("var")+3:].strip()

                                            except ValueError:
                                                print "error"
                                                print line
                                                continue

                                            finally:
                                                for variable_name in clear_keyword.split(","):
                                                    if variable_name not in all_variable_in_file:
                                                        #print line
                                                        #print variable_name.strip()
                                                        #raw_input()
                                                        all_variable_in_file.append(variable_name.strip())

                                else:
                                    continue
                            else:
                                continue
                    else:
                        if "=" in line:
                            line = line.strip().replace("\t", "").replace("\r", "")
                            left_part = str(line.split("=")[0])
                            if "var" in left_part:
                                try:
                                    clear_keyword = left_part[left_part.index("var")+3:].strip()

                                except ValueError:
                                    print "error"
                                    print line
                                    continue

                                finally:
                                    for variable_name in clear_keyword.split(","):
                                        if variable_name not in all_variable_in_file:
                                            #print line
                                            #print variable_name.strip()
                                            #raw_input()
                                            all_variable_in_file.append(variable_name.strip())


            Global.all_javascript_variables[js_file_name] = all_variable_in_file
            #print Global.all_javascript_variables[js_file_name]


            self.file_functions_object.writeFile(new_formatted_data, current_file_path)

        return 0


