import streamlit as st
import pandas as pd
import plotly.express as px


# Import pages
from overview import show_overview
from top_200 import show_top_200

# Set the title of the app
st.title("Watch Reference Analysis Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ("Overview", "Top 200"))


# Load data
@st.cache_data
def load_data(url):
    return pd.read_csv(url)


try:
    df_chrono = load_data(
        "https://drive.google.com/uc?id=1gPuCoihoOHB-OOrV9IbYaqmIsYSu3dQQ"
    )
    df_LT = load_data(
        "https://drive.google.com/uc?id=1geeUDwGKY14NLtIBBotK9UtC7EoLDicU"
    )
except FileNotFoundError:
    st.error(
        "One or both of the data files could not be found. Please check the file paths."
    )
    st.stop()  # Stop execution of the app

# Step 1: Filter for brand selection (allowing multiple selections)
brands = df_chrono["brand"].unique()

selected_brands = st.multiselect(
    "Select 3 Brands (max 3):",
    brands,
    default=["Audemars Piguet", "Breitling", "Bulgari"],
    max_selections=3,
)

# Filtre DF on selected brands
df_filtered_C = df_chrono[df_chrono["brand"].isin(selected_brands)].copy()
df_filtered_LT = df_LT[df_LT["brand"].isin(selected_brands)].copy()


# Page navigation
if page == "Overview":
    show_overview(df_filtered_C, df_filtered_LT, selected_brands)
elif page == "Top 200":
    show_top_200(df_filtered_C, df_filtered_LT, selected_brands)
