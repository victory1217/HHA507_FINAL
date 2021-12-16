#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 18:23:34 2021

@author: victoria_rodriguez
"""

## Import needed packages 

## Import needed packages 

import streamlit as st
import pandas as pd
import numpy as np 
import time


## Load in the 3 primary csv files for display  

@st.cache
def load_hospitals():
   hospitaldf = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/hospital_info.csv')
   return hospitaldf
@st.cache
def load_inatpatient():
    inpatientdf = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/inpatient_2015.csv')
    return inpatientdf
@st.cache
def load_outpatient():
    outpatientdf = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/outpatient_2015.csv')
    return outpatientdf
    
# FAKE LOADER BAR TO STIMULATE LOADING    
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)
  
st.title('HHA 507 - Final Assignment')
st.write('Victoria Rodriguez Silva :sunglasses:') 

# Load the data:     
hospitaldf = load_hospitals()
inpatientdf = load_inatpatient()
outpatientdf = load_outpatient()  

# Preview the dataframes 
st.header('Hospital Data Preview')
st.markdown('This dataset consists of 5,314 hospitals in the United States. Each row represents a unique hospital, referenced by "provider_id", and additional info for each location.')
st.dataframe(load_hospitals())

st.header('Inpatient Data Preview')
st.markdown('This dataset consists of drg codes for multiple inpatient locations. Each row represents a unique drg code, referenced by "drg_definition", along with payment details for each code.')
## Also, includes averages for charges, total payments, and medicare payments. ')
st.dataframe(load_inatpatient())

st.header('Outpatient Data Preview')
st.markdown('This dataset consists of apc codes for multiple outpatient locations. Each row represents a unique apc code, referenced by "apc", along with service and payment details for each code.')
st.dataframe(load_outpatient() )

# Create a unique dataframe for New York Hospitals 
hospitals_ny = hospitaldf[hospitaldf['state'] == 'NY']
st.header('Hospitals in New York Summary')
st.markdown('This dataset filters out hospitals located in New York from the main hospital dataframe')
st.dataframe(hospitals_ny)

# Create a breakdown of the hospital types for New York
table1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.header('Hospital Types for New York')
st.dataframe(table1)
st.markdown('Per the table above, you can see that the most popular hospital type in New York state is for acute care.')
st.markdown('Stony Brook University Hospital also falls within this category.')

# Create a breakdown of the common inpatient discharges
inpatient_ny = inpatientdf[inpatientdf['provider_state'] == 'NY']
common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()
st.header('Inpatient Discharges for New York')
st.dataframe(common_discharges)
st.markdown('Per the table above, you can see that the drg code with the highest number of discharges is 871 - SEPTICEMIA OR SEVERE SEPSIS W/O MV 96+ HOURS W MCC.')

# Create a breakdown of the common outpatient services 
outpatient_ny = outpatientdf[outpatientdf['provider_state'] == 'NY']
outpatient_discharges = outpatient_ny.groupby('apc')['outpatient_services'].sum().reset_index()
st.header('Outpatient Services for New York')
st.dataframe(outpatient_discharges)
st.markdown('Per the table above, you can see that the apc code with the most outpatient services is 0634 - Hospital Clinic Visits.')

# Create a unique dataframe for Stony Brook Inpatient info
sb_inpatient = inpatientdf[inpatientdf['provider_id']==330393]
st.header('Inpatient Data for Stony Brook')
st.dataframe(sb_inpatient)
st.markdown('This dataset filters out inpatient data for Stony Brook University Hospital from the main inpatient dataframe')

sb_discharges = sb_inpatient.pivot_table(index =['drg_definition'],values =['total_discharges'],aggfunc='mean')
st.header('Total Discharges for DRG Codes at Stony Brook')
st.dataframe(sb_discharges)
st.markdown('This pivot table shows the total discharges per drg code for Stony Brook University Hospital.')
st.markdown('Per the table above, you can see that the highest amount of discharges came from drg code 871 - SEPTICEMIA OR SEVERE SEPSIS W/O MV 96+ HOURS W MCC.')
st.markdown('In comparison to the cumulative inpatient discharge data for all of New York, Stony Brook University Hospital shares the same drg code with the most discharges.')

# Create a unique dataframe for Stony Brook Outpatient info
sb_outpatient = outpatientdf[outpatientdf['provider_id']==330393]
st.header('Outpatient Data for Stony Brook')
st.dataframe(sb_outpatient) 
st.markdown('This dataset filters out outpatient data for Stony Brook University Hospital from the main outpatient dataframe')


sb_services = sb_outpatient.pivot_table(index =['apc'],values=['outpatient_services'],aggfunc='mean')
st.header('Total Outpatient Services for APC Codes at Stony Brook')
st.dataframe(sb_services)
st.markdown('This pivot table shows the number of outpatient services per apc code for Stony Brook University Hospital')
st.markdown('Per the table above, you can see that the apc cde with the largest amount of services is 0269 - Level I Echocardiogram Without Contrast.')
st.markdown('In comparison to the cumulative outpatient data for all of New York, where apc code 0634 - Hospital Clinic Visits was the service with the most services.')


# Map of New York Hospital locations 
st.subheader('Map of NY Hospital Locations')
hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])
st.map(hospitals_ny_gps)

