# import packages
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import flask

# run local server
server = flask.Flask(__name__)

# datset path
data_url = "Datasets/MathE_dataset.csv"  
def load_data():
    return pd.read_csv(data_url, encoding="ISO-8859-1", delimiter=";")

@server.route("/data")
def serve_data():
    df = load_data()
    return df.to_json(orient="records")

# Initialize Dash app
app = dash.Dash(__name__, server=server)

df = load_data()

app.layout = html.Div([
    html.H1("Assessment of Higher education students in Maths Learning", style={'textAlign': 'center'}),
    
    # Dropdown for filtering by country
    html.Label("Select Country of the students:"),
    dcc.Dropdown(
        id='country-filter',
        options=[{'label': c, 'value': c} for c in df["Student Country"].unique()],
        value=None,
        placeholder="Select a country",
        multi=True
    ),
    
    # Interactive Graphs
    dcc.Graph(id='question-popularity'),
    dcc.Graph(id='student-engagement'),
    dcc.Graph(id='correct-vs-incorrect'),
    dcc.Graph(id='difficulty-impact'),
    dcc.Graph(id='country-performance')
])

@app.callback(
    [
        Output('question-popularity', 'figure'),
        Output('student-engagement', 'figure'),
        Output('correct-vs-incorrect', 'figure'),
        Output('difficulty-impact', 'figure'),
        Output('country-performance', 'figure')
    ],
    [Input('country-filter', 'value')]
)
def update_charts(selected_countries):
    df = load_data()
    if selected_countries:
        df = df[df["Student Country"].isin(selected_countries)]
    
    fig1 = px.bar(df["Question ID"].value_counts().head(10),
                  x=df["Question ID"].value_counts().head(10).index,
                  y=df["Question ID"].value_counts().head(10).values,
                  title="Top 10 Most Frequently Answered Questions",
                  labels={'x': 'Question ID', 'y': 'Number of Questions Answered'}
                )
    
    student_counts = df["Student ID"].value_counts()
    fig2 = px.histogram(
        x=student_counts.index,  
        y=student_counts.values, 
        nbins=30,
        title="Distribution of Questions Answered per Student",
        labels={'x': 'Student ID', 'y': 'Number of Questions Answered'}
    )
        
    fig3 = px.bar(df["Type of Answer"].value_counts(normalize=True),
                  x=df["Type of Answer"].value_counts(normalize=True).index,
                  y=df["Type of Answer"].value_counts(normalize=True).values,
                  title="Proportion of Correct vs Incorrect Answers",
                  labels={'x': 'Type of Answers (0: Inncorrect; 1: correct)', 'y': 'Proportions of answers'})
    
    fig4 = px.bar(df.groupby("Question Level")["Type of Answer"].mean(),
                  x=df.groupby("Question Level")["Type of Answer"].mean().index,
                  y=df.groupby("Question Level")["Type of Answer"].mean().values,
                  title="Average Accuracy by Question Level",
                  labels={'x': 'Question Level', 'y': 'Average Accuracy'})
    
    fig5 = px.bar(df.groupby("Student Country")["Type of Answer"].mean().sort_values(),
                  x=df.groupby("Student Country")["Type of Answer"].mean().sort_values().index,
                  y=df.groupby("Student Country")["Type of Answer"].mean().sort_values().values,
                  title="Average Accuracy by Country",
                  labels={'x': 'Country of Student', 'y': 'Average Accuracy'})
    
    return fig1, fig2, fig3, fig4, fig5

if __name__ == '__main__':
    server.run(debug=True, port=8081)
