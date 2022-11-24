import time
from creds import *
from xlsx_setup import *

def process_patients(resident):
    jobs = get_jobs(resident.last)
    for patient in jobs :
        resident.register_patient(patient)
        resident.record_visit(patient)

residents = [Rozy, Jay, Carmela, Sacha, Marge]
#[Rozy, Jay, Carmela, Sacha, Marge]
def main():
    start = time.time()
    for resident in residents:
        resident.login()
        process_patients(resident)
    Rozy.driver.quit()
    end = time.time()
    
    print('Script finished in ', time.strftime("%H:%M:%S",time.gmtime(end-start)))


if __name__ == '__main__':
    main()