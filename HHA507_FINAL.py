#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 19:20:05 2021

@author: victoria_rodriguez
"""

## PART 1 - DATA EXTRACTION PORTION

## Step 1 - Import needed packages 

import pandas as pd
!pip install pandas_profiling
!pip install sweetviz
!pip install pyjanitor 
from janitor import clean_names, remove_empty 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob 


## Step 2 - Upload the 3 primary csv files for data analysis 

hospitaldf = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/hospital_info.csv')

outpatientdf = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/outpatient_2015.csv')

inpatientdf = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/inpatient_2015.csv')


## Step 3 - Gather the lengths for the 3 primary csv files

print ('hospital_info:' , len(hospitaldf))
## hospital_info = 5,314 rows x 29 columns

print ('outpatient_info:' , len(outpatientdf))
## outpatient_info = 32,532 rows x 11 columns

print ('inpatient_info:' , len(inpatientdf))
## inpatient_info = 201,876 rows x 12 columns

## The order from largest to shortest dataset : inpatient, outpatient, hospital 


## Step 4 - Deeper dive into hospitaldf dataset 

list (hospitaldf) 

 ['provider_id',
 'hospital_name',
 'address',
 'city',
 'state',
 'zip_code',
 'county_name',
 'phone_number',
 'hospital_type',
 'hospital_ownership',
 'emergency_services',
 'meets_criteria_for_meaningful_use_of_ehrs',
 'hospital_overall_rating',
 'hospital_overall_rating_footnote',
 'mortality_national_comparison',
 'mortality_national_comparison_footnote',
 'safety_of_care_national_comparison',
 'safety_of_care_national_comparison_footnote',
 'readmission_national_comparison',
 'readmission_national_comparison_footnote',
 'patient_experience_national_comparison',
 'patient_experience_national_comparison_footnote',
 'effectiveness_of_care_national_comparison',
 'effectiveness_of_care_national_comparison_footnote',
 'timeliness_of_care_national_comparison',
 'timeliness_of_care_national_comparison_footnote',
 'efficient_use_of_medical_imaging_national_comparison',
 'efficient_use_of_medical_imaging_national_comparison_footnote',
 'location']
 
## Each row represents a unique hospital (referenced by 'provider_id') and additional info for each location. 


## Step 5 - Deeper dive into outpatientdf dataset 

list (outpatientdf)

['provider_id',
 'provider_name',
 'provider_street_address',
 'provider_city',
 'provider_state',
 'provider_zipcode',
 'apc',
 'hospital_referral_region',
 'outpatient_services',
 'average_estimated_submitted_charges',
 'average_total_payments']

## Each row represents a unique apc code for multiple outpatient locations (referenced by 'provider_id').
## Also, includes averages for charges and total payments. 


## Step 6 - Deeper dive into inpatientdf dataset 

list (inpatientdf)

['provider_id',
 'provider_name',
 'provider_street_address',
 'provider_city',
 'provider_state',
 'provider_zipcode',
 'drg_definition',
 'hospital_referral_region_description',
 'total_discharges',
 'average_covered_charges',
 'average_total_payments',
 'average_medicare_payments']

## Each row represents a unique drg code for multiple inpatient locations (referenced by 'provider_id').
## Also, includes averages for charges, total payments, and medicare payments. 


## Step 7 - Prepare the 3 datasets for future merges or concats **DATA CLEANING STEP**
## Start off by removing NaN values from all 3 datasets 

## The outpatient and inpatient datasets were able to be fixed using the dropna function.

outpatientdf2 = outpatientdf.dropna()

inpatientdf2 = inpatientdf.dropna()

## The hospital dataset consists of numerous null values, so remove the nulls from the columns that will be used.
## Confirm that there are no more null values in the column by using the isn().sum() command. 

newhospitaldf1 = hospitaldf[hospitaldf['hospital_overall_rating'].notna()] 
newhospitaldf1['hospital_overall_rating'].isna().sum()


newhospitaldf2 = hospitaldf[hospitaldf['readmission_national_comparison'].notna()]
newhospitaldf2['readmission_national_comparison'].isna().sum()


newhospitaldf3 = hospitaldf[hospitaldf['patient_experience_national_comparison'].notna()] 
newhospitaldf3['patient_experience_national_comparison'].isna().sum()


newhospitaldf4 = hospitaldf[hospitaldf['efficient_use_of_medical_imaging_national_comparison'].notna()] 
newhospitaldf4['efficient_use_of_medical_imaging_national_comparison'].isna().sum()


## Step 8 - Concat each of the new hospital dataframes into 1 dataframe
## Note - used concat function because we are combining dataframes that have the same columns 

hospital_merged1 = pd.concat([newhospitaldf1,newhospitaldf2])
hospital_merged2 = pd.concat([newhospitaldf3,newhospitaldf4])

final_hospital = pd.concat([hospital_merged1,hospital_merged2])


## Step 9 - Change the primary column named 'provider_id' to a string for all 3 datasets (for easy merging)

outpatientdf2['provider_id'] = outpatientdf['provider_id'].astype(str)

inpatientdf2['provider_id'] = inpatientdf['provider_id'].astype(str)

final_hospital['provider_id'] = hospitaldf['provider_id'].astype(str)


## Step 10 - Merge the newly cleaned hospital dataframe to the outpatient dataframe (left merge onto outpatient)
## Note - used merge because these are dataframe with different columns 

outpatient_hospital = outpatientdf2.merge(final_hospital, how = 'left', left_on='provider_id', right_on='provider_id')
outpatient_hospital.sample(50)


## Step 11 - Merge the newly cleaned hospital dataframe to the inpatient dataframe

inpatient_hospital = inpatientdf2.merge(final_hospital, how = 'left', left_on='provider_id', right_on='provider_id')
inpatient_hospital.sample(50)


## Step 12 - Deeper dive into Stony Brook 

SBUinfo = hospitaldf[hospitaldf['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']

## Quick notes: 
## provider_id = 330393
## hospital_type = Acute Care 
## hospital_ownership = Government - state
## hospital_overall_rating = 4
## mortality_national_comparison = above national average
## safety_of_care_national_comparison = above national average
## readmission_national_comparison = below national average
## patient_experience_national_comparison = below national average
## effectiveness_of_care_national_comparison = same as national average
## timeliness_of_care_national_comparison = below national average
## efficient_use_of_medical_imaging_national_comparison = same as national average

sb_inpatient = inpatientdf[inpatientdf['provider_id'] == 330393]

sb_outpatient = outpatientdf[outpatientdf['provider_id'] == 330393]


## Step 13 - Deeper dive into New York locations 

NY_info = hospitaldf[hospitaldf['state'] == 'NY']

NY_inpatient = inpatientdf[inpatientdf['provider_state'] == 'NY']

NY_outpatient = outpatientdf[outpatientdf['provider_state'] == 'NY']


##Answering the following questions for this final assignment:
    
###1. How does Stony Brook compare to the rest of NY?
###2. What is the most expensive inpatient DRG service?
###3. What is the most expensive outpatient APC service?\

###4. Which DRG service has the highest total discharges for Stony Brook?
###5. Which APC service has the highest total discharges for Stony Brook?
###6. What are Stony Brook's quality comparison levels in comparison to Albany Medical Center Hospital? 
-------------------------------------------------------------------------------------------------------------------
### PART 2 - STREAMLIT PORTION

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
st.write('Hello, *World!* :sunglasses:') 

# Load the data:     
hospitaldf = load_hospitals()
inpatientdf = load_inatpatient()
outpatientdf = load_outpatient()  

# Preview the dataframes 
st.header('Hospital Data Preview')
st.dataframe(load_hospitals())

st.header('Inpatient Data Preview')
st.dataframe(load_inatpatient())

st.header('Outpatient Data Preview')
st.dataframe(load_outpatient() )


# Create a unique dataframe for New York Hospitals 
hospitals_ny = hospitaldf[hospitaldf['state'] == 'NY']
st.header('Hospitals in New York Summary')
st.dataframe(hospitals_ny)

st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)




# Generate a summary for Stony Brook 
SBUinfo = hospitaldf[hospitaldf['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']

st.header('Stony Brook University Comparison')
st.dataframe(SBUinfo)
st.markdown('In comparison to the other hospitals in New York')