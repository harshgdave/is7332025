import pandas as pd

# Define the correct file path
file_path = "C:/Users/shris/OneDrive/Desktop/pythonproject/Air_Quality.csv"

# Load the dataset
df = pd.read_csv(file_path)

# Remove the 'Message' column if it exists
if "Message" in df.columns:
    df.drop(columns=["Message"], inplace=True)

# Perform data cleaning (Modify as needed)
df_cleaned = df.dropna()  # Removing rows with missing values

# Save the cleaned dataset
df_cleaned.to_csv("C:/Users/shris/OneDrive/Desktop/pythonproject/Air_Quality_Cleaned.csv", index=False)

# Print dataset information
print("✅ Data cleaning completed successfully.")
print(df_cleaned.info())  # Now, df_cleaned is properly defined

# Additional dataset insights
print(df_cleaned.describe())  # Summary statistics
print(df_cleaned.isnull().sum())  # Check for remaining missing values
