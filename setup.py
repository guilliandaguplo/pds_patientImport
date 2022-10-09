from operator import index
import numpy as np
import pandas as pd
import xlrd
# Set what excel sheet is read
xlsx = "patient_set.xlsx"
# Set used columns and skip to the first patient
df = pd.read_excel(xlsx, sheet_name=0,usecols="B:E,G:H,K,L,M,N,P,Q,S,T",skiprows=4)
# Replace column names
df.columns = ['visit_date','resident', 'consultant','location','last_name','first_name','age','sex','Dx1','status_1','Dx2','status_2','Dx3','status_3']
# Add column to keep track of duplicates
df['onboarded'] = False
df['converted_date'] = df['visit_date'].dt.strftime('%m %d %Y')



