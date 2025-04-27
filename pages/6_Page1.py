import streamlit as st
import streamlit as st
import duckdb as db
import pandas as pd
import plotly.express as px

st.write("# Top 10 จำนวนสาขาของ Starbucks แยกตาม Timezone 🔝 1️⃣0️⃣")
df = pd.read_csv("Starbucks.csv")
#st.write(df)

timezone = db.sql(
    """Select Timezone, COUNT(*) AS count 
    FROM df 
    GROUP BY Timezone 
    ORDER BY count DESC 
    LIMIT 10 
    """).df()

fig1 = px.bar(timezone,x="Timezone",y="count",text_auto = True)
fig1.update_layout(
    title = "10 อันดับ Timezone ที่จำนวนสาขามากที่สุด",
    xaxis_title = "Timezone",
    yaxis_title = "จำนวนสาขา",
)
st.plotly_chart(fig1)
