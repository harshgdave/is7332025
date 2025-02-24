
# Assessment of Higher education students in Maths Learning

# Overview
The project provides a simple Python-based dynamic dashboard for visualizing key insights from the dataset from the MathE platform and providing an assesment of higher education students.
The dashboard leverages matplotlib to generate plots and interactive dashbaord using Dash.

# Technologies Used
- Python
- Dash Plotly using Python
- Python Packages: pandas, Matplotlib, profile_report

# Project Structure
```
├── README.md                    # Project documentation
├── HW1_HV68817
├──├── data_exploration.ipynb    # jupyter notebook to generate visualizations and profile report
├──├── dashboard_interactive.py  # run the file to host the interactive dashboard on local server
├──├── data_profiling.html       # data profile report 
├──├── Datasets                  # Project datasets
├──├──├── MathE_dataset.csv      # Dataset file (added manually)
```

# Dashboard
make the sure the required packages are installed and Run the dashboard script:
```
python3 dashboard_interactive.py
```

# Features: Visualizations
1. Student Country Distribution: Displays the number of students from each country.
2. Question Level Distribution: Visualizes the number of Basic vs. Advanced level questions.
3. Most Frequently Answered Questions: Identifies the top 10 most commonly answered questions.
4. Correct vs Incorrect Answers: Shows the proportion of correct vs incorrect responses.


# Future Enhancements
- Add support for interactive plots using Plotly
- Implement a Flask API for dynamic data fetching
- Host the project on a server.

# Contact
For any questions or contributions, feel free to reach out: akhasa1@umbc.edu
