import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, precision_score, recall_score, f1_score
from sklearn.cluster import KMeans
from autogluon.tabular import TabularPredictor

MODELS_DIR = 'models'
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

def preprocess_data(df):
    df = df.dropna(subset=['Aggregate rating', 'Votes', 'Average Cost for two', 'Cuisines', 'Has Online delivery'])
    le = LabelEncoder()
    df['Has Online delivery'] = le.fit_transform(df['Has Online delivery'])
    return df, le

def train_and_save_model(df, model_type, success_rating_threshold=4.0, success_votes_threshold=500):
    """Trains a model and saves it to the models directory."""
    df_clean = df.copy()
    le = LabelEncoder()

    numeric_cols = ['Average Cost for two', 'Votes', 'Aggregate rating', 'Price range']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    if 'Has Online delivery' in df_clean.columns:
        df_clean['Has Online delivery'] = le.fit_transform(df_clean['Has Online delivery'].astype(str))

    if model_type == 'rating':
        required = ['Average Cost for two', 'Votes', 'Has Online delivery', 'Aggregate rating']
        df_clean.dropna(subset=required, inplace=True)
        if len(df_clean) < 10:
            return None, "Not enough valid data (<10 rows) for training the rating model after cleaning."
        if df_clean['Aggregate rating'].nunique() < 2:
            return None, "Training failed: The target column ('Aggregate rating') has only one unique value after cleaning. The model has nothing to learn."
        X = df_clean[['Average Cost for two', 'Votes', 'Has Online delivery']]
        y = df_clean['Aggregate rating']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model_path = os.path.join(MODELS_DIR, 'rating_prediction_model.pkl')

    elif model_type == 'success':
        required = ['Aggregate rating', 'Votes']
        df_clean.dropna(subset=required, inplace=True)
        if len(df_clean) < 10:
            return None, "Not enough valid data (<10 rows) for training the success model after cleaning."
        df_clean['Success'] = ((df_clean['Aggregate rating'] >= success_rating_threshold) & (df_clean['Votes'] >= success_votes_threshold)).astype(int)
        if df_clean['Success'].nunique() < 2:
            return None, "Training failed: The target column ('Success') has only one unique value after cleaning. The model has nothing to learn."
        X = df_clean[['Aggregate rating', 'Votes']]
        y = df_clean['Success']
        model = LogisticRegression(random_state=42, class_weight='balanced') # Handle imbalance
        model_path = os.path.join(MODELS_DIR, 'success_prediction_model.pkl')

    elif model_type == 'price_range':
        required = ['Average Cost for two', 'Aggregate rating', 'Votes', 'Price range']
        df_clean.dropna(subset=required, inplace=True)
        if len(df_clean) < 10:
            return None, "Not enough valid data (<10 rows) for training the price range model after cleaning."
        if df_clean['Price range'].nunique() < 2:
            return None, "Training failed: The target column ('Price range') has only one unique value after cleaning. The model has nothing to learn."
        X = df_clean[['Average Cost for two', 'Aggregate rating', 'Votes']]
        y = df_clean['Price range']
        model = DecisionTreeRegressor(random_state=42) # Correct model for regression
        model_path = os.path.join(MODELS_DIR, 'price_range_prediction_model.pkl')
    else:
        return None, "Invalid model type specified."

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)
        joblib.dump(model, model_path)
        return model_path, "Model trained and saved successfully."
    except Exception as e:
        # Create a detailed diagnostic report
        report = []
        target_col = y.name
        report.append(f"**{model_type.capitalize()} Model Training Failed:** {e}")
        report.append("This usually happens if the data has issues after cleaning.")
        report.append("\n**Data Diagnostics:**")
        report.append(f"- Shape of the training data: `{X.shape}`")
        report.append(f"- Target column ('{target_col}') value counts:\n```\n{y.value_counts().to_string()}\n```")
        report.append(f"- Data summary:\n```\n{X.describe().to_string()}\n```")
        return None, "\n".join(report)

def load_model(model_path):
    """Loads a saved model from the models directory."""
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None


def predict_rating(model, cost, votes, online_delivery):
    """Predicts the rating based on input features."""
    le = LabelEncoder()
    # This is a simplified way to handle the encoding for prediction.
    # In a real-world scenario, the encoder should be saved and reused.
    online_delivery_encoded = 1 if online_delivery == 'Yes' else 0
    input_data = pd.DataFrame({
        'Average Cost for two': [cost],
        'Votes': [votes],
        'Has Online delivery': [online_delivery_encoded]
    })
    return model.predict(input_data)


def predict_success(model, rating, votes):
    input_data = pd.DataFrame([[rating, votes]], columns=['Aggregate rating', 'Votes'])
    return model.predict(input_data)


def predict_price_range(model, cost, rating, votes):
    input_data = pd.DataFrame([[cost, rating, votes]], columns=['Average Cost for two', 'Aggregate rating', 'Votes'])
    return model.predict(input_data)

def perform_clustering(df):
    df_cluster = df[['Average Cost for two', 'Aggregate rating', 'Votes']].copy()

    # Convert columns to numeric, coercing errors to NaN
    for col in df_cluster.columns:
        df_cluster[col] = pd.to_numeric(df_cluster[col], errors='coerce')

    df_cluster.dropna(inplace=True)
    
    if df_cluster.empty:
        return None # Return None if no data is left after cleaning

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10) # Explicitly set n_init
    df_cluster['Cluster'] = kmeans.fit_predict(df_cluster)
    return df_cluster

def train_and_save_autogluon_model(df, model_type, success_rating_threshold=4.0, success_votes_threshold=500):
    """Trains a problem-aware model using AutoGluon and saves it."""
    df_clean = df.copy()
    numeric_cols = ['Average Cost for two', 'Votes', 'Aggregate rating']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    problem_type = None
    hyperparameters = None

    if model_type == 'success':
        target = 'Success'
        problem_type = 'binary'
        required = ['Aggregate rating', 'Votes']
        df_clean.dropna(subset=required, inplace=True)
        if len(df_clean) < 10:
            return None, "Not enough valid data (<10 rows) for training."
        df_clean[target] = ((df_clean['Aggregate rating'] >= success_rating_threshold) & (df_clean['Votes'] >= success_votes_threshold)).astype(int)
        if df_clean[target].nunique() < 2:
            return None, f"Training failed: Target column ('{target}') has only one unique value."
        model_path = os.path.join(MODELS_DIR, 'autogluon_success_model')
        # Use default models which are better for imbalance, but keep TabPFN as an option
        hyperparameters = {'GBM': {}, 'CAT': {}, 'XGB': {}, 'RF': {}, 'XT': {}, 'TABPFNMIX': {}}

    elif model_type == 'price_range':
        target = 'Price range'
        problem_type = 'regression'
        required = ['Average Cost for two', 'Aggregate rating', 'Votes', 'Price range']
        df_clean.dropna(subset=required, inplace=True)
        if len(df_clean) < 10:
            return None, "Not enough valid data (<10 rows) for training."
        model_path = os.path.join(MODELS_DIR, 'autogluon_price_range_model')
        # Use default regression models
        hyperparameters = {'GBM': {}, 'CAT': {}, 'XGB': {}, 'RF': {}, 'XT': {}}
    else:
        return None, "AutoGluon is only configured for success and price range prediction."

    try:
        predictor = TabularPredictor(label=target, problem_type=problem_type, path=model_path).fit(
            df_clean,
            presets='medium_quality',
            hyperparameters=hyperparameters,
            verbosity=2 # Increase verbosity for better logging
        )
        return model_path, "AutoGluon model trained and saved successfully."
    except RuntimeError as e:
        # Create a detailed diagnostic report
        report = []
        report.append(f"**AutoGluon Training Failed:** {e}")
        report.append("This usually happens if the data is too small or lacks variation after cleaning.")
        report.append("\n**Data Diagnostics:**")
        report.append(f"- Shape of the training data: `{df_clean.shape}`")
        report.append(f"- Target column ('{target}') value counts:\n```\n{df_clean[target].value_counts().to_string()}\n```")
        report.append(f"- Data summary:\n```\n{df_clean.describe().to_string()}\n```")
        return None, "\n".join(report)

def predict_with_autogluon(model_path, data):
    """Makes a prediction using a saved AutoGluon model."""
    predictor = TabularPredictor.load(model_path)
    return predictor.predict(data)
