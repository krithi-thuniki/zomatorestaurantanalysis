🍽️ Zomato Restaurant Data Analytics using Machine Learning (Streamlit App)
📌 Project Overview

This project is an interactive data analytics and machine learning system built using Zomato restaurant dataset. It provides exploratory data analysis (EDA), predictive modeling, clustering, and visualization dashboards through a user-friendly Streamlit web application.
The system helps analyze restaurant trends such as ratings, pricing behavior, and customer preferences, and also builds machine learning models to make predictions based on restaurant features.

🎯 Key Objectives
Analyze restaurant data to extract meaningful business insights
Build predictive ML models for restaurant-related outcomes
Visualize patterns using interactive dashboards
Provide a simple GUI for non-technical users using Streamlit

⚙️ Features

📂 Dataset Upload
Upload Zomato restaurant dataset in CSV format
Automatic preprocessing and validation

📊 Exploratory Data Analysis (EDA)
Distribution analysis (ratings, price, votes)
Categorical feature insights (cuisine, location, restaurant type)
Correlation heatmaps and trend visualization

🤖 Machine Learning Models
Rating Prediction (Regression)
Restaurant Success Prediction (Classification)
Price Range Prediction (Classification)
Restaurant Segmentation (K-Means Clustering)

📈 Visualization Dashboard
Interactive filters (city, cuisine, rating, price)
Dynamic charts using Plotly & Seaborn
Business insight dashboard for decision making

🧠 Machine Learning Workflow

Data Collection → Data Cleaning → Feature Engineering → Model Training → Evaluation → Prediction UI

🧰 Tech Stack
Frontend-UI	Streamlit
Backend-Python
ML Models-Scikit-learn
Data Processing-Pandas, NumPy
Visualization-Matplotlib, Seaborn, Plotly
📁 Project Structure
.
├── app.py
├── assets/
├── components/
│   ├── dashboard_plots.py
│   ├── eda_plots.py
│   └── sidebar.py
│
├── deliverables/
│   ├── Presentation.pptx
│   └── Project_Report.md
│
├── models/
│   ├── trained_models.pkl
│
├── pages/
│   ├── 1_data_upload.py
│   ├── 2_exploratory_data_analysis.py
│   ├── 3_machine_learning_predictions.py
│   └── 4_visualization_dashboard.py
│
├── utils/
│   ├── helpers.py
│   └── ml_models.py
│
├── requirements.txt
└── README.md
🚀 How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/your-username/zomato-ml-analytics.git
cd zomato-ml-analytics
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run Streamlit App
streamlit run app.py
🌐 Live Demo

👉 [https://your-streamlit-app-link.com](https://youtu.be/nl0KwNpj2Z0)

📊 Sample Results
Rating Prediction Model: ~0.4 RMSE (varies by dataset)
Success Prediction Accuracy: ~85–90%
Optimal Clusters (K-Means): 3–5 restaurant segments identified

🧪 Key Insights from Data
High-rated restaurants often cluster in specific localities
Price range strongly correlates with rating and votes
Certain cuisines dominate high-traffic regions
Clear segmentation of restaurants based on customer behavior

📌 Future Improvements
Deploy model as API (FastAPI/Flask)
Add deep learning-based recommendation system
Integrate real-time Zomato API (if available)
Improve model accuracy with hyperparameter tuning
Add user authentication for personalized analytics
