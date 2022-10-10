
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time
from setup import *

RATE_LIMIT = 1
IMPLICIT_WAIT = 30

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://uerm.pdshis.website/patients/1ed3dd55-3cfc-642a-a8ab-06804c000428")
wait = WebDriverWait(driver,20)



def resident_login(email, password):
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(email)
    wait.until(EC.text_to_be_present_in_element_value((By.ID, 'email'),email))
  
    pass_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    pass_field.send_keys(password)
    wait.until(EC.text_to_be_present_in_element_value((By.ID, 'password'),password))
    
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div[2]/form/div[4]/button')))
    login_button.click()
    # time.sleep(RATE_LIMIT)

def new_patient(patient):
    addPatient = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/nav/div[1]/div/div[1]/div[4]/a')))
    addPatient.click()

    lName_field = wait.until(EC.text_to_be_present_in_element_value((By.ID,'lastname'),patient['last_name']))
    lName_field.send_keys(patient['last_name'])

    fName_field = wait.until(EC.text_to_be_present_in_element_value((By.ID,'firstname'),patient['first_name']))
    fName_field.send_keys(patient['first_name'])

    current_day = datetime.datetime.now()
    current_year = current_day.strftime("%Y")
    birthday_field = wait.until(EC.presence_of_element_located((By.ID,'year_of_birth')))
    if 'mos' not in patient['age']:
        birthday_field.send_keys(int(current_year) - int(patient['age']))
    else:
        birthday_field.send_keys(int(current_year))
    
    if patient['sex'] == 'M' or patient['sex'] == 'm':
        m_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="male"]')))
        m_button.click()
    else:
        f_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="female"]')))
        f_button.click()
    create_patient = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/main/div/div/div[2]/button[2]')))
    create_patient.click()

def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True   

def new_visit(patient):
# TO DO - add waits to ensure that fields are found before we interact we them. MAKE SURE TO ADD EXPLICIT WAITS
    wait.until(EC.invisibility_of_element((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[1]/div')))
    driver.execute_script("arguments[0].click();", wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div[1]/div[2]/button"))))

    time.sleep(RATE_LIMIT)
    patient['visit_date'] = pd.to_datetime(df['visit_date'])
    date_field = wait.until(EC.element_to_be_clickable((By.ID,'visit_date')))
    date_field.click()
    time.sleep(RATE_LIMIT)
    date_field.clear()
    time.sleep(RATE_LIMIT)
    date_field.send_keys(patient['converted_date'])
    time.sleep(RATE_LIMIT)
    date_field.send_keys(Keys.ENTER)
    time.sleep(RATE_LIMIT)

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
    
    time.sleep(RATE_LIMIT)
    add_dx(patient)

    finalize_visit = driver.find_element(By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[2]/button[2]')
    finalize_visit.click()
    # cancel_visit = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[2]/button[1]')))
    # cancel_visit.click()

def addDx_helper(dx,options):
    for count,option in enumerate(options):
        # print(f'On count: {count}')
        if option.text.lower() in dx.lower():
            option.click()
        if count == len(options)-1:
            option.click()
# TO DO modify add_dx to make it more robust, add checks to make sure fields are filled and add methods to retry when it fails
def add_dx(patient):
    # condition will check if the first diagnosis is already added
    condition = check_exists_by_xpath('//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[7]/label')
    print(f'"Diagnosis 1 on page": {condition}')

    if not condition:
        add_dx = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[7]/button')))
        add_dx.click()
    dx_field = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[7]/div[2]/input')))
    dx_field.send_keys(patient['Dx1'])
    create_dx = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[7]/div[2]/div/ul')))
    options = create_dx.find_elements(By.TAG_NAME,'li')
    addDx_helper(patient['Dx1'],options)

    create_dx.click()
    if 'ff' in patient['status_1']:
        dx_type = wait.until(EC.element_to_be_clickable((By.ID,'diagnoses.0.diagnosis_type_ffup')))
        time.sleep(RATE_LIMIT)
        dx_type.click()

    if pd.notna(patient['Dx2']):
        add_dx = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[10]/button')))
        add_dx.click()
        dx_field = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[10]/div[2]/input')))
        dx_field.send_keys(patient['Dx2'])
        create_dx = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[10]/div[2]/div/ul')))
        options = create_dx.find_elements(By.TAG_NAME,'li')
        addDx_helper(patient['Dx2'],options)
        if 'ff' in patient['status_2']:
            dx_type = wait.until(EC.element_to_be_clickable((By.ID,'diagnoses.1.diagnosis_type_ffup')))
            time.sleep(RATE_LIMIT)
            dx_type.click()

    if pd.notna(patient['Dx3']):
        add_dx = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[13]/button')))
        add_dx.click()
        dx_field = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[13]/div[2]/input')))
        dx_field.send_keys(patient['Dx3'])
        create_dx = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="919e06c4ea7e2a5bb720134d693a8671"]/div[2]/div[1]/div[2]/div/form/div/div/div[13]/div[2]/div/ul')))
        options = create_dx.find_elements(By.TAG_NAME,'li')
        addDx_helper(patient['Dx3'],options)
        if 'ff' in patient['status_3']:
            dx_type = wait.until(EC.element_to_be_clickable((By.ID,'diagnoses.2.diagnosis_type_ffup')))
            time.sleep(RATE_LIMIT)
            dx_type.click()
    time.sleep(RATE_LIMIT)


# TO DO  
# Modify rate limit to test request limit
# test the program on example patient


def change_resident(new_resident):
    # log out of current resident
    dropdown = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/nav/div[1]/div/div[2]/div/div/div[1]/span/button')))
    dropdown.click()

    logout_button = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/nav/div[1]/div/div[2]/div/div/div[2]/div/form/a')))
    logout_button.click()
    time.sleep(RATE_LIMIT)
    new_resident = new_resident.lower()
    if 'ledesma' in new_resident:
        
        time.sleep(RATE_LIMIT)
    elif 'lim' in new_resident:
        
        time.sleep(RATE_LIMIT)
    elif 'miranda' in new_resident:
        
        time.sleep(RATE_LIMIT)
    elif 'salamanca' in new_resident:
        
        time.sleep(RATE_LIMIT)
    elif 'tee' in new_resident:
        
        time.sleep(RATE_LIMIT)
        


def main():
    start = time.time()
    
    attending_resident = 'Ledesma'

    for index, patient in df.iterrows():
        patient_resident = patient['resident']
        # print('processing'+patient_resident)
        # Decide patient resident
        if patient_resident.find('/'):
            patient_resident = patient_resident[patient_resident.find('/')+1:]
            patient_resident = patient_resident[:patient_resident.find(',')]
            # print('returned'+patient_resident)
        else:
            patient_resident[:patient_resident.find(',')]
            # print('returned'+patient_resident)

           

        if not patient['onboarded']:
            if (attending_resident not in patient_resident):
                attending_resident = patient_resident
                change_resident(attending_resident)
                time.sleep(RATE_LIMIT)
            time.sleep(RATE_LIMIT)
            new_patient(patient)
            new_visit(patient)
            time.sleep(RATE_LIMIT)
            patient['onboarded'] == True

    end = time.time()
    print('Script finished in ', time.strftime("%H:%M:%S",time.gmtime(end-start)))
    driver.quit()

if __name__ == '__main__':
    main()
    


        
    

   
