
from lib2to3.pgen2 import driver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait   
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime
import time
from creds import *
from setup import *

RATE_LIMIT = 1.5
IMPLICIT_WAIT = 30
INITIAL_WAIT = 3


class Session:
    def __init__(self):
        """SESSION CONSTANTS"""
        self.PATH = '/usr/local/bin/chromedriver'
        self.RATE_LIMITER = 1
        self.INITIAL_WAIT = 3
        self.IMPLICIT_WAIT = 30
        """NECESSARY DRIVERS"""
        self.driver = webdriver.Chrome(PATH)
        self.wait = WebDriverWait(self.driver,self.IMPLICIT_WAIT)
        
    """METHODS TO WAIT AND GRAB ELEMENTS"""
    def check_exists_by_xpath(self,xpath):
        try:
            self.driver.find_element(By.XPATH,xpath)
        except NoSuchElementException:
            return False
        return True   
    def grab_clickable_element_xpath(self,xpath):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH,xpath)))
    def grab_present_element_xpath(self,xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH),xpath))
    
    """SESSION METHODS"""
    def resident_login(self):
        pass
        
    def change_resident(self,index):
        pass
    
    def initialize(self):
        self.attending_resident = None
        self.driver.get('https://uerm.pdshis.website/login')
         
        
        
        
    def __del__(self):
        driver.quit()

class Patient(Session):
    def __init__(self,*args):
        self.visit_date = args[0]
        self.resident = args[1]
        self.consultant = args[2]
        self.location = args[3]
        self.last_name = args[4]
        self.first_name = args[5]
        self.age = args[6]
        self.sex = args[7]
        self.dx1 = args[8]
        self.dxs1 = args[9]
        self.dx2 = args[10]
        self.dxs2 = args[11]
        self.dx3 = args[12]
        self.dxs3 = args[13]
        self.dx4 = args[14]
        self.dxs4 = args[15]
        
    

def new_patient(patient):
    pass
    
def choose_date(patient, desired_date):
    pass

def new_visit(patient):
    pass
    
def addDx_helper(dx,options):
    pass

def add_dx(patient):
    pass

        
def main():
    for index, patient in enumerate(patient_list):
        
     

if __name__ == '__main__':
    main()
    