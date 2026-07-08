import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Buyer Segmentation Dashboard",
    layout="wide"
)

df = pd.read_csv("Buyer segment processed data.csv")
st.title("🏠 Machine Learning Based Buyer Segmentation")

st.markdown(
"""
Analyze buyer behavior, investment patterns,
and customer segments using Machine Learning.
"""
)
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Country",
    options=df["country"].unique(),
    default=df["country"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

purpose = st.sidebar.multiselect(
    "Acquisition Purpose",
    options=df["acquisition_purpose"].unique(),
    default=df["acquisition_purpose"].unique()
)

client_type = st.sidebar.multiselect(
    "Client Type",
    options=df["client_type"].unique(),
    default=df["client_type"].unique()
)



filtered = df[
    (df["country"].isin(country))
    & (df["region"].isin(region))
    & (df["acquisition_purpose"].isin(purpose))
    & (df["client_type"].isin(client_type))
]

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Total Buyers",
    filtered["client_id"].nunique()
)

col2.metric(
    "Average Age",
    round(filtered["age"].mean(),1)
)

col3.metric(
    "Average Satisfaction",
    round(filtered["satisfaction_score"].mean(),2)
)

col4.metric(
    "Clusters",
    filtered["segment"].nunique()
)


st.subheader("Buyer Segmentation Overview")

fig1 = px.histogram(
    filtered,
    x="segment",
    color="segment",
     color_discrete_sequence=[
        "#003f5c",
        "#58508d",
        "#bc5090",
        "#ff6361"
     ]
)

st.plotly_chart(fig1, use_container_width=True)


st.subheader("Buyer Behavior Dashboard")

fig2 = px.histogram(
    filtered,
    x="acquisition_purpose",
    color="segment",
    color_discrete_sequence=px.colors.qualitative.Set2,
    barmode="group"
)

st.plotly_chart(fig2, use_container_width=True)

investor_data = (
    filtered.groupby(['segment', 'acquisition_purpose'])
    .size()
    .reset_index(name='count')
)

#fig2 = px.line(
   # investor_data,
    #x="acquisition_purpose",
    #y="count",
    #color="segment",
    #markers=True,
    #title="Investor Behavior by Segment"
#)

#st.plotly_chart(fig2, use_container_width=True)

st.subheader("Geographic Buyer Analysis")

region_count = (
    filtered.groupby(
        ["region","segment"]
    )
    .size()
    .reset_index(name="count")
)

fig3 = px.bar(
    region_count,
    x="region",
    y="count",
    color="segment"
)

st.plotly_chart(fig3, use_container_width=True)



country_data = (
    filtered.groupby("country")
    .size()
    .reset_index(name="buyers")
)

fig = px.choropleth(
    country_data,
    locations="country",
    locationmode="country names",
    color="buyers",
    title="Global Buyer Distribution"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Customer Satisfaction by Segment")

fig4 = px.box(
    filtered,
    x="segment",
    y="satisfaction_score",
    color="segment"
)

st.plotly_chart(fig4, use_container_width=True)

region_data = (
    filtered.groupby("region")
    ["satisfaction_score"]
    .mean()
    .reset_index()
)

fig = px.scatter(
    region_data,
    x="region",
    y="satisfaction_score",
    size="satisfaction_score",
    color="satisfaction_score"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Loan Behaviour Analysis")

#fig5 = px.histogram(
    #filtered,
    #x="loan_applied",
    #color="segment",
    #barmode="group"
#)

#st.plotly_chart(fig5, use_container_width=True)

#loan_data = pd.crosstab(
    #filtered['segment'],
    #filtered['loan_applied']
#)

#fig = px.imshow(
    #loan_data,
    #text_auto=True,
    #title="Loan Behaviour Heatmap"
#)

#st.plotly_chart(fig, use_container_width=True)
#loan_yes = filtered[filtered["loan_applied"] == "Yes"]
#st.subheader("Loan Behaviour Analysis")

loan_yes = filtered[filtered["loan_applied"] == "Yes"]

fig5 = px.histogram(
    loan_yes,
    x="loan_applied",
    color="segment",
    barmode="group",
   # title="Loan Applied"
)

st.plotly_chart(fig5, use_container_width=True)

#loan_yes = filtered[filtered["loan_applied"] == "Yes"]

loan_data = pd.crosstab(
    loan_yes["segment"],
    loan_yes["loan_applied"]
)

fig = px.imshow(
    loan_data,
    text_auto=True,
    title="Loan Behaviour Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

loan_yes_count = (
    loan_yes.groupby("segment")
    .size()
    .reset_index(name="Loan_Count")
)

fig = px.bar(
    loan_yes_count,
    x="Loan_Count",
    y="segment",
    orientation="h",
    color="Loan_Count",
    title="Buyers Who Applied for Loans"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Loan Behaviour Sunburst Chart")

fig = px.sunburst(
    filtered,
    path=['segment', 'loan_applied'],
    title="Loan Application Behaviour"
)

st.plotly_chart(fig, use_container_width=True)



st.subheader("Segment Insights Panel")

segment_summary = (
    filtered
    .groupby("segment")
    .agg({
        "age":"mean",
        "satisfaction_score":"mean"
    })
    .round(2)
)

st.dataframe(
    segment_summary,
    use_container_width=True
)


st.subheader("Dataset")

st.dataframe(
    filtered,
    use_container_width=True
)
