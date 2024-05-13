import streamlit as st
import pandas as pd
import pydeck as pdk


def main_plot(df):
    points = []
    lines = []

    for _, row in df.iterrows():
        points.append(
            {
                "position": [row["Longitude"], row["Latitude"]],
                "color": row["Point Color"],
                "radius": 67,
                "name": row["Station"],
            }
        )

        destination_row = df[df["Station"] == row["Destination"]]
        if not destination_row.empty:
            destination_longitude = destination_row.iloc[0]["Longitude"]
            destination_latitude = destination_row.iloc[0]["Latitude"]
            lines.append(
                {
                    "sourcePosition": [row["Longitude"], row["Latitude"]],
                    "targetPosition": [destination_longitude, destination_latitude],
                    "color": row["Color"],
                    "width": 3,
                }
            )

    map_layers = [
        pdk.Layer(
            "LineLayer",
            data=lines,
            get_source="sourcePosition",
            get_target="targetPosition",
            get_color="color",
            get_width="width",
        ),
        pdk.Layer(
            "ScatterplotLayer",
            data=points,
            get_position="position",
            get_color="color",
            get_radius="radius",
            get_text="name",
            get_text_size=20,
        ),
    ]

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            initial_view_state=pdk.ViewState(
                latitude=df["Latitude"].mean(),
                longitude=df["Longitude"].mean(),
                zoom=10,
                pitch=0,
            ),
            layers=map_layers,
        ),
    )
