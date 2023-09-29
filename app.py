import pandas as pd
import streamlit as st
import pickle

# Define your password here
password = "itvedant"

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

# Function to make performance rating predictions
def predict_performance_rating(user_input):
    # Scale the user input
    scaled_data = per_se.transform(user_input)

    # Make predictions for performance rating
    performance_prediction = per_ra_reg.predict(scaled_data)
    return performance_prediction

# Function to create the performance rating page
def performance_rating_page():
    st.title("Performance Rating Prediction")
    st.sidebar.title("Select Employee")

    # Create a form to enter employee information for performance prediction
    EmpEnvironmentSatisfaction = st.sidebar.slider("Employee Environment Satisfaction", 1, 4, 2)
    EmpLastSalaryHikePercent = st.sidebar.slider("Employee Last Salary Hike Percent", 1, 25, 10)
    YearsSinceLastPromotion = st.sidebar.slider("Years Since Last Promotion", 0, 15, 3)
    EmpDepartment = st.sidebar.selectbox("Employee Department", ['Data Science', 'Development', 'Finance', 'Human Resources', 'Research & Development', 'Sales'])
    EmpDepartment_encoded = emp_department_map[EmpDepartment]
    ExperienceYearsInCurrentRole = st.sidebar.slider("Experience Years in Current Role", 0, 20, 2)
    EmpHourlyRate = st.sidebar.slider("Employee Hourly Rate", 20, 100, 50)
    EmpJobRole = st.sidebar.selectbox("Employee Job Role", ['Business Analyst', 'Data Scientist', 'Delivery Manager', 'Developer', 'Finance Manager', 'Healthcare Representative', 'Human Resources', 'Laboratory Technician', 'Manager', 'Manager R&D', 'Manufacturing Director', 'Research Director', 'Research Scientist', 'Sales Executive', 'Sales Representative', 'Senior Developer', 'Senior Manager R&D', 'Technical Architect', 'Technical Lead'])
    EmpJobRole_encoded = emp_job_role_map[EmpJobRole]
    TotalWorkExperienceInYears = st.sidebar.slider("Total Work Experience (years)", 0, 40, 5)

    # Create a button to make  performance predictions
    if st.sidebar.button("Predict Performance Rating"):
        # Create a DataFrame with user input
        user_df = pd.DataFrame(data=[[EmpEnvironmentSatisfaction, EmpLastSalaryHikePercent, YearsSinceLastPromotion, EmpDepartment_encoded,
                                      ExperienceYearsInCurrentRole, EmpHourlyRate, EmpJobRole_encoded, TotalWorkExperienceInYears]],
                               columns=['EmpEnvironmentSatisfaction', 'EmpLastSalaryHikePercent', 'YearsSinceLastPromotion',
                                        'EmpDepartment', 'ExperienceYearsInCurrentRole', 'EmpHourlyRate', 'EmpJobRole',
                                        'TotalWorkExperienceInYears'])

        # Make predictions for performance rating
        performance_prediction = predict_performance_rating(user_df)

        st.subheader("Performance Rating Prediction")
        st.write(f"Predicted Performance Rating: {performance_prediction[0]}")

# Function to make attrition predictions
def predict_attrition(user_input):
    # Scale the user input
    scaled_data = att_se.transform(user_input)

    # Make predictions for attrition
    attrition_prediction = att_ra_reg.predict(scaled_data)
    return attrition_prediction

# Function to create the main page for attrition prediction
def attrition_page():
    st.title("Attrition Prediction Web App")
    st.sidebar.title("Select Employee")

    Age = st.sidebar.slider("Age", 18, 65, 30)
    DistanceFromHome = st.sidebar.slider("Distance From Home (miles)", 1, 29, 10)
    TotalWorkExperienceInYears = st.sidebar.slider("Total Work Experience (years)", 0, 40, 5)
    ExperienceYearsInCurrentRole = st.sidebar.slider("Experience Years in Current Role", 0, 20, 2)
    YearsWithCurrManager = st.sidebar.slider("Years with Current Manager", 0, 20, 2)
    EmpJobInvolvement = st.sidebar.slider("Employee Job Involvement", 1, 4, 2)
    ExperienceYearsAtThisCompany = st.sidebar.slider("Experience Years at This Company", 0, 40, 5)
    EmpEnvironmentSatisfaction = st.sidebar.slider("Employee Environment Satisfaction", 1, 4, 2)
    
    # Encode categorical features
    OverTime = st.sidebar.selectbox("OverTime", ['No', 'Yes'])
    OverTime_encoded = 1 if OverTime == 'Yes' else 0
    
    MaritalStatus = st.sidebar.selectbox("Marital Status", ['Divorced', 'Married', 'Single'])
    MaritalStatus_encoded = {'Divorced': 2, 'Married': 1, 'Single': 0}[MaritalStatus]
    
    EmpJobRole = st.sidebar.selectbox("Employee Job Role", ['Business Analyst', 'Data Scientist', 'Delivery Manager', 'Developer', 'Finance Manager', 'Healthcare Representative', 'Human Resources', 'Laboratory Technician', 'Manager', 'Manager R&D', 'Manufacturing Director', 'Research Director', 'Research Scientist', 'Sales Executive', 'Sales Representative', 'Senior Developer', 'Senior Manager R&D', 'Technical Architect', 'Technical Lead'])
    EmpJobRole_encoded = {
        'Business Analyst': 13, 'Data Scientist': 8, 'Delivery Manager': 3, 'Developer': 14, 'Finance Manager': 6,
        'Healthcare Representative': 15, 'Human Resources': 1, 'Laboratory Technician': 16, 'Manager': 7,
        'Manager R&D': 10, 'Manufacturing Director': 12, 'Research Director': 5, 'Research Scientist': 11,
        'Sales Executive': 9, 'Sales Representative': 4, 'Senior Developer': 17, 'Senior Manager R&D': 0,
        'Technical Architect': 18, 'Technical Lead': 2
    }[EmpJobRole]

    # Create a button to make predictions for attrition
    if st.sidebar.button("Predict Attrition"):
        # Create a DataFrame with user input
        user_df = pd.DataFrame(data=[[Age, DistanceFromHome, TotalWorkExperienceInYears, ExperienceYearsInCurrentRole, 
                                      YearsWithCurrManager, EmpJobInvolvement, ExperienceYearsAtThisCompany, 
                                      EmpEnvironmentSatisfaction, OverTime_encoded, MaritalStatus_encoded, 
                                      EmpJobRole_encoded]],
                               columns=['Age', 'DistanceFromHome', 'TotalWorkExperienceInYears', 
                                        'ExperienceYearsInCurrentRole', 'YearsWithCurrManager', 'EmpJobInvolvement',
                                        'ExperienceYearsAtThisCompany', 'EmpEnvironmentSatisfaction', 'OverTime',
                                        'MaritalStatus', 'EmpJobRole'])

        # Make predictions for attrition
        attrition_prediction = predict_attrition(user_df)

        st.subheader("Attrition Prediction")
        if attrition_prediction[0] == 0:
            st.success("No attrition predicted. Employee is likely to stay.")
        else:
            st.warning("Attrition predicted. Employee may leave the company.")


# Function to make job satisfaction predictions
def predict_job_satisfaction(user_input):
    # Scale the user input
    scaled_data = job_sat_se.transform(user_input)

    # Make predictions for job satisfaction
    job_satisfaction_prediction = job_sat_ra_reg.predict(scaled_data)
    return job_satisfaction_prediction

# Job satisfaction prediction page (similar structure to the performance rating page)
def job_satisfaction_page():
    st.title("Job Satisfaction Prediction")
    st.sidebar.title("Select Employee")

    marital_status_map = {'Divorced': 1, 'Married': 2, 'Single': 0}
    over_time_map = {'No': 0, 'Yes': 1}
    gender_map = {'Female': 1, 'Male': 0}
    job_role_map = {'Healthcare Representative': 6, 'Human Resources': 4, 'Laboratory Technician': 2, 'Manager': 8, 'Manufacturing Director': 7, 'Research Director': 3, 'Research Scientist': 1, 'Sales Executive': 0, 'Sales Representative': 5}
        

    MaritalStatus = st.sidebar.selectbox("Marital Status", ['Divorced', 'Married', 'Single'])
    MaritalStatus_encoded = marital_status_map[MaritalStatus]

    PercentSalaryHike = st.sidebar.slider("Percent Salary Hike", 1, 25, 10)

    OverTime = st.sidebar.selectbox("OverTime", ['No', 'Yes'])
    OverTime_encoded = over_time_map[OverTime]

    Gender = st.sidebar.selectbox("Gender", ['Female', 'Male'])
    Gender_encoded = gender_map[Gender]

    JobRole = st.sidebar.selectbox("Job Role", ['Healthcare Representative', 'Human Resources', 'Laboratory Technician',
                                                 'Manager', 'Manufacturing Director', 'Research Director',
                                                 'Research Scientist', 'Sales Executive', 'Sales Representative'])
    JobRole_encoded = job_role_map[JobRole]

    EnvironmentSatisfaction = st.sidebar.slider("Environment Satisfaction", 1, 4, 2)
    TotalWorkingYears = st.sidebar.slider("Total Working Years", 1, 40, 10)
    HourlyRate = st.sidebar.slider("Hourly Rate", 20, 100, 50)
    Age = st.sidebar.slider("Age", 18, 65, 30)

    BusinessTravel = st.sidebar.selectbox("Business Travel", ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'])
    BusinessTravel_encoded = {'Non-Travel': 0, 'Travel_Frequently': 1, 'Travel_Rarely': 2}[BusinessTravel]

    MonthlyIncome = st.sidebar.slider("Monthly Income", 1000, 20000, 5000)

    # Create a button to make predictions
    if st.sidebar.button("Predict Job Satisfaction"):
        # Create a DataFrame with user input
        user_df = pd.DataFrame(data=[[MaritalStatus_encoded, PercentSalaryHike, OverTime_encoded, Gender_encoded,
                                      JobRole_encoded, EnvironmentSatisfaction, TotalWorkingYears, HourlyRate, Age,
                                      BusinessTravel_encoded, MonthlyIncome]],
                               columns=['MaritalStatus', 'PercentSalaryHike', 'OverTime', 'Gender', 'JobRole',
                                        'EnvironmentSatisfaction', 'TotalWorkingYears', 'HourlyRate', 'Age',
                                        'BusinessTravel', 'MonthlyIncome'])

        # Make predictions for job satisfaction
        job_satisfaction_prediction = predict_job_satisfaction(user_df)

        st.subheader("Job Satisfaction Prediction")
        st.write(f"Predicted Job Satisfaction: {job_satisfaction_prediction[0]}")


# Main function for the Streamlit app
def main():
    st.set_page_config(
        page_title="HR Support System",
        page_icon=":chart_with_upwards_trend:",
        layout="centered",
        initial_sidebar_state="auto",
    )

    # Create an input field for the password
    entered_password = st.sidebar.text_input("Enter Password", type="password")

    if entered_password == password:
        # Create a sidebar navigation
        pages = {
            "Attrition Prediction": attrition_page,
            "Job Satisfaction Prediction": job_satisfaction_page,
            "Performance Rating Prediction": performance_rating_page
        }

        st.sidebar.title("Navigate")
        page = st.sidebar.radio("Go to", tuple(pages.keys()))

        # Display the selected page
        pages[page]()
    elif entered_password != "":
        st.sidebar.error("Incorrect password. Please try again.")

if __name__ == "__main__":
    main()
