import pandas as pd  # ✅ Make sure pandas is imported
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df_cleaned = pd.read_csv("Air_Quality_Cleaned.csv")  # ✅ Ensure the file is in the same directory

# Convert Start_Date to datetime format
df_cleaned["Start_Date"] = pd.to_datetime(df_cleaned["Start_Date"], errors="coerce")

# Extract useful time-based features
df_cleaned["Year"] = df_cleaned["Start_Date"].dt.year
df_cleaned["Month"] = df_cleaned["Start_Date"].dt.month
df_cleaned["Day_of_Week"] = df_cleaned["Start_Date"].dt.day_name()

# 1️⃣ **Air Quality Trends Over the Years** 📈
plt.figure(figsize=(10, 5))
sns.lineplot(x="Year", y="Data Value", data=df_cleaned, estimator='mean', ci=None, marker="o")
plt.title("Average Air Quality Trends Over the Years")
plt.xlabel("Year")
plt.ylabel("Average Pollution Level")
plt.grid(True)
plt.show()



# **Visualization for Chapter 2: Pollution Hotspots**

# **1️⃣ Identify the Top 10 Most Polluted Locations**
top_locations = df_cleaned.groupby("Geo Place Name")["Data Value"].mean().nlargest(10)

# **Bar Chart for Most Polluted Locations**
plt.figure(figsize=(10, 5))
sns.barplot(x=top_locations.values, y=top_locations.index, palette="Reds_r")
plt.title("Top 10 Most Polluted Locations (Average Pollution Level)")
plt.xlabel("Average Pollution Level")
plt.ylabel("Location")
plt.grid(True)
plt.show()

# **2️⃣ Heatmap for Pollution by Location and Year**
# Pivot table for visualization
pollution_pivot = df_cleaned.pivot_table(index="Geo Place Name", columns="Year", values="Data Value", aggfunc="mean")

# Heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(pollution_pivot, cmap="Reds", linewidths=0.5)
plt.title("Pollution Levels by Location and Year")
plt.xlabel("Year")
plt.ylabel("Location")
plt.show()




# **Visualization for Chapter 3: Weekday vs. Weekend Air Quality Differences**

# Ensure that the "Day_of_Week" column is properly extracted
df_cleaned["Day_of_Week"] = df_cleaned["Start_Date"].dt.day_name()

# Define the order of days for proper visualization
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# **1️⃣ Box Plot for Air Quality by Day of the Week**
plt.figure(figsize=(10, 5))
sns.boxplot(x="Day_of_Week", y="Data Value", data=df_cleaned, order=day_order, palette="coolwarm")
plt.title("Air Quality Variation by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Pollution Level")
plt.grid(True)
plt.show()

# **2️⃣ Line Plot to Show Weekly Trends in Air Pollution**
plt.figure(figsize=(10, 5))
sns.lineplot(x="Day_of_Week", y="Data Value", data=df_cleaned, estimator='mean', errorbar=None, marker="o")

plt.title("Average Pollution Levels Throughout the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Average Pollution Level")
plt.grid(True)
plt.show()



# **Visualization for Chapter 4: Seasonal Pollution Cycle**

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df_cleaned = pd.read_csv("Air_Quality_Cleaned.csv")

# Convert Start_Date to datetime format
df_cleaned["Start_Date"] = pd.to_datetime(df_cleaned["Start_Date"], errors="coerce")

# Extracting the Season from the Start_Date
df_cleaned["Season"] = df_cleaned["Start_Date"].dt.month.map({
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Fall", 10: "Fall", 11: "Fall"
})

# **Box Plot for Pollution Levels by Season**
plt.figure(figsize=(10, 5))
sns.boxplot(x="Season", y="Data Value", data=df_cleaned, order=["Winter", "Spring", "Summer", "Fall"], palette="coolwarm")
plt.title("Pollution Levels by Season")
plt.xlabel("Season")
plt.ylabel("Pollution Level")
plt.grid(True)
plt.show()


# **Visualization for Chapter 5: The Road Ahead**

# Re-load necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Reload the cleaned dataset

file_path="C:/Users/shris/OneDrive/Desktop/pythonproject/Air_Quality_Cleaned.csv"
df_cleaned = pd.read_csv(file_path)

# Convert Start_Date to datetime format
df_cleaned["Start_Date"] = pd.to_datetime(df_cleaned["Start_Date"], errors="coerce")

# Extract year for trend analysis
df_cleaned["Year"] = df_cleaned["Start_Date"].dt.year

# **1️⃣ Line Chart - Pollution Trends Over the Years**

plt.figure(figsize=(10, 5))
sns.lineplot(x="Year", y="Data Value", data=df_cleaned, estimator="mean", errorbar=None, marker="o")
plt.title("Air Pollution Trends Over the Years")
plt.xlabel("Year")
plt.ylabel("Average Pollution Level")
plt.grid(True)
plt.show()

# **2️⃣ Forecasting Future Air Quality Trends** (Basic Projection)

# Group by year and calculate mean pollution values
yearly_avg = df_cleaned.groupby("Year")["Data Value"].mean().dropna()

# Fit a linear trend line
x = yearly_avg.index
y = yearly_avg.values

# Fit a polynomial regression line (degree=2 for slight curvature)
coeffs = np.polyfit(x, y, 2)
trend_poly = np.poly1d(coeffs)

# Generate future years for projection (next 10 years)
future_years = np.arange(x.min(), x.max() + 10)
future_trend = trend_poly(future_years)

# Plot the actual trend and projected trend
plt.figure(figsize=(10, 5))
plt.plot(x, y, marker="o", label="Actual Trend", linestyle="-", color="blue")
plt.plot(future_years, future_trend, linestyle="dashed", color="red", label="Projected Trend (Next 10 Years)")

plt.title("Future Air Quality Projection Based on Current Trends")
plt.xlabel("Year")
plt.ylabel("Projected Pollution Level")
plt.legend()
plt.grid(True)
plt.show()


# Machine learning finding #

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "C:/Users/shris/OneDrive/Desktop/pythonproject/Air_Quality_Cleaned.csv"
df = pd.read_csv(file_path)

# Check if 'Data Value' column exists (modify if your pollution column has a different name)
pollution_column = "Data Value"  # Update this if the column name is different

if pollution_column not in df.columns:
    raise ValueError(f"Column '{pollution_column}' not found in dataset. Check the correct column name.")

# Generate the distribution plot (Histogram)
plt.figure(figsize=(10, 5))
sns.histplot(df[pollution_column], bins=30, kde=True, color="blue")
plt.title("Distribution of Pollution Levels")
plt.xlabel("Pollution Levels")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

