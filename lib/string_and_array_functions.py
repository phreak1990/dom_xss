from string import ascii_letters,digits
from random import randint



class StingAndArrayFunctions:
    
    def __init__(self):
        pass
    
####################################################################################
    def randDigitAlpha(self, length=25):
            result = ""
            i = 1
            digit_alpha = digits + ascii_letters
            digit_alpha_length = len(digit_alpha)
            while i< length:
                    result += digit_alpha[randint(0,digit_alpha_length-1)]
                    length = length - 1 
            return  result
        
####################################################################################
    def randAlpha(self, length=25):
            result = ""
            i = 1
            digit_alpha =  ascii_letters
            digit_alpha_length = len(digit_alpha)
            while i< length:
                    result += digit_alpha[randint(0,digit_alpha_length-1)]
                    length = length - 1 
            return  result
        
####################################################################################
    def randDigit(self, length=25):
            result = ""
            i = 1
            digit_alpha = digits
            digit_alpha_length = len(digit_alpha)
            while i< length:
                    result += digit_alpha[randint(0,digit_alpha_length-1)]
                    length = length - 1 
            return  result
        
####################################################################################
    def removeNone(self, array):
        if not array is None:
            flag = 1 
            while flag:
                flag = 0
                for value in array:
                    if ((value is None) or (len(value) == 0)):
                        array.remove(value)
                        flag = 1
            if not array is None:
                return array
            else:
                return None
        else:
            return None

####################################################################################