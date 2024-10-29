import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


def show_overview(df_filtered_C, df_filtered_LT, selected_brands):

    # Title of the dashboard
    st.title("Watch Reference Analysis Dashboard")

    # Create three columns
    col1, col2, col3 = st.columns(3)

    with col1:
        # -------------- Catalogue Chrono24

        df_filtered_C_uniref = (
            df_filtered_C.drop_duplicates(subset="reference")
            .groupby("brand")
            .size()
            .reset_index(name="count")
        )

        st.write("\# references in Chrono24 catalogue :")
        st.dataframe(df_filtered_C_uniref, use_container_width=True, hide_index=True)

    with col3:

        # -------------- Catalogue Luxtech

        df_filtered_LT_uniref = (
            df_filtered_LT.drop_duplicates(subset="modelNumber")
            .groupby("brand")
            .size()
            .reset_index(name="count")
        )
        for brand in selected_brands:
            if brand not in df_filtered_LT_uniref["brand"].values:
                df_filtered_LT_uniref = pd.concat(
                    [
                        df_filtered_LT_uniref,
                        pd.DataFrame(
                            {
                                "brand": [brand],
                                "count": "Not in the catalogue for the moment.",
                            }
                        ),
                    ],
                    ignore_index=True,
                )

        st.write("\# references in Luxtech catalogue :")
        st.dataframe(df_filtered_LT_uniref, use_container_width=True, hide_index=True)

    with col2:
        # -------------- Catalogue Common

        df_filtered_common = df_filtered_C[
            df_filtered_C["reference"].isin(df_filtered_LT["modelNumber"])
        ]  # .drop_duplicates(subset="reference")

        df_filtered_common_uniref = (
            df_filtered_common.drop_duplicates(subset="reference")
            .groupby("brand")
            .size()
            .reset_index(name="count")
        )
        # Create a DataFrame for missing brands
        missing_brands = [
            brand
            for brand in selected_brands
            if brand not in df_filtered_common_uniref["brand"].values
        ]

        if missing_brands:
            missing_df = pd.DataFrame(
                {
                    "brand": missing_brands,
                    "count": ["Not in the catalogue for the moment."]
                    * len(missing_brands),
                }
            )
            df_filtered_common_uniref = pd.concat(
                [df_filtered_common_uniref, missing_df], ignore_index=True
            )

        # Calculate the percentage with a security check
        df_filtered_common_uniref["% of Chrono24"] = np.where(
            df_filtered_C_uniref["count"].astype(str).str.isnumeric()
            & (df_filtered_C_uniref["count"] != "0"),
            round(
                (
                    df_filtered_common_uniref["count"]
                    .replace("Not in the catalogue for the moment.", 0)
                    .astype(float)
                    / df_filtered_C_uniref["count"].astype(float)
                    * 100
                ),
                1,
            ),
            0,  # Assign 0 if the count in df_filtered_C_uniref is zero or not numeric
        )
        st.write("\n \n<== # references shared ==>")
        st.dataframe(
            df_filtered_common_uniref, use_container_width=True, hide_index=True
        )
    # =================================================================================
    # ---------- On Chrono24 datas
    st.markdown("---")
    show_chrono24_details = st.checkbox("Show Chrono24 details")
    if show_chrono24_details:
        df_filtered_C.sort_values("yearOfProduction", ascending=True, inplace=True)

        st.dataframe(
            df_filtered_C, use_container_width=True, hide_index=True, height=200
        )

        # --- # ref per YOP
        fig_year = px.histogram(
            df_filtered_C,
            x="yearOfProduction",
            color="brand",
            title="Distribution of Year of Production - Chrono24 data",
            barmode="overlay",
        )
        st.plotly_chart(
            fig_year, use_container_width=True, key="chrono24_year_distribution"
        )

        # --- pourcents
        df_pourcent = (
            df_filtered_C.groupby(["brand", "reference"])
            .agg(count=("reference", "count"))
            .reset_index()
        )

        # Calculate the total count for each brand
        df_pourcent["total_count"] = df_pourcent.groupby("brand")["count"].transform(
            "sum"
        )

        # Calculate the percentage
        df_pourcent["percentage"] = round(
            df_pourcent["count"] / df_pourcent["total_count"] * 100, 1
        )  # Multiply by 100 for percentage

        # Drop the 'total_count'
        df_pourcent.drop(columns="total_count", inplace=True)

        fig_percentage = px.bar(
            df_pourcent,
            x="reference",
            y="percentage",
            color="brand",
            title="Percentage of References by Brand - Chrono24 Data",
            labels={"percentage": "Percentage (%)"},
            text="percentage",
        )
        # Show the figure
        st.plotly_chart(
            fig_percentage,
            use_container_width=True,
            key="chrono24_percentage_references",
        )

        # --- # reference
        fig_reference = px.histogram(
            df_filtered_C.sort_values("brand", ascending=True),
            x="reference",
            color="brand",  # Color by brand
            title="# Reference by Brand - Chrono24 data",
            barmode="overlay",
        )
        # Show the figure
        st.plotly_chart(
            fig_reference, use_container_width=True, key="chrono24_reference_by_brand"
        )

    # ---------- On Common datas
    st.markdown("---")
    show_common_details = st.checkbox("Show details (common ref. in both catalogue)")

    if show_common_details:
        df_filtered_common.sort_values("yearOfProduction", ascending=True, inplace=True)

        st.dataframe(
            df_filtered_common, use_container_width=True, hide_index=True, height=200
        )

        # --- # ref per YOP
        fig_year_common = px.histogram(
            df_filtered_common,
            x="yearOfProduction",
            color="brand",
            title="Distribution of Year of Production - Common data",
            barmode="overlay",
        )
        st.plotly_chart(
            fig_year_common, use_container_width=True, key="common_year_distribution"
        )

        df_pourcent = (
            df_filtered_C.groupby(["brand", "reference"])
            .agg(count=("reference", "count"))
            .reset_index()
        )

        # Calculate the total count for each brand
        df_pourcent["total_count"] = df_pourcent.groupby("brand")["count"].transform(
            "sum"
        )

        # Calculate the percentage
        df_pourcent["percentage"] = round(
            df_pourcent["count"] / df_pourcent["total_count"] * 100, 1
        )  # Multiply by 100 for percentage

        # Drop the 'total_count'
        df_pourcent.drop(columns="total_count", inplace=True)

        fig_percentage_common = px.bar(
            df_pourcent,
            x="reference",
            y="percentage",
            color="brand",
            title="Percentage of References by Brand - Chrono24 Data",
            labels={"percentage": "Percentage (%)"},
            text="percentage",
        )
        # Show the figure
        st.plotly_chart(
            fig_percentage_common,
            use_container_width=True,
            key="common_percentage_references",
        )

        # --- # reference
        fig_reference_common = px.histogram(
            df_filtered_common.sort_values("brand", ascending=True),
            x="reference",
            color="brand",  # Color by brand
            title="# Reference by Brand - Common data",
            barmode="overlay",
        )
        # Show the figure
        st.plotly_chart(
            fig_reference_common,
            use_container_width=True,
            key="common_reference_by_brand",
        )

    # ---------- On Luxtech datas
    st.markdown("---")
    show_luxtech_details = st.checkbox("Show Luxtech catalogue details")

    if show_luxtech_details:

        st.dataframe(
            df_filtered_LT, use_container_width=True, hide_index=True, height=200
        )

        fig_luxtech = px.histogram(
            df_filtered_LT.sort_values("brand", ascending=True),
            x="modelNumber",
            color="brand",  # Color by brand
            title="# Reference by Brand - Luxtech data",
            barmode="overlay",
        )
        # Show the figure
        st.plotly_chart(
            fig_luxtech, use_container_width=True, key="luxtech_reference_by_brand"
        )
