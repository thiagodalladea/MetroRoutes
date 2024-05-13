import streamlit as st
import pandas as pd
import pydeck as pdk
from src.distance import calculate_distance
from src.main_plot import main_plot
from src.traffic_plot import traffic_plot


def convert_color(color_string):
    # Remover "#" se presente e converter a string de cor em uma lista de valores RGB
    color_string = color_string.lstrip("#")
    r = int(color_string[0:2], 16)
    g = int(color_string[2:4], 16)
    b = int(color_string[4:6], 16)
    return [r, g, b]


# DATA
df = pd.read_csv("Metro_Madrid_2021.csv")
df["Longitude"] = df["Longitude"].str.replace(",", ".").astype(float)
df["Latitude"] = df["Latitude"].str.replace(",", ".").astype(float)
df.insert(1, "Destination", df["Station"].shift(-1))
df.insert(2, "Distance", df.apply(lambda row: calculate_distance(row, df), axis=1))
df = df.dropna(subset=["Distance"])
df.drop(df.loc[df["Distance"] > 5000].index, inplace=True)
df["Color"] = df["Color"].apply(convert_color)
df["Point Color"] = df["Point Color"].apply(convert_color)

graph_df = df[["Station", "Destination", "Distance", "Line"]]
graph = {}

for row in df.itertuples():
    station = row.Station
    destination = row.Destination
    distance = row.Distance
    line = row.Line

    if pd.isna(distance):
        continue

    if station not in graph:
        graph[station] = []

    graph[station].append((destination, distance, line))

main_plot(df)
traffic_plot(df)
