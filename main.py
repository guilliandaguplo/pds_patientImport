
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
INITIAL_WAIT = 0

PATH = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(PATH)
# driver.get("https://uerm.pdshis.website/login")
"""FOR PATIENT TESTING"""
driver.get("https://uerm.pdshis.website/patients/1ed3dd55-3cfc-642a-a8ab-06804c000428")
wait = WebDriverWait(driver,20)

def new_patient(patient):
    #time.sleep(INITIAL_WAIT)
    addPatient = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/main/div/div[1]/div[2]/button')))
    addPatient.click()
    
    lName_field = wait.until(EC.visibility_of_element_located((By.ID,'lastname')))
    lName_field.send_keys(patient['last_name'])
    wait.until(EC.text_to_be_present_in_element_value((By.ID,'lastname'),patient['last_name']))

    fName_field = wait.until(EC.visibility_of_element_located((By.ID,'firstname')))
    fName_field.send_keys(patient['first_name'])
    wait.until(EC.text_to_be_present_in_element_value((By.ID,'firstname'),patient['first_name']))
    
    current_day = datetime.now()
    current_year = current_day.strftime("%Y")
    birthday_field = wait.until(EC.presence_of_element_located((By.ID,'year_of_birth')))
    
    try:
        if 'mo' not in str(patient['age']).lower():
            birthday_field.send_keys(int(current_year) - int(patient['age']))
        else:
            birthday_field.send_keys(int(current_year) - 1)
    except ValueError:
            birthday_field.send_keys(int(current_year) - 1)
        
    if patient['sex'] == 'M' or patient['sex'] == 'm':
        m_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="male"]')))
        m_button.click()
    else:
        f_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="female"]')))
        f_button.click()
        
    create_patient = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="15a0b5091bb0b1f8772d34f29ca65097"]/div[2]/div[2]/button[2]')))
    cancel_patient = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="15a0b5091bb0b1f8772d34f29ca65097"]/div[2]/div[2]/button[1]')))
    # create_patient.click()
    cancel_patient.click()
    
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True   

def choose_date(patient, desired_date):
    #time.sleep(INITIAL_WAIT)
    patient['visit_date'] = pd.to_datetime(df['visit_date'])
    desired_date = desired_date.strftime('%b %d, %Y')
    date_field = wait.until(EC.visibility_of_element_located((By.ID,'visit_date')))
    chosen_date = date_field.get_attribute("value")
    while desired_date not in str(chosen_date):
        #time.sleep(RATE_LIMIT)
        date_field.click()
        #time.sleep(RATE_LIMIT)
        date_field.clear()
        #time.sleep(RATE_LIMIT)
        date_field.send_keys(patient['converted_date'] + Keys.ENTER)
        chosen_date = date_field.get_attribute('value')
        chosen_date = datetime.strptime(chosen_date,'%b %d, %Y')
        chosen_date = chosen_date.strftime('%b %d, %Y')
        #time.sleep(RATE_LIMIT)
  
def new_visit(patient):
    #time.sleep(INITIAL_WAIT)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[1]/div[2]/button"))))
    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]')))
    choose_date(patient, patient['visit_date'])

    if(patient['location'] == 'TD'):
        clinic = Select(wait.until(EC.element_to_be_clickable((By.ID,'clinic'))))
        clinic.select_by_value('UERMMMC Teleconsult')
    
    consultant = str(patient['consultant']).lower()
    consultant = consultant[:consultant.find(',')]
    consultants_dropdown = Select(wait.until(EC.element_to_be_clickable((By.ID,'consultant'))))
    consultant_options = consultants_dropdown.options
    for choice in consultant_options:
        if(consultant in choice.text.lower()):
            consultants_dropdown.select_by_value(choice.text)
            # print(f'Chosen Consultant: {choice.text}')
            # print(f'IS::SELECTED {choice.is_selected()}')
    
    #time.sleep(RATE_LIMIT)
    add_dx(patient)

    # finalize_visit = driver.find_element(By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[2]/button[2]')
    # finalize_visit.click()
    cancel_visit = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[2]/button[1]')))
    cancel_visit.click()
    wait.until(EC.invisibility_of_element((By.XPATH,'/html/body/div[3]')))

def addDx_helper(dx,options):
    for count,option in enumerate(options):
        # print(f'On count: {count}')
        if option.text.lower() in dx.lower():
            option.click()
        if count == len(options)-1:
            option.click()

def add_dx(patient):
    # condition will check if the first diagnosis is already added
    time.sleep(RATE_LIMIT)
    condition = check_exists_by_xpath('//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[7]/div[2]/input')
    print(f'"Diagnosis 1 on page": {condition}')
    if not condition:
        add_dx = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[7]/button')))
        add_dx.click()
        
    dx_field = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[7]/div[2]/input')))
    dx_field.send_keys(patient['Dx1'])
    dx_options = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[7]/div[2]/div/ul')))
    options = dx_options.find_elements(By.TAG_NAME,'li')
    addDx_helper(patient['Dx1'],options)
    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[7]/div[1]/button[1]')))


    if 'ff' in str(patient['status_1']).lower():
        wait.until(EC.visibility_of_element_located((By.ID,'diagnoses.0.diagnosis_type_ffup')))
        dx_type = wait.until(EC.element_to_be_clickable((By.ID,'diagnoses.0.diagnosis_type_ffup')))
        #time.sleep(RATE_LIMIT)
        dx_type.click()

    if pd.notna(patient['Dx2']):
        add_dx = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[10]/button')))
        add_dx.click()
        dx_field = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[10]/div[2]/input')))
        dx_field.send_keys(patient['Dx2'])
        create_dx = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[10]/div[2]/div/ul')))
        options = create_dx.find_elements(By.TAG_NAME,'li')
        addDx_helper(patient['Dx2'],options)
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[10]/div[1]/button[1]')))
        
        if 'ff' in str(patient['status_2']).lower():
            wait.until(EC.visibility_of_element_located((By.ID,'diagnoses.1.diagnosis_type_ffup')))
            dx_type = wait.until(EC.element_to_be_clickable((By.ID,'diagnoses.1.diagnosis_type_ffup')))
            #time.sleep(RATE_LIMIT)
            dx_type.click()

    if pd.notna(patient['Dx3']):
        add_dx = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[13]/button')))
        add_dx.click()
        dx_field = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[13]/div[2]/input')))
        dx_field.send_keys(patient['Dx3'])
        create_dx = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[13]/div[2]/div/ul')))
        options = create_dx.find_elements(By.TAG_NAME,'li')
        addDx_helper(patient['Dx3'],options)
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[13]/div[1]/button[1]')))
        
        if 'ff' in str(patient['status_3']).lower():
            wait.until(EC.visibility_of_element_located((By.ID,'diagnoses.2.diagnosis_type_ffup')))
            dx_type = wait.until(EC.element_to_be_clickable((By.ID,'diagnoses.2.diagnosis_type_ffup')))
            #time.sleep(RATE_LIMIT)
            dx_type.click()
    # time.sleep(RATE_LIMIT)

def resident_login(resident):
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(resident.email)
    wait.until(EC.text_to_be_present_in_element_value((By.ID, 'email'),resident.email))
  
    pass_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    pass_field.send_keys(resident.password)
    wait.until(EC.text_to_be_present_in_element_value((By.ID, 'password'),resident.password))
    
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div[2]/form/div[4]/button')))
    login_button.click()
    
def change_resident(new_resident):
    # log out of current resident
    #time.sleep(INITIAL_WAIT)
    if check_exists_by_xpath('/html/body/div[2]/nav/div[1]/div/div[2]/div/div/div[1]/span/button'):
        dropdown = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/nav/div[1]/div/div[2]/div/div/div[1]/span/button')))
        dropdown.click()
        logout_button = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/nav/div[1]/div/div[2]/div/div/div[2]/div/form/a')))
        logout_button.click()
    resident_login(new_resident)
        
def main():
    start = time.time()
    attending_resident = DEFAULT
    resident_login(Rozy)
    for index, patient in df.iterrows():
        patient_resident = get_resident(patient['resident'])
        # if (attending_resident.last not in patient_resident.last):
        #     attending_resident = patient_resident
        #     time.sleep(RATE_LIMIT)
        #     change_resident(attending_resident)
        if not patient['onboarded'] and pd.notna(patient['last_name']):
            # new_patient(patient)
            # time.sleep(RATE_LIMIT)
            new_visit(patient)
            time.sleep(RATE_LIMIT)
            patient['onboarded'] == True
     

    end = time.time()
    print('Script finished in ', time.strftime("%H:%M:%S",time.gmtime(end-start)))
    driver.quit()

if __name__ == '__main__':
    main()
    