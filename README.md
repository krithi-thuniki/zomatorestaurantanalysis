# 🍽️ Zomato Restaurant Data Analytics using Machine Learning (Streamlit App)

---

## 📌 Project Overview

This project is an interactive data analytics and machine learning system built using a Zomato restaurant dataset. It provides **Exploratory Data Analysis (EDA), predictive modeling, clustering, and visualization dashboards** through a user-friendly Streamlit web application.

The system helps analyze restaurant trends such as ratings, pricing behavior, and customer preferences, and also builds machine learning models to make predictions based on restaurant features.

---
🌐 Live Demo

👉 https://youtu.be/nl0KwNpj2Z0

---
## 🎯 Key Objectives

- Analyze restaurant data to extract meaningful business insights  
- Build predictive ML models for restaurant-related outcomes  
- Visualize patterns using interactive dashboards  
- Provide a simple GUI for non-technical users using Streamlit  

---

## ⚙️ Features

### 📂 Dataset Upload
- Upload Zomato restaurant dataset in CSV format  
- Automatic preprocessing and validation  

---

### 📊 Exploratory Data Analysis (EDA)
- Distribution analysis of ratings, price, and votes  
- Categorical feature insights (cuisine, location, restaurant type)  
- Correlation heatmaps  
- Trend visualization using interactive plots  

---

### 🤖 Machine Learning Models
- Rating Prediction (Regression)  
- Restaurant Success Prediction (Classification)  
- Price Range Prediction (Classification)  
- Restaurant Segmentation using K-Means Clustering  

---

### 📈 Visualization Dashboard
- Interactive filters (city, cuisine, rating, price)  
- Dynamic charts using Plotly & Seaborn  
- Business insights for decision-making  

---

## 🧠 Machine Learning Workflow

Data Collection → Data Cleaning → Feature Engineering → Model Training → Evaluation → Prediction UI

---

## 🧰 Tech Stack

| Component        | Technology        |
|------------------|------------------|
| Frontend UI      | Streamlit        |
| Backend          | Python           |
| ML Models        | Scikit-learn     |
| Data Processing  | Pandas, NumPy    |
| Visualization    | Matplotlib, Seaborn, Plotly |

---


## 🚀 How to Run the Project

### 
1 Install Dependencies
pip install -r requirements.txt
2 Run Streamlit App
streamlit run app.py

---

##📊 Sample Results
###
Rating Prediction Model: ~0.4 RMSE (varies by dataset)
Success Prediction Accuracy: ~85–90%

---
##🧪 Key Insights from Data
###
High-rated restaurants often cluster in specific localities
Price range strongly correlates with rating and votes
Certain cuisines dominate high-traffic regions
Clear segmentation of restaurants based on customer behavior

---
##🏆 Learning Outcomes
###
End-to-end Machine Learning pipeline development
Data preprocessing and feature engineering
Building interactive dashboards using Streamlit
Model evaluation for regression and classification tasks
Real-world dataset analysis and insights extraction

---
##📌 Future Improvements
###
Deploy model as API using FastAPI/Flask
Add deep learning-based recommendation system
Integrate real-time Zomato API (if available)
Improve model accuracy using hyperparameter tuning
Add user authentication for personalized analytics
