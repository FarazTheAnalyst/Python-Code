import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="Job Salary Predictor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("💰 Job Salary Predictor")
st.markdown("Predict the expected salaries based on experience, job title, gender, education level.")

# st.sidebar.subheader("Top Important Features")
# st.sidebar.image("Ml_Resume_Projects/feature_importance.png", caption="Top features")

# Main form
col1, col2 = st.columns(2)

with col1:
    job_title = st.text_input("Job Title", "Data Scientist")
    experience = st.number_input("Year of Experience", min_value=0, max_value=50, value=5)
    
with col2:
    gender = st.selectbox("Gender", ["Female", "Male"])
    education = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "PhD"])

# Predict button
if st.button("Predict Salary"):
    with st.spinner("Predicting..."):
        # Call FastAPI endpoint
        try:
            response = requests.post(
                "https://farazgill-salary-predictor-fastapi.hf.space/predict",
                json={
                    "Job_Title": job_title,
                    "Years_of_Experience": float(experience),  # Convert to float
                    "Education_Level": education,
                    "Gender": gender
                },
                headers={"Content-Type": "application/json"},  # Add headers
                timeout=10  # Add timeout
            )

            if response.status_code == 200:
                result = response.json()
                st.success(f"Predicted Salary: ${result['predicted_salary']:,.2f} {result['currency']}")

                # Show some insights
                st.subheader("Salary Insights")
                
                # Create a hypothetical salary progression (simulated to avoid multiple API calls)
                years = list(range(0, 21, 5))
                base_salary = result['predicted_salary']
                
                # Simulate salary progression based on experience
                salaries = []
                for year in years:
                    if year == experience:
                        salaries.append(base_salary)
                    else:
                        # Simple linear progression for demonstration
                        salary_estimate = base_salary * (1 + (year - experience) * 0.1)
                        salaries.append(max(salary_estimate, 30000))  # Minimum salary
                        
                # Plot salary progression
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(years, salaries, marker="o", linewidth=3, color="#2E86AB", markersize=8)
                ax.set_xlabel("Years of Experience", fontsize=12)
                ax.set_ylabel("Estimated Salary (USD)", fontsize=12)
                ax.set_title("Salary Growth Projection")
                ax.grid(True, linestyle="--", alpha=0.7)
                ax.ticklabel_format(style='plain', axis='y')  # Prevent scientific notation
                plt.xticks(years)
                
                # Format y-axis as currency
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
                
                st.pyplot(fig)
    
            else:
                st.error(f"Error in prediction: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"Could not connect to the API. Error: {e}")

# Sample data section
st.subheader("Sample Salary Data")
sample_data = pd.DataFrame({
    "Job Title": ["Data Scientist", "Software Engineer", "Product Manager"],
    "Experience": [5, 3, 7],
    "Gender": ["Male", "Female", "Male"],
    "Education": ["Master's", "Bachelor's", "MBA"],
    "Estimated Salary": ["$120,000", "$110,000", "$140,000"]
})

st.dataframe(sample_data, use_container_width=True)

# Add a test section to verify API connection
st.sidebar.subheader("API Status")
if st.sidebar.button("Check API Health"):
    try:
        health_response = requests.get("https://farazgill-salary-predictor-fastapi.hf.space/health", timeout=5)
        if health_response.status_code == 200:
            st.sidebar.success("✅ API is healthy!")
            st.sidebar.json(health_response.json())
        else:
            st.sidebar.error("❌ API health check failed")
    except:
        st.sidebar.error("❌ Cannot connect to API")

# Footer
st.markdown("---")
st.markdown("""
**Data sourced from Kaggle:** Predictions are estimates based on historical data.
**API Hosted on:** Hugging Face Spaces
**Frontend Built with:** Streamlit
""")
