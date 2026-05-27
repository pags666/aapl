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
# =========================================================
# SHOW MAIN TREEMAP
# =========================================================

st.title("AAPL Central Hospital Monitoring System")

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# GENERAL MEDICINE PATIENT DATA
# =========================================================

gm_url = "https://docs.google.com/spreadsheets/d/1eECpcgOguZyhQ6ct5Va1Bic1vzb_3TkbQF6Ku-1ARv8/export?format=csv&gid=1018029888"

gm_data = pd.read_csv(gm_url)

# =========================================================
# RISK SCORE
# =========================================================

risk_map = {

    "Low": 30,

    "Medium": 60,

    "High": 90
}

gm_data["Risk Score"] = gm_data["Risk Level"].map(risk_map)

# =========================================================
# PATIENT TREEMAP
# =========================================================

gm_fig = px.treemap(

    gm_data,

    path=[
        px.Constant("AAPLMS1"),
        px.Constant("General Medicine"),
        "Patient ID"
    ],

    values="Heart Rate",

    color="Risk Score",

    range_color=(0,100),

    hover_data={

        "Bed No": True,

        "Age": True,

        "Gender": True,

        "Heart Rate": True,

        "Blood Pressure": True,

        "SpO2": True,

        "Temp (°F)": True,

        "Resp Rate": True,

        "Risk Level": True
    },

    color_continuous_scale=[
        "#00FF00",
        "#FFA500",
        "#FF0000"
    ]
)

# =========================================================
# TEXT INSIDE PATIENT BOX
# =========================================================

gm_fig.data[0].texttemplate = (

    "<b>%{label}</b>"

    "<br>"

    "HR: %{value}"
)

# =========================================================
# STYLE
# =========================================================

gm_fig.update_traces(

    marker_line_width=2,

    marker_line_color="black",

    textposition="middle center",

    hovertemplate=

    "<b>%{label}</b><br><br>"

    +

    "Bed No: %{customdata[0]}<br>"

    +

    "Age: %{customdata[1]}<br>"

    +

    "Gender: %{customdata[2]}<br>"

    +

    "Heart Rate: %{customdata[3]}<br>"

    +

    "Blood Pressure: %{customdata[4]}<br>"

    +

    "SpO2: %{customdata[5]}<br>"

    +

    "Temperature: %{customdata[6]}<br>"

    +

    "Resp Rate: %{customdata[7]}<br>"

    +

    "Risk Level: %{customdata[8]}<br>"

    +

    "<extra></extra>"
)

# =========================================================
# LAYOUT
# =========================================================

gm_fig.update_layout(

    title="AAPLMS1 - General Medicine Patient Monitoring",

    height=850,

    font_size=13
)

# =========================================================
# SHOW PATIENT TREEMAP
# =========================================================

st.plotly_chart(
    gm_fig,
    use_container_width=True
)
