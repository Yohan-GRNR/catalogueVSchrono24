import streamlit as st
import pandas as pd
import plotly.express as px


def show_top_200(df_filtered_C, df_filtered_LT, selected_brands):
    st.header("Top 200 References")  # Header for the next section

    # Create three columns
    col1, col2 = st.columns(2)

    with col1:
        # Create top200 references
        df_200ref = (
            df_filtered_C.groupby(["brand", "reference"])
            .size()
            .reset_index(name="count")
        )

        df_200ref.sort_values("count", ascending=False, inplace=True)
        df_200ref = df_200ref.head(200)

        st.write("Top 200 References")
        st.dataframe(df_200ref, use_container_width=True, hide_index=True)

    with col2:
        # Create top200 reference with Year of Production
        df_200ref_YOP = (
            df_filtered_C.groupby(["brand", "reference", "yearOfProduction"])
            .size()
            .reset_index(name="count")
        )

        df_200ref_YOP.sort_values("count", ascending=False, inplace=True)
        df_200ref_YOP = df_200ref_YOP.head(200)

        st.write("Top 200 References - YOP")
        st.dataframe(df_200ref_YOP, use_container_width=True, hide_index=True)

    st.header("Watch Year of Production Distribution")

    # Create a histogram with auto-binning for each brand
    fig = px.histogram(
        df_200ref_YOP,
        x="yearOfProduction",
        color="brand",
        title="Distribution of Year of Production by Brand",
        barmode="overlay",
    )

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)
