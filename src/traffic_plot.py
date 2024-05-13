import streamlit as st
import pandas as pd
import pydeck as pdk


def traffic_plot(df):
    chart_data = df.iloc[:, [5, 6, 7]]
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=40.41248995,
                longitude=-3.699402901,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=chart_data,
                    get_position="[Longitude, Latitude]",
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 500],
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=chart_data,
                    get_position="[Longitude, Latitude]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=200,
                ),
            ],
        )
    )
