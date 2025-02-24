import pandas as pd
import matplotlib.pyplot as plt

data_path = '/Users/satyajit/Desktop/IS 733/space_missions.csv'

# Load the dataset
df = pd.read_csv(data_path, encoding='latin-1')

print(df.head())



# Check column names
print(df.columns)

# Check data types
print(df.dtypes)

# Check for missing values
print(df.isnull().sum())



df = df.dropna(subset=['MissionStatus'])  # Drop rows with missing mission status

df['Price'] = df['Price'].fillna(0)  # Fill missing prices with 0
df['Time'] = df['Time'].fillna('Unknown')  # Fill missing times with 'Unknown'

# Check column names
print(df.columns)

# Check data types
print(df.dtypes)

# Check for missing values
print(df.isnull().sum())

print(df['MissionStatus'].unique())
print(df['RocketStatus'].unique())

# Standardize MissionStatus
df['MissionStatus'] = df['MissionStatus'].str.strip().str.title()  # Remove extra spaces and standardize case

# Standardize RocketStatus
df['RocketStatus'] = df['RocketStatus'].str.strip().str.title()

# Extract country from Location
df['Country'] = df['Location'].apply(lambda x: x.split(',')[-1].strip())

# Check unique countries
print(df['Country'].unique())

# Convert Date to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract Year
df['Year'] = df['Date'].dt.year

# Check for duplicates
print(df.duplicated().sum())

# Drop duplicates
df = df.drop_duplicates()

print(df['Company'].unique())


# Save cleaned data to a new CSV file
df.to_csv('space_missions_clean.csv', index=False)