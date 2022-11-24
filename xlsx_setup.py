import pandas as pd
from Job import Job
# Set what excel sheet is read
xlsx = "to_import/patient_set.xlsx"
# Set used columns and skip to patient before the first patient (index starts at 0) 105
df = pd.read_excel(xlsx, sheet_name=0,usecols="B,D,E,F,H,I,K,L,R,S,U,V,X,Y,AA,AB",skiprows=331)
# Replace column names
df.columns = ['visit_date','resident', 'consultant','location','last_name','first_name','age','sex','Dx1','status_1','Dx2','status_2','Dx3','status_3','Dx4','status_4']



def get_jobs(resident):
    temp_df = df[df.resident.str.contains(resident.upper(),na=False)]
    jobs = []
    for index, patient in temp_df.iterrows():
        # Create job object
        if pd.notna(patient['last_name']):
            job = Job(pd.to_datetime(patient['visit_date']),patient['resident'],patient['consultant'],patient['location'],patient['last_name'],patient['first_name'],patient['age'],patient['sex'],patient['Dx1'],patient['status_1'],patient['Dx2'],patient['status_2'],patient['Dx3'],patient['status_3'],patient['Dx4'],patient['status_4'])
            jobs.append(job)
    return jobs
