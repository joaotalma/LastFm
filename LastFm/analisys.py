import pandas as pd

recent_tracks = pd.read_csv('recent_tracks.csv')

recent_tracks = recent_tracks.rename(columns={'0':'Date_Listen','1': 'Artist_Name', '2':'Music_Name'})
print(recent_tracks)
