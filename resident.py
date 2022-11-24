from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

import random
import time
import pandas as pd
from Job import Job
class Resident: 
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service= service)
    def __init__(self, first, last, email, password):
        self.first = first
        self.last = last
        self.email = email
        self.password = password
    
    def login(self):
        # Set up driver
        try:
            driver = self.driver
            web_url = "https://uerm.pdshis.website/login"
            # TO TEST
            # web_url = "https://uerm.pdshis.website/patients/1ed3dd55-3cfc-642a-a8ab-06804c000428" 
   
            driver.get(web_url)
            self.driver.find_element(by=By.ID, value='email').send_keys(self.email)
            self.driver.find_element(by=By.ID, value='password').send_keys(self.password)
            self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']").click()
        except NoSuchElementException:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span button[type='button']"))).click()
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div a[href='https://uerm.pdshis.website/logout']"))).click()
            self.driver.find_element(by=By.ID, value='email').send_keys(self.email)
            self.driver.find_element(by=By.ID, value='password').send_keys(self.password)
            self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']").click()

    def register_patient(self, patient):
        driver = self.driver
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[class='hidden space-x-8 sm:-my-px sm:ml-10 sm:flex'] a[href='https://uerm.pdshis.website/new-patient-wizard']"))).click()
        wait.until(EC.visibility_of_element_located((By.ID,'lastname'))).send_keys(patient.last_name)
        wait.until(EC.visibility_of_element_located((By.ID,'firstname'))).send_keys(patient.first_name)
        birthday_field = wait.until(EC.presence_of_element_located((By.ID,'year_of_birth')))
        birthday_field.click()
        current_year = datetime.now().strftime("%Y")
        try:
            birthday_field.send_keys(int(current_year)-int(patient.age))
            time.sleep(1)
        except:
            birthday_field.send_keys(int(current_year) - 1)
            time.sleep(2)
        
        try:
            if patient.sex.lower() == 'm':
                m_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="male"]')))
                m_button.click()
            else:
                f_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="female"]')))
                f_button.click()
        except:
            # Default to Male if no sex is given
            print('Exception occurred when handling patient sex, defaulting to male')
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="male"]'))).click()
            
        # TO ADD, SUBMIT PROCESS
        driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        
    def select_dx(dx,options):
        for count,option in enumerate(options):
            if option.text.lower() in dx.lower():
                option.click()
            if count == len(options)-1:
                option.click()

    def record_visit(self,patient):
        driver = self.driver
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"i[class^='far fa-edit']")))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[class^='flex'] button[type='submit']"))).click()
        date_field = wait.until(EC.element_to_be_clickable((By.ID,"visit_date")))
        date_field.click()
        date_field.clear()
        date_field.send_keys(pd.to_datetime(patient.visit_date).strftime("%b %d %Y")+Keys.ENTER)
        try:
            if patient.location == 'TD':
                Select(wait.until(EC.element_to_be_clickable((By.ID,'clinic')))).select_by_value('UERMMMC Teleconsult')
        except:
            print('Exception occured while selecting clinic, defaulting to UERMMMC Main Clinic')


       
        dx_count = 0
        for count, dx in enumerate(patient.diagnosis):
            if count % 2 == 0 and 'nan' not in str(dx) and len(dx) < 350:
                dx_count += 1
        index = 0
        count = 0
        while count < dx_count:
            driver.find_element(by=By.CSS_SELECTOR,value="button[class='btn btn-sm btn-secondary font-medium text-sm text-gray-700']").click()
            xpath_id = [7,10,13,16,19]
            dx_field = None
            dx_field = wait.until(EC.visibility_of_element_located((By.XPATH,f'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[{xpath_id[count]}]/div[2]/input')))
            
                # Solution 1
                # ActionChains(driver).send_keys_to_element(dx_field,patient.diagnosis[index]).perform()
                # driver.execute_script(f"arguments[0].value='{patient.diagnosis[index]}'", dx_field)
                # EO Solution 1
            try:
                # Solution 2
                text = patient.diagnosis[index].strip()
                actions = ActionChains(driver)
                actions.move_to_element(dx_field)
                actions.click()
                actions.send_keys(text)
                actions.perform()
                # EO Solution 2
                wait.until(EC.text_to_be_present_in_element_value((By.XPATH,f'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[{xpath_id[count]}]/div[2]/input'),patient.diagnosis[index].strip()))
            except:
                driver.refresh()
                print('Exception with dx input occured')
                self.record_visit(patient)
            
            try:   
                dx_option = wait.until(EC.visibility_of_element_located((By.XPATH,f'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[{xpath_id[count]}]/div[2]/div/ul')))
                diagnosis_options = dx_option.find_elements(by=By.TAG_NAME,value="li")
                Resident.select_dx(patient.diagnosis[index],diagnosis_options)
                wait.until(EC.invisibility_of_element(dx_option))
            except:
                print('Exception with dx_options occured, check patient\'s diagnosis' )
            
            try:
                if 'ff' in patient.diagnosis[index+1].lower():
                    wait.until(EC.element_to_be_clickable((By.ID,f'diagnoses.{count}.diagnosis_type_ffup'))).click()
            except:
                print('Exception when selecting visit type, defaulting to New Diagnosis')
            index += 2
            count += 1
            
        consultants_dropdown = Select(wait.until(EC.element_to_be_clickable((By.ID,'consultant'))))
        for choice in consultants_dropdown.options:
            if patient.consultant in choice.text.lower():
                consultants_dropdown.select_by_value(choice.text)
        driver.find_element(by=By.CSS_SELECTOR,value="div[class='px-6 py-4 bg-gray-100 text-right'] button[type='submit']").click()
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[1]/div')))
        wait.until(EC.invisibility_of_element((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[1]/div')))
        self.driver = driver

   
     



