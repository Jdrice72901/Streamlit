import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/jdrice72901/streamlit/main/yearly_deaths_by_clinic.csv")

df.columns = df.columns.str.strip()
df.columns = ["Year", "Births", "Deaths", "Clinic"]
df["MortalityRate"] = df["Deaths"] / df["Births"]

st.set_page_config(page_title="Semmelweis Handwashing", layout="wide")

# -------------------------
# Compute Useful Stats
# -------------------------
pre_hw = df[df["Year"] < 1847]
post_hw = df[df["Year"] >= 1847]

avg_pre = pre_hw["MortalityRate"].mean()
avg_post = post_hw["MortalityRate"].mean()
decline_pct = round((avg_pre - avg_post) / avg_pre * 100, 1)

peak_deaths = df["Deaths"].max()
lowest_post = post_hw["Deaths"].min()

# -------------------------
# Title Section
# -------------------------
st.title("🧼 How Handwashing Transformed Maternal Safety in Vienna")

st.markdown(
    f"""
   > **Created by:** Jake Rice, Mam Salan Njie, Tyler 
   > **Key finding:** After Semmelweis introduced handwashing in **1847**,  
    the average mortality rate fell by **{decline_pct}%**, marking one of the earliest and most powerful 
    demonstrations of infection control in medical history.
    """
)

# -------------------------
# KPI STATISTICS
# -------------------------
colA, colB, colC = st.columns(3)

colA.metric("📉 Avg Mortality Before 1847", f"{avg_pre:.2%}")
colB.metric("📈 Avg Mortality After 1847", f"{avg_post:.2%}")
colC.metric("💡 Mortality Reduction", f"{decline_pct}%", "- improvement")

st.markdown("---")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔍 Explore the Data")

clinic_choice = st.sidebar.multiselect(
    "Choose clinics:",
    options=df["Clinic"].unique(),
    default=df["Clinic"].unique()
)

year_range = st.sidebar.slider(
    "Filter Years:",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(int(df["Year"].min()), int(df["Year"].max()))
)

highlight_hw = st.sidebar.checkbox("Highlight 1847 (handwashing introduced)", value=True)

filtered = df[
    (df["Clinic"].isin(clinic_choice)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# -------------------------
# Section 1 – Deaths Over Time
# -------------------------
st.subheader("📉 Deaths Drop Dramatically After Handwashing Begins")

st.markdown(
    f"""
    **Insight:** Before handwashing, deaths peaked at **{peak_deaths}** in a single year.  
    After 1847, the lowest recorded number of deaths dropped to **{lowest_post}** — a powerful 
    indicator of the life-saving impact of hygiene.
    """
)

col1, col2 = st.columns([3, 1])

# Chart
with col1:
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    for clinic in filtered["Clinic"].unique():
        sub = filtered[filtered["Clinic"] == clinic]
        ax1.plot(sub["Year"], sub["Deaths"], marker="o", label=clinic)

    if highlight_hw:
        ax1.axvline(1847, color="red", linestyle="--", label="Handwashing Introduced (1847)")

    ax1.set_xlabel("Year")
    ax1.set_ylabel("Deaths")
    ax1.legend()
    st.pyplot(fig1)

# Side Insight Box
with col2:
    st.markdown("### 🔍 Quick Stats")
    st.write(f"**Peak deaths:** {peak_deaths}")
    st.write(f"**Lowest deaths after 1847:** {lowest_post}")
    st.write(f"**Clinics shown:** {', '.join(clinic_choice)}")

st.markdown("---")

# -------------------------
# Section 2 – Mortality Rate
# -------------------------
st.subheader("📊 Mortality Rate Shows the Clear Impact of Hygiene Practices")

fig2, ax2 = plt.subplots(figsize=(8, 4))
for clinic in filtered["Clinic"].unique():
    sub = filtered[filtered["Clinic"] == clinic]
    ax2.bar(sub["Year"], sub["MortalityRate"], alpha=0.6, label=clinic)

if highlight_hw:
    ax2.axvline(1847, color="red", linestyle="--")

ax2.set_xlabel("Year")
ax2.set_ylabel("Mortality Rate (Deaths / Births)")
ax2.legend()
st.pyplot(fig2)

st.markdown(
    f"""
    **Interpretation:**  
    Mortality rates in Clinic 1 fell by **{decline_pct}%** after 1847.  
    Clinic 2 consistently had lower mortality, suggesting differences in training or procedures.
    """
)

st.markdown("---")

# -------------------------
# Data Table
# -------------------------
st.subheader("📋 Explore Filtered Data")
st.dataframe(filtered)

st.caption("Created for DSBA Streamlit Assignment — Interactive Semmelweis Visualization")




