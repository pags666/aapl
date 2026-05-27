# =========================================================
# AAPALLA CENTRAL HOSPITAL MONITORING SYSTEM
# =========================================================

# INSTALL:
# pip install pandas plotly

# =========================================================
# IMPORTS
# =========================================================

import pandas as pd
import plotly.express as px
import streamlit as st
# =========================================================
# GOOGLE SHEET CSV URLS
# =========================================================

st.set_page_config(layout="wide")

sheet_urls = {

    "AAPLMS1":
    "https://docs.google.com/spreadsheets/d/1eECpcgOguZyhQ6ct5Va1Bic1vzb_3TkbQF6Ku-1ARv8/export?format=csv&gid=0",

    "AAPLMS2":
    "https://docs.google.com/spreadsheets/d/1eECpcgOguZyhQ6ct5Va1Bic1vzb_3TkbQF6Ku-1ARv8/export?format=csv&gid=1700825465",

    "AAPLTPJ":
    "https://docs.google.com/spreadsheets/d/1eECpcgOguZyhQ6ct5Va1Bic1vzb_3TkbQF6Ku-1ARv8/export?format=csv&gid=216738042",

    "AAPLTEN":
    "https://docs.google.com/spreadsheets/d/1eECpcgOguZyhQ6ct5Va1Bic1vzb_3TkbQF6Ku-1ARv8/export?format=csv&gid=191035573",

    "AAPLCBE":
    "https://docs.google.com/spreadsheets/d/1eECpcgOguZyhQ6ct5Va1Bic1vzb_3TkbQF6Ku-1ARv8/export?format=csv&gid=2127107420",

    "AAPLMDU":
    "https://docs.google.com/spreadsheets/d/1eECpcgOguZyhQ6ct5Va1Bic1vzb_3TkbQF6Ku-1ARv8/export?format=csv&gid=942749837"
}

# =========================================================
# LOAD ALL SHEETS
# =========================================================

all_data = []

for hospital, url in sheet_urls.items():

    temp_df = pd.read_csv(url)

    temp_df["Hospital"] = hospital

    all_data.append(temp_df)

# =========================================================
# COMBINE DATA
# =========================================================

df = pd.concat(all_data, ignore_index=True)

# =========================================================
# REMOVE EMPTY ROWS
# =========================================================

df = df.dropna(subset=["Department"])

df = df[df["Department"].astype(str).str.strip() != ""]

# =========================================================
# CLEAN PERCENTAGE COLUMN
# =========================================================

df["Availability_Value"] = (

    df["Bed Availability (%)"]

    .astype(str)

    .str.replace("%", "")

    .astype(int)
)

# =========================================================
# BED STATUS
# =========================================================

df["Bed Status"] = (

    df["Available Beds"].astype(str)

    + "/"

    + df["Total Beds"].astype(str)
)

# =========================================================
# TREEMAP
# =========================================================

fig = px.treemap(

    df,

    path=[
        px.Constant("AAPL"),
        "Hospital",
        "Department"
    ],

    values="Total Beds",

    color="Availability_Value",
    range_color=(0, 60),

    hover_data={

        "Total Beds": True,

        "Admitted Patients": True,

        "Available Beds": True,

        "Bed Availability (%)": True,

        "Bed Status": True,

        "Availability_Value": False
    },

    color_continuous_scale=[
        "#FF0000",
        "#FFA500",
        "#00FF00"
    ],

    color_continuous_midpoint=30
)

# =========================================================
# TEXT INSIDE BOX
# =========================================================

fig.data[0].texttemplate = (

    "<b>%{label}</b>"

    "<br>"

    "%{customdata[4]}"
)

# =========================================================
# TREEMAP STYLE
# =========================================================

fig.update_traces(

    textposition="middle center",

    marker_line_width=2,

    marker_line_color="black",

    hovertemplate=

    "<b>%{label}</b><br><br>"

    +

    "Total Beds: %{customdata[0]}<br>"

    +

    "Admitted Patients: %{customdata[1]}<br>"

    +

    "Available Beds: %{customdata[2]}<br>"

    +

    "Availability: %{customdata[3]}<br>"

    +

    "Bed Status: %{customdata[4]}<br>"

    +

    "<extra></extra>"
)

# =========================================================
# LAYOUT
# =========================================================

fig.update_layout(

    title="AAPL Central Hospital Monitoring System",

    margin=dict(
        t=50,
        l=20,
        r=20,
        b=20
    ),

    font_size=14,

    height=900
)

# =========================================================
# SHOW TREEMAP
# =========================================================

st.title("AAPL Central Hospital Monitoring System")

st.plotly_chart(
    fig,
    use_container_width=True
)
