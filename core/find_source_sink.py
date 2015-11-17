__author__ = 'Phreak'
"""
I am addicted to the way I feel when I think of YoU.
I wish I could do EvrYthNG on Earth with YoU.
"""
# !/usr/bin/env python
import re
from os import path
from lib.file_functions import FileFunctions
from core.global_variable import Global
from bs4 import BeautifulSoup

class FindSourceSink(Global):
    def __init__(self):
        self.sources_match_lines = []
        self.sinks_match_lines = []

####################################################################################
    def analysis_html(self, file_path):
        file_functions_object = FileFunctions()
        result_file = path.join(Global.create_current_result_dir , "source_sink_result.txt")

        SOURCES_RE = re.compile("""(location\s*[\[.])|([.\[]\s*["']?\s*(arguments|dialogArguments|innerHTML|open(Dialog)?|showModalDialog|cookie|URL|documentURI|baseURI|referrer|name|opener|parent|top|content|self|frames)\W)|(localStorage|sessionStorage|Database)""")
        SINKS_RE = re.compile("""((src|href|data|location|code|value|action)\s*["'\]]*\s*\+?\s*=)|([.\[]\s*["']?\s*(innerHTML|appendChild\W))|((replace|assign|navigate|getResponseHeader|innerHTML|write(ln)?|open(Dialog)?|showModalDialog|eval|evaluate|execCommand|execScript|setTimeout|setInterval)\s*["'\]]*\s*\()""")

        sources_dict = {}
        sinks_dict = {}
        self.sources_match_lines = []
        self.sinks_match_lines = []


        source_sink_depends_on_position = ["innerHTML"]

        try:

            with open(file_path,'r') as f:
                dat = f.read()

            soup = BeautifulSoup(dat, 'html.parser')
            for javascript in soup.find_all('script'):
                oldest_data = javascript.string

                for line in oldest_data.split("\n"):
                    for pattern in re.findall(SOURCES_RE, line):
                        for match in pattern:
                            match = match.strip()
                            if len(match) > 0:

                                line_number = 0
                                for key, value in Global.all_file_line_and_number.iteritems():
                                    if str(line.strip()) == str(value.strip()):
                                        line_number = int(key)
                                        break

                                if not line_number:
                                    print "Something went wrong"
                                    continue

                                if line_number in sources_dict:
                                    if match not in sources_dict[line_number]:

                                        position_flag = 0
                                        for entry in source_sink_depends_on_position:
                                            if entry in match and "=" in line:
                                                position_flag = 1
                                                break

                                        if position_flag:
                                            right_part = line.split("=")[-1]
                                            if entry in right_part:
                                                data = "Source Match pattern found {0} at line {1}\n".format(match, line_number)
                                                file_functions_object.appendFile(data, result_file)
                                                sources_dict[line_number] = str(sources_dict[line_number]) + match
                                                if line_number not in self.sources_match_lines:
                                                    self.sources_match_lines.append(line_number)

                                        else:
                                            data = "Source Match pattern found {0} at line {1}\n".format(match, line_number)
                                            file_functions_object.appendFile(data, result_file)
                                            sources_dict[line_number] = str(sources_dict[line_number]) + match
                                            if line_number not in self.sources_match_lines:
                                                self.sources_match_lines.append(line_number)


                                else:
                                    position_flag = 0
                                    for entry in source_sink_depends_on_position:
                                        if entry in match and "=" in line:
                                            position_flag = 1
                                            break

                                    if position_flag:
                                        right_part = line.split("=")[-1]
                                        if entry in right_part:
                                            data = "Source Match pattern found {0} at line {1}\n".format(match, line_number)
                                            file_functions_object.appendFile(data, result_file)
                                            sources_dict[line_number] = match
                                            if line_number not in self.sources_match_lines:
                                                self.sources_match_lines.append(line_number)

                                    else:
                                        data = "Source Match pattern found {0} at line {1}\n".format(match, line_number)
                                        file_functions_object.appendFile(data, result_file)
                                        sources_dict[line_number] = match
                                        if line_number not in self.sources_match_lines:
                                            self.sources_match_lines.append(line_number)




                    for pattern in re.findall(SINKS_RE, line):
                        for match in pattern:
                            match = match.strip()
                            if len(match) > 0:

                                line_number = 0
                                for key, value in Global.all_file_line_and_number.iteritems():
                                    """
                                    print line.strip()
                                    print value.strip()
                                    raw_input()
                                    """
                                    if str(line.strip()) == str(value.strip()):
                                        line_number = int(key)
                                        break

                                if not line_number:
                                    print "Something went wrong"
                                    continue

                                if line_number in sinks_dict:
                                    if match not in sinks_dict[line_number]:

                                        position_flag = 0
                                        for entry in source_sink_depends_on_position:
                                            if entry in match and "=" in line:
                                                position_flag = 1
                                                break

                                        if position_flag:
                                            left_part = line.split("=")[0]
                                            if entry in left_part:

                                                data = "Sink Match pattern found {0} at line {1}\n".format(match, line_number)
                                                file_functions_object.appendFile(data, result_file)
                                                sinks_dict[line_number] = str(sinks_dict[line_number]) + match
                                                if line_number not in self.sinks_match_lines:
                                                    self.sinks_match_lines.append(line_number)

                                        else:
                                            data = "Sink Match pattern found {0} at line {1}\n".format(match, line_number+1)
                                            file_functions_object.appendFile(data, result_file)
                                            sinks_dict[line_number] = str(sinks_dict[line_number]) + match
                                            if line_number not in self.sinks_match_lines:
                                                self.sinks_match_lines.append(line_number)
                                else:
                                    position_flag = 0
                                    for entry in source_sink_depends_on_position:
                                        if entry in match and "=" in line:
                                            position_flag = 1
                                            break

                                    if position_flag:
                                        left_part = line.split("=")[0]
                                        if entry in left_part:
                                            data = "Sink Match pattern found {0} at line {1}\n".format(match, line_number)
                                            file_functions_object.appendFile(data, result_file)
                                            sinks_dict[line_number] = match
                                            if line_number not in self.sinks_match_lines:
                                                    self.sinks_match_lines.append(line_number)

                                    else:
                                        data = "Sink Match pattern found {0} at line {1}\n".format(match, line_number)
                                        file_functions_object.appendFile(data, result_file)
                                        sinks_dict[line_number] = match
                                        if line_number not in self.sinks_match_lines:
                                                self.sinks_match_lines.append(line_number)
        except:
            pass

        self.inserting_alert(file_path)

        return 0

####################################################################################
    def inserting_alert(self, file_path):
        file_functions_object = FileFunctions()

        with open(file_path,'r') as f:
            dat = f.read()

        Global.number_of_alerts = 0
        new_data = []
        file_name = file_path.split("/")[-1]
        #print file_name
        all_javascript_variables_values = Global.all_javascript_variables[file_name]
        #print all_javascript_variables_values

        for line_number, line in enumerate(dat.split("\n")):
            line_number += 1
            if line_number in self.sinks_match_lines:

                for var in all_javascript_variables_values:
                    if var in line:
                        new_line = "alert({0});".format(var)
                        #new_line = "alert(JSON.parse({0}));".format(var)
                        #new_line = "console.log({0});".format(var)
                        Global.number_of_alerts = Global.number_of_alerts + 1
                        new_data.append(new_line)
                    else:
                        pass

            new_data.append(line)

        file_functions_object.writeArrayToFileReplaceOld(new_data, file_path)

        return 0

####################################################################################
    def analysis_js(self, file_path):

        file_functions_object = FileFunctions()
        result_file = path.join(Global.create_current_result_dir , "source_sink_result.txt")

        SOURCES_RE = re.compile("""(location\s*[\[.])|([.\[]\s*["']?\s*(arguments|dialogArguments|innerHTML|open(Dialog)?|showModalDialog|cookie|URL|documentURI|baseURI|referrer|name|opener|parent|top|content|self|frames)\W)|(localStorage|sessionStorage|Database)""")
        SINKS_RE = re.compile("""((src|href|data|location|code|value|action)\s*["'\]]*\s*\+?\s*=)|([.\[]\s*["']?\s*(innerHTML|appendChild\W))|((replace|assign|navigate|getResponseHeader|innerHTML|write(ln)?|open(Dialog)?|showModalDialog|eval|evaluate|execCommand|execScript|setTimeout|setInterval)\s*["'\]]*\s*\()""")

        self.sources_match_lines = []
        self.sinks_match_lines = []

        file_name = file_path.split("/")[-1]

        source_sink_depends_on_position = ["innerHTML"]

        try:

            fp = open(file_path)
            for line_number, line in enumerate(fp):
                line_number += 1
                for pattern in re.findall(SOURCES_RE, line):
                    for match in pattern:
                        match = match.strip()
                        if len(match) > 0:

                            position_flag = 0
                            for entry in source_sink_depends_on_position:
                                if entry in match and "=" in line:
                                    position_flag = 1
                                    break

                            if position_flag:
                                right_part = line.split("=")[-1]
                                if entry in right_part:
                                    if line_number not in self.sources_match_lines:
                                        self.sources_match_lines.append(line_number)
                                        data = "Source Match pattern found {0} at line {1} in file {2}\n".format(match, line_number, file_name)
                                        file_functions_object.appendFile(data, result_file)

                                    else:
                                        if line_number not in self.sources_match_lines:
                                            self.sources_match_lines.append(line_number)
                                            data = "Source Match pattern found {0} at line {1} in file {2}\n".format(match, line_number, file_name)
                                            file_functions_object.appendFile(data, result_file)


                            else:
                                position_flag = 0
                                for entry in source_sink_depends_on_position:
                                    if entry in match and "=" in line:
                                        position_flag = 1
                                        break

                                if position_flag:
                                    right_part = line.split("=")[-1]
                                    if entry in right_part:
                                        if line_number not in self.sources_match_lines:
                                            self.sources_match_lines.append(line_number)
                                            data = "Source Match pattern found {0} at line {1} in file {2}\n".format(match, line_number, file_name)
                                            file_functions_object.appendFile(data, result_file)

                                else:
                                    if line_number not in self.sources_match_lines:
                                        self.sources_match_lines.append(line_number)
                                        data = "Source Match pattern found {0} at line {1} in file {2}\n".format(match, line_number, file_name)
                                        file_functions_object.appendFile(data, result_file)




                for pattern in re.findall(SINKS_RE, line):
                    for match in pattern:
                        match = match.strip()
                        if len(match) > 0:
                            position_flag = 0
                            for entry in source_sink_depends_on_position:
                                if entry in match and "=" in line:
                                    position_flag = 1
                                    break

                            if position_flag:
                                left_part = line.split("=")[0]
                                if entry in left_part:
                                    if line_number not in self.sinks_match_lines:
                                        #print line
                                        #print line_number
                                        #raw_input()
                                        self.sinks_match_lines.append(line_number)
                                        data = "Sink Match pattern found {0} at line {1} in file {2}\n".format(match, line_number, file_name)
                                        file_functions_object.appendFile(data, result_file)

                            else:
                                if line_number not in self.sinks_match_lines:
                                    #print line
                                    #print line_number
                                    #raw_input()
                                    self.sinks_match_lines.append(line_number)
                                    data = "Sink Match pattern found {0} at line {1} in file {2}\n".format(match, line_number+1, file_name)
                                    file_functions_object.appendFile(data, result_file)

                        """
                        else:
                            position_flag = 0
                            for entry in source_sink_depends_on_position:
                                if entry in match and "=" in line:
                                    position_flag = 1
                                    break

                            if position_flag:
                                left_part = line.split("=")[0]
                                if entry in left_part:
                                    if line_number not in self.sinks_match_lines:
                                        self.sinks_match_lines.append(line_number)
                                        data = "Sink Match pattern found {0} at line {1} in file {2}\n".format(match, line_number, file_name)
                                        file_functions_object.appendFile(data, result_file)

                            else:
                                if line_number not in self.sinks_match_lines:
                                    self.sinks_match_lines.append(line_number)
                                    data = "Sink Match pattern found {0} at line {1} in file {2}\n".format(match, line_number, file_name)
                                    file_functions_object.appendFile(data, result_file)
                        """
        except:
            pass

        #print self.sinks_match_lines

        self.inserting_alert(file_path)

        return 0


