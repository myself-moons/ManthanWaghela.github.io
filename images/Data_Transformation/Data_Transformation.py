import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor

try:
    xls = pd.ExcelFile("dataset.xlsx")
    print("Sheet names in the Excel file:")
    print(xls.sheet_names)
except FileNotFoundError:
    print("Error: The file was not found at dataset.xlsx")
except Exception as e:
    print(f"An error occurred while trying to read the Excel file: {e}")

df = pd.read_excel("dataset.xlsx", sheet_name="Sheet1")
print("Dataset loaded successfully.")

# Inspect missing values
print(df.isnull().sum())

# Standardize employment status (convert to lowercase and map variations)
df['Employment_Status'] = df['Employment_Status'].str.lower().str.strip()
# Map common variations to a standard value
employment_map = {
    'emp': 'employed',
    'self-employed': 'self-employed', # explicit for clarity
    'unemployed': 'unemployed',
    'employed': 'employed',
    'retired': 'retired'
}
df['Employment_Status'] = df['Employment_Status'].map(employment_map).fillna(df['Employment_Status'])
# Check unique values to confirm
print(df['Employment_Status'].value_counts())

# Impute Credit_Score (Single Missing Value - Median)
median_cs = df['Credit_Score'].median()
df['Credit_Score'] = df['Credit_Score'].fillna(median_cs)

# Impute Loan_Balance (Median by Group)
# Calculate the median loan balance for each credit card type group
median_loan_by_type = df.groupby('Credit_Card_Type')['Loan_Balance'].transform('median')
# Fill missing values with their group's median
df['Loan_Balance'] = df['Loan_Balance'].fillna(median_loan_by_type)

# Impute Income (Predictive Imputation - MICE)
# First, we need to encode categorical variables for the imputer
df_for_impute = df.copy()

# Drop columns that are not suitable for numerical imputation
cols_to_drop_for_imputation = ['Customer_ID', 'Month_1', 'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6']
df_for_impute = df_for_impute.drop(cols_to_drop_for_imputation, axis=1)

# Select categorical columns to encode
cat_cols = ['Employment_Status', 'Credit_Card_Type', 'Location']
df_for_impute = pd.get_dummies(df_for_impute, columns=cat_cols, drop_first=True)

# Initialize the MICE imputer with a Random Forest estimator
imputer = IterativeImputer(estimator=RandomForestRegressor(),
                           max_iter=10,
                           random_state=42,
                           initial_strategy='median')

# Fit and transform the dataset to impute 'Income'
imputed_data = imputer.fit_transform(df_for_impute)

# Create a new DataFrame from the imputed data
df_imputed = pd.DataFrame(imputed_data, columns=df_for_impute.columns)

# Assign the imputed 'Income' values back to our original DataFrame
income_imputed = df_imputed['Income']
df['Income'] = df['Income'].fillna(income_imputed)

# Cap any value above 1.0 to 1.0
df['Credit_Utilization'] = df['Credit_Utilization'].clip(upper=1.0)

# Add Customer_ID back to the final dataframe (it was preserved in the original df)
print("Imputation completed successfully!")
print(df.isnull().sum())

df.to_excel("transformed_dataset.xlsx") #Transformed Dataset into Excel
