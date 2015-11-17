__author__ = 'Phreak'
"""
I am addicted to the way I feel when I think of YoU.
I wish I could do EvrYthNG on Earth with YoU.
"""

# !/usr/bin/env python
from core.global_variable import Global
from selenium import webdriver
from lib.string_and_array_functions import StingAndArrayFunctions
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException



class SeleniumTest(Global):
    def __init__(self):
        self.number_of_variable_in_generated_url = 7

####################################################################################
    def selenium_test(self, path):

        random_digit_alpha = StingAndArrayFunctions()

        dict_key = path.split("/")[-1]
        #print path

        d = DesiredCapabilities.FIREFOX
        d['loggingPrefs'] = {'browser': 'ALL'}

        driver = webdriver.Firefox(capabilities=d)
        driver.implicitly_wait(10)

        new_url = "file://" + path + "/"

        counter = 0
        random_value_container = []
        query = ""

        for var in Global.all_javascript_variables[dict_key]:
            random_value = random_digit_alpha.randDigitAlpha(8)
            query = query + var + "=" + random_value + "&"
            random_value_container.append(random_value)
            counter = counter + 1

            if counter == self.number_of_variable_in_generated_url:
                #print "Counter value {0}".format(counter)
                new_url = new_url + "?" + query
                random_value = random_digit_alpha.randDigitAlpha(8)
                random_value_container.append(random_value)
                new_url = new_url + "#" + random_value
                driver.get(new_url)

                #print "in upper if {0}".format(new_url)

                counter = 0
                random_value_container = []
                query = ""
                new_url = "file://" + path + "/"


                try:
                    for x in range(Global.number_of_alerts):

                        try:

                            alert_object = driver.switch_to.alert
                            alert_value = alert_object.text
                            #print "alert value is {0}".format(alert_value)
                        except NoAlertPresentException, UnexpectedAlertPresentException:
                            #print "no alert present above"
                            break

                        for random in random_value_container:
                            if random in alert_value:
                                print "DOM XSS Confirn MaSter for url {0}".format(new_url)
                                print ""
                                break

                        alert_object.accept()

                    sleep(1)

                except:
                    #print "error"
                    sleep(1)
                    continue

        if query:
            new_url = new_url + "?" + query
            random_value = random_digit_alpha.randDigitAlpha(8)
            random_value_container.append(random_value)
            new_url = new_url + "#" + random_value
            driver.get(new_url)
            #driver.refresh()
            #print new_url

            try:
                for x in range(Global.number_of_alerts):

                    try:
                        alert_object = driver.switch_to.alert
                        alert_value = alert_object.text

                    except NoAlertPresentException, UnexpectedAlertPresentException:
                        #print "no alert present below"
                        break

                    for random in random_value_container:
                        if random in alert_value:
                            print "DOM XSS Confirn MaSter for url {0}".format(new_url)
                            print ""
                            break

                    alert_object.accept()

                sleep(1)

            except:
                #print "error"
                sleep(1)

        driver.quit()
        print "Testing Done...MaSter"
        return 0


