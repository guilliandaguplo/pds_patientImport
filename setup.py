import pandas as pd

# Set what excel sheet is read
xlsx = "to_import/patient_set.xlsx"
# Set used columns and skip to row before the first patient (index starts at 0)
df = pd.read_excel(xlsx, sheet_name=0,usecols="B,D,E,F,H,I,K,L,R,S,U,V,X,Y,AA,AB",skiprows=4)
# Replace column names
df.columns = ['visit_date','resident', 'consultant','location','last_name','first_name','age','sex','Dx1','status_1','Dx2','status_2','Dx3','status_3','Dx4','status_4']
# Add column to keep track of duplicates
df['onboarded'] = False
df['visit_date'] = pd.to_datetime(df['visit_date'])
df['converted_date'] = df['visit_date'].dt.strftime('%b %d %Y')