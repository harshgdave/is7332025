
import pandas as pd
import sweetviz as sv

#data_path = "/Users/satyajit/Downloads/Space+Missions/space_missions.csv"

df = pd.read_csv('space_missions.csv', encoding='latin-1')
report = sv.analyze(df)

report.show_html()