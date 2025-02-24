# **Using Skimpy for Data Profiling and Saving as CSV**
import pandas as pd
from skimpy import skim

# Load the cleaned dataset
file_path = "C:/Users/shris/OneDrive/Desktop/pythonproject/Air_Quality_Cleaned.csv"
df = pd.read_csv(file_path)

# Ensure the 'Message' column is removed (if not already)
if "Message" in df.columns:
    df.drop(columns=["Message"], inplace=True)

# Convert problematic mixed-type columns to string
for col in df.columns:
    if df[col].dtype == "object":  
        try:
            df[col] = pd.to_numeric(df[col])  # Convert numeric-like text to numbers
        except ValueError:
            df[col] = df[col].astype(str)  # Convert to string if mixed types remain

# Drop unsupported columns (if any)
df = df.select_dtypes(include=["number", "object"])  # Keep only numbers and text

# Generate dataset profile summary
profile_summary = skim(df)

# Save the summary as a CSV file
csv_file_path = "C:/Users/shris/OneDrive/Desktop/pythonproject/Data_Profiling_Report_Skimpy.csv"
df.describe(include="all").to_csv(csv_file_path)

print(f"✅ Data profiling report saved as '{csv_file_path}'")
