import streamlit as st
import streamlit.components.v1 as components
import pickle
import pandas as pd 
from streamlit_option_menu import option_menu


# Load the models for attrition, job satisfaction, and performance rating
att_ra_reg = pickle.load(open('attritionmodel2.pkl', 'rb'))
att_se = pickle.load(open('attritionscaling2.pkl', 'rb'))

job_sat_ra_reg = pickle.load(open('JobSatisfactionmodel.pkl', 'rb'))
job_sat_se = pickle.load(open('JobSatisfactionscaling.pkl', 'rb'))

per_ra_reg = pickle.load(open('performancemodel.pkl', 'rb'))
per_se = pickle.load(open('performancescaling.pkl', 'rb'))

# Encoding maps
emp_department_map = {'Data Science': 5, 'Development': 3, 'Finance': 1, 'Human Resources': 0, 'Research & Development': 4, 'Sales': 2}
emp_job_role_map = {'Business Analyst': 13, 'Data Scientist': 8, 'Delivery Manager': 3, 'Developer': 14, 'Finance Manager': 6, 'Healthcare Representative': 15, 'Human Resources': 1, 'Laboratory Technician': 16, 'Manager': 7, 'Manager R&D': 10, 'Manufacturing Director': 12, 'Research Director': 5, 'Research Scientist': 11, 'Sales Executive': 9, 'Sales Representative': 4, 'Senior Developer': 17, 'Senior Manager R&D': 0, 'Technical Architect': 18, 'Technical Lead': 2}


selected = option_menu(
    menu_title="Main Menu",
    options= ['Attrition','Performance','Job Satisfaction','Dashboard','Chatbot','Contact'],
    orientation= 'horizontal',

)

if selected == 'Attrition':
    pass