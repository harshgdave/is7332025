#Question-1 :- Create a dataset profile table that gives an overview of the dataset. 
#Answer 1:- The below cell consists of the code required to generate the dataset profile data, and necessary packages that have to be installed and imported to visulaize the output.(Check Run the below code to get dataset profile table)
#Question1 Solution Code
!pip install ydata-profiling
import pandas as pd
from ydata_profiling import ProfileReport
import os

file_path = "https://raw.githubusercontent.com/UB01976/is7332025/refs/heads/main/data-mining-project-repo/hw1/hw1_UB01976/BKB_WaterQualityData_2020084.csv"  # Path where the dataset is located in my Github Repository
df = pd.read_csv(file_path)

categorical_columns = df.select_dtypes(include=['object']).columns  # Identify categorical or discrete attributes

unique_values_count = {col: df[col].nunique() for col in categorical_columns} # Count unique values for each categorical column

top_values = {col: df[col].value_counts().head(3) for col in categorical_columns} # Finding the three most common values for each categorical column

print("Total Number of Unique Values per Attribute:")
for col, count in unique_values_count.items():
    print(f"{col}: {count} unique values")

print("\nTop Three Attribute Values with the Largest Count:")
for col, values in top_values.items():
    print(f"\n{col}:")
    print(values)

profile = ProfileReport(df, explorative=True)

profile.to_notebook_iframe()
profile_output = "Water_Quality_Profile.html"
profile.to_file(profile_output)
numeric_stats = df.describe().T[['min', 'max', 'mean', '50%', 'std']]  # Compute Statistics for Numeric Columns ( for median calculation we use 50%, as it is the mid-value)
numeric_stats.rename(columns={'50%': 'median'}, inplace=True)
print("\n Numeric Column Summary:")
print(numeric_stats)
if os.path.exists(profile_output):
    from IPython.display import FileLink
    print("Click below to download the profile report:")
    display(FileLink(profile_output))
else:
    print("Profile report was not generated correctly!")



#Question-2 :- Generate a series of plots to describe the temporal pattern (year-to-year, monthly, and day-of-week) or other aggregate patterns. #Answer 2 :- The code below gives the plot related to data aaccording to time series, i.e. for yearly, monthly, and for each day of week. The number of recordings or measurements are plotted against the respective x-axis of year, month, and day.(Please Run the code block below for temporal pattern)
#Question2 Solution Code   
import pandas as pd             
import matplotlib.pyplot as plt
import seaborn as sns  

#No need to import the packages which are present again if already imported in the previous question, need only in case if it is run independent.
file_path = "https://raw.githubusercontent.com/UB01976/is7332025/refs/heads/main/data-mining-project-repo/hw1/hw1_UB01976/BKB_WaterQualityData_2020084.csv"  # Path where the dataset is located in my Github Repository
df = pd.read_csv(file_path)

date_col = None                                # Identifying the date column dynamically
for col in df.columns:
    if "date" in col.lower():
        date_col = col
        break

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df["Year"] = df[date_col].dt.year                      # Extracting year, month, and day of the week
    df["Month"] = df[date_col].dt.month
    df["DayOfWeek"] = df[date_col].dt.dayofweek

    # Setting up subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 15))

    # plot color
    plot_color = "#1f77b4"  # Strong Blue

    # Yearly trend plot
    sns.histplot(df["Year"], bins=20, kde=False, ax=axes[0], color=plot_color)
    axes[0].set_title("Yearly Data Distribution", fontsize=14, fontweight="bold")
    axes[0].set_xlabel("Year", fontsize=12)
    axes[0].set_ylabel("Number of Recorded Measurements", fontsize=12)  
    axes[0].tick_params(axis='x', rotation=45)
    
    # Monthly trend plot
    sns.countplot(x="Month", data=df, ax=axes[1], color=plot_color)
    axes[1].set_title("Monthly Data Distribution", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Month", fontsize=12)
    axes[1].set_ylabel("Number of Recorded Measurements", fontsize=12)
    axes[1].set_xticklabels(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=10)

    # Day-of-week trend
    sns.countplot(x="DayOfWeek", data=df, ax=axes[2], color=plot_color)
    axes[2].set_title("Day of the Week Data Distribution", fontsize=14, fontweight="bold")
    axes[2].set_xlabel("Day of Week", fontsize=12)
    axes[2].set_ylabel("Number of Recorded Measurements", fontsize=12)
    axes[2].set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], fontsize=10)

    plt.tight_layout()
    plt.savefig("plot.png", dpi=300)
else:
    print("No date column found in the dataset. Please check column names.")


#Question-3 :- Generate a plot describing the distribution of your data, think of what machine learning problem could be around. 
#Answer 3 :- Below is the code to generate plots for various water quality metrics. The Machine learning problem here would be around analysing the water quality, which can be done using these metrics and with the data mining methods.(Run the below code for plots describing the distribution of data)
#Question3 Solution Code
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#No need to import the packages which are present again if already imported in the previous question, need only in case if it is run independent.
# Load dataset
file_path = "https://raw.githubusercontent.com/UB01976/is7332025/refs/heads/main/data-mining-project-repo/hw1/hw1_UB01976/BKB_WaterQualityData_2020084.csv"  # Path where the dataset is located in my Github Repository
df = pd.read_csv(file_path)

# We are creating a folder named plots to save all the plots
output_folder = "plots"
os.makedirs(output_folder, exist_ok=True)

# Display basic info about dataset
print(df.info())
print(df.describe())

# We need to identify the numerical columns
num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
sns.set(style="whitegrid")

# Plot distribution for numerical columns and save to folder
for col in num_cols:
    plt.figure(figsize=(8, 5))
    sns.histplot(df[col].dropna(), bins=30, kde=True, edgecolor='black')
    plt.xlabel(col)
    plt.ylabel("Frequency of Readings")
    plt.title(f"Distribution of {col}")
    plt.savefig(os.path.join(output_folder, f"{col}_distribution.png"))
    plt.close()

# Check for correlations between features
plt.figure(figsize=(10, 6))
sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.savefig(os.path.join(output_folder, "correlation_heatmap.png"))
plt.close()

# Pairplot to explore relationships between variables
sns.pairplot(df[num_cols])
plt.savefig(os.path.join(output_folder, "pairplot.png"))
plt.close()

#Question-4 :- Generate a series of plots to illustrate to support your story and make your points clear. 
#Answer 4 :- Below are the codes to display the plots (line and heatmap) to show how water quality is analyzed based on the metrics. Please run the below code to get the plots.
#Question4 Solution Code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import seaborn as sns

#No need to import the packages which are present again if already imported in the previous question, need only in case if it is run independent.
file_path = "https://raw.githubusercontent.com/UB01976/is7332025/refs/heads/main/data-mining-project-repo/hw1/hw1_UB01976/BKB_WaterQualityData_2020084.csv"  # Path where the dataset is located in my Github Repository
data = pd.read_csv(file_path)

# Data Cleaning and Preprocessing

# Convert 'ReadDate' to datetime objects, handling different formats
data['ReadDate'] = pd.to_datetime(data['ReadDate'], errors='coerce')

data['Time 24 clcok'] = pd.to_numeric(data['Time 24 clcok'], errors='coerce')

# Drop rows where essential columns have NaN values (after date conversion)
data = data.dropna(subset=['Salinity in ppt', 'Dissolved Oxygen milligram per lit', 'pH ',
                           'Secchi Depth meters', 'Water Depth meters', 'Water Temp Celsius'])

# Fill missing values with the mean for numeric columns
for col in data.columns:
    if pd.api.types.is_numeric_dtype(data[col]):
        data[col] = data[col].fillna(data[col].mean())

# Defining Water Quality Criteria (Based on available guidelines of water quality on Internet)
def assign_quality(row):
    if (5 <= row['pH '] <= 9 and
            row['Dissolved Oxygen milligram per lit'] >= 5 and
            row['Salinity in ppt'] <= 3 and
            row['Secchi Depth meters'] >= 0.5):
        return 1  # Good
    else:
        return 0  # Bad

data['quality'] = data.apply(assign_quality, axis=1)

# Selecting features and target variable
X = data[['Salinity in ppt', 'Dissolved Oxygen milligram per lit', 'pH ',
           'Secchi Depth meters', 'Water Depth meters', 'Water Temp Celsius']]
y = data['quality']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)


X_scaled = scaler.transform(X) 
data['predicted_quality'] = model.predict(X_scaled)  

# 1. Line Plot of Average Water Quality Over Time
data_sorted = data.sort_values('ReadDate')  # To ensure data is sorted by date
window_size = 12
smoothed_quality = data_sorted['predicted_quality'].rolling(window=window_size, center=True).mean()  
plt.figure(figsize=(14, 6))  
plt.plot(data_sorted['ReadDate'], smoothed_quality, color='royalblue')  
plt.title('Water Quality Over Time')
plt.xlabel('Date')
plt.ylabel('Predicted Quality (0 to 1)')
plt.grid(True)
plt.tight_layout()
plt.savefig('Water_quality_lineplot.png')
plt.show()


# Selecting only the numeric columns for correlation analysis
numeric_cols = data.select_dtypes(include=np.number).columns
df_numeric = data[numeric_cols]

# Calculating the correlation matrix
correlation_matrix = df_numeric.corr()

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Water Quality Parameters')
plt.tight_layout()
plt.savefig('Water_quality_correlation_heatmap.png')
plt.show()


#Question-5 :- Design a dashboard that allows users to explore the data pattern. 
#Answer 5 :- Below is the code to create a realtime dashboard where all the data patterns can be explored. Please run the code to generate the dashboard.
#Question5 Solution Code
!pip install dash pandas plotly
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

#No need to import the packages which are present again if already imported in the previous question, need only in case if it is run independent.

# Initialize the Dash app
app = dash.Dash(__name__)

# Load data from GitHub (simulating an API endpoint)
url = "https://raw.githubusercontent.com/UB01976/is7332025/refs/heads/main/data-mining-project-repo/hw1/hw1_UB01976/BKB_WaterQualityData_2020084.csv"  # Path where the dataset is located in my Github Repository
df = pd.read_csv(url)

# Data Cleaning and Preprocessing

# Convert 'ReadDate' to datetime objects, handling different formats
df['ReadDate'] = pd.to_datetime(df['ReadDate'], errors='coerce')

# Convert time to numeric, handling 'N/A' values
df['Time 24 clcok'] = pd.to_numeric(df['Time 24 clcok'], errors='coerce')

# Replace missing values with the mean for numeric columns
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(df[col].mean())

# Sort data by date for proper time series plotting
df = df.sort_values(by='ReadDate')

# Function to calculate the rolling mean
def calculate_rolling_mean(df, parameter, window_size):
    return df[parameter].rolling(window=window_size, center=True, min_periods=1).mean()

window_size = 30  # Adjust as needed

# Dashboard Layout
app.layout = html.Div([
    html.H1("Water Quality Dashboard"),

    dcc.DatePickerRange(
        id='date-range',
        start_date=df['ReadDate'].min(),
        end_date=df['ReadDate'].max(),
        display_format='YYYY-MM-DD'
    ),

    dcc.Dropdown(
        id='parameter-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns if pd.api.types.is_numeric_dtype(df[col])],
        value='pH ',
        multi=False
    ),

    dcc.Graph(id='time-series-chart'),

    html.Div([
        html.Label("Rolling Average Window Size:"),
        dcc.Slider(
            id='window-size-slider',
            min=1,
            max=365,
            step=7,
            value=30,
            marks={i: str(i) for i in range(1, 366, 30)} #Mark every 30 to prevent overcrowding
        )
    ]),

])

# Callback for updating the time series chart
@app.callback(
    Output('time-series-chart', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('parameter-dropdown', 'value'),
     Input('window-size-slider', 'value')]
)
def update_time_series(start_date, end_date, parameter, window_size):
    filtered_df = df[(df['ReadDate'] >= start_date) & (df['ReadDate'] <= end_date)].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Calculating the rolling mean
    if parameter in filtered_df.columns:
        filtered_df['Value'] = calculate_rolling_mean(filtered_df, parameter, window_size)

    # Creating the time series chart using Plotly Express
    fig = px.line(filtered_df, x='ReadDate', y='Value', title=f'{parameter} Over Time')
    fig.update_layout(xaxis_title='Date(in years)', yaxis_title=f'{parameter}')

    return fig

# To Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
