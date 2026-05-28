# Project Report: Zomato Restaurant Data Analytics

## 1. Introduction

This report details the development of the Zomato Restaurant Data Analytics and Machine Learning application. The project's goal was to create an interactive tool for analyzing restaurant data, providing both exploratory insights and predictive modeling capabilities through a user-friendly Streamlit GUI.

## 2. System Architecture

The application is built with a modular architecture, separating concerns into different components:
- **Streamlit Pages:** For the user interface of each section (Data Upload, EDA, ML Predictions, Dashboard).
- **Components:** Reusable UI and logic components (e.g., plots, sidebar).
- **Utils:** Helper functions for data loading and machine learning models.
- **Models:** Directory for storing trained machine learning models.

## 3. Machine Learning Models

Four machine learning models were implemented:
- **Rating Prediction:** A Random Forest Regressor to predict restaurant ratings.
- **Success Prediction:** A Logistic Regression model to classify restaurants as successful or not.
- **Price Range Prediction:** A Decision Tree Classifier to predict the price range.
- **Clustering:** K-Means clustering to group similar restaurants.

## 4. Conclusion

The project successfully delivers a functional Streamlit application that meets all the requirements outlined in the PRD. It serves as a comprehensive tool for Zomato restaurant data analysis, suitable for academic and portfolio purposes.
