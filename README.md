# Zomato Restaurant Data Analytics using Machine Learning (Streamlit GUI)

This project is an interactive data analytics and machine learning system that analyzes Zomato restaurant data and provides visual insights and predictive results through a Streamlit-based graphical user interface (GUI).

## Features

- **Dataset Upload:** Upload Zomato restaurant datasets in CSV format.
- **Exploratory Data Analysis (EDA):** Interactive charts and graphs to explore the data.
- **Machine Learning Models:**
  - Rating Prediction (Regression)
  - Restaurant Success Prediction (Classification)
  - Price Range Prediction (Classification)
  - Clustering (K-Means)
- **Visualization Dashboard:** Interactive dashboard with filters for in-depth analysis.

## Tech Stack

- **Frontend GUI:** Streamlit
- **Backend:** Python
- **ML Library:** Scikit-learn
- **Visualization:** Matplotlib, Seaborn, Plotly

## Project Structure

```
.├── app.py
├── assets
├── components
│   ├── __init__.py
│   ├── dashboard_plots.py
│   ├── eda_plots.py
│   └── sidebar.py
├── deliverables
│   ├── Presentation.pptx
│   └── Project_Report.md
├── models
├── pages
│   ├── 1_data_upload.py
│   ├── 2_exploratory_data_analysis.py
│   ├── 3_machine_learning_predictions.py
│   └── 4_visualization_dashboard.py
├── README.md
├── requirements.txt
└── utils
    ├── __init__.py
    ├── helpers.py
    └── ml_models.py
```

## How to Run

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
