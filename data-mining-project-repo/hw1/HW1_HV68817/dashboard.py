import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "Datasets/MathE_dataset.csv"
df = pd.read_csv(file_path, encoding="ISO-8859-1", delimiter=";", on_bad_lines="skip")

# Function to plot student country distribution
def plot_student_country_distribution():
    plt.figure(figsize=(12, 6))
    df["Student Country"].value_counts().plot(kind="bar", color="skyblue")
    plt.title("Distribution of Student Countries")
    plt.xlabel("Country")
    plt.ylabel("Number of Students")
    plt.xticks(rotation=45)
    plt.show()

# Function to plot question difficulty level distribution
def plot_question_level_distribution():
    plt.figure(figsize=(8, 5))
    df["Question Level"].value_counts().plot(kind="bar", color="orange")
    plt.title("Distribution of Question Levels")
    plt.xlabel("Question Level")
    plt.ylabel("Number of Questions")
    plt.xticks(rotation=0)
    plt.show()

# Function to plot most frequently answered questions
def plot_most_frequent_questions():
    plt.figure(figsize=(10, 5))
    df["Question ID"].value_counts().head(10).plot(kind="bar", color="green")
    plt.title("Top 10 Most Frequently Answered Questions")
    plt.xlabel("Question ID")
    plt.ylabel("Number of Answered Questions")
    plt.xticks(rotation=45)
    plt.show()

# Function to plot analysis of correct vs incorrect answers
def plot_correct_vs_incorrect():
    plt.figure(figsize=(8, 5))
    df["Type of Answer"].value_counts().plot(kind="bar", color=["red", "green"])
    plt.title("Distribution of Correct vs Incorrect Answers")
    plt.xlabel("Answer Type (0 = Incorrect, 1 = Correct)")
    plt.ylabel("Number of Answers")
    plt.xticks(rotation=0)
    plt.show()

# Call all visualization functions
plot_student_country_distribution()
plot_question_level_distribution()
plot_most_frequent_questions()
plot_correct_vs_incorrect()