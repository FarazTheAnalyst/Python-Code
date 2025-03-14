import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import logging
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def preprocess_data():
    logging.info("Starting data preprocessing")
    file_path = '/opt/airflow/dags/screentime_analysis.csv'
    data = pd.read_csv(file_path)

    data['Date'] = pd.to_datetime(data['Date'])
    data['DayOfWeek'] = data['Date'].dt.dayofweek
    data['Month'] = data['Date'].dt.month
    data.drop('Date', axis=1, inplace=True)

    data = pd.get_dummies(data, columns=['App'], drop_first=True)

    scaler = MinMaxScaler()
    data[['Notifications', 'Times Opened']] = scaler.fit_transform(data[['Notifications', 'Times Opened']])

    data['PreviousDayUsage'] = data['Usage (minutes)'].shift(1).fillna(0)
    data['NotificationsxTimesOpened'] = data['Notifications'] * data['Times Opened']

    preprocessed_path = "preprocessed_screentime.csv"
    data.to_csv(preprocessed_path, index=False)
    logging.info(f"Preprocessing complete. Saved to {preprocessed_path}")

def train_model():
    logging.info("Starting model training")
    data = pd.read_csv("preprocessed_screentime.csv")

    X = data.drop(columns=["Usage (minutes)"])
    Y = data["Usage (minutes)"]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    logging.info(f"Model trained with MAE: {mae:.2f}")

# Define DAG
dag = DAG(
    'Dag_screen_time_pipeline',
    schedule_interval="@daily",
    start_date=datetime(2025, 3, 8),
    catchup=False
)

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

preprocess_task >> train_task




