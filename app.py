import streamlit as st
import pandas as pd
import altair as alt

# Load data
df = pd.read_csv("C:\\Users\\jdric\\Downloads\\yearly_deaths_by_clinic.csv")
df.columns = df.columns.str.strip()
# Calculate mortality rate
df['mortality_rate'] = (df['Deaths'] / df['Birth']) * 100

# Title and description
st.title("Wash Your Hands or DIE!!!")
st.write("""
Dr. Semmelweis's case study on maternal mortality.
Highlighting the impact of hand-washing in clinics Startring in the 1840s.
    This dashboard visualizes the affect of hand-washing on mortality rates in two clinics.
""")

# Clinic filter
clinic = st.selectbox("Select Clinic:", df['Clinic'].unique())

# Filtered data for mortality chart
filtered_df = df[df['Clinic'] == clinic]

# Mortality rate chart
mortality_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
    x='Year:O',
    y='mortality_rate:Q',
    tooltip=['Year', 'mortality_rate']
).properties(title=f"Mortality Rate in {clinic}")
st.altair_chart(mortality_chart, use_container_width=True)

# Prepare data for births vs deaths chart
melted_df = df.melt(id_vars=['Year', 'Clinic'], value_vars=['Birth', 'Deaths'],
                    var_name='Type', value_name='Count')

# Filter melted data for selected clinic
melted_filtered = melted_df[melted_df['Clinic'] == clinic]

# Births vs Deaths chart with check
if not melted_filtered.empty:
    birth_death_chart = alt.Chart(melted_filtered).mark_line(point=True).encode(
        x='Year:O',
        y='Count:Q',
        color='Type:N',
        tooltip=['Year', 'Type', 'Count']
    ).properties(title=f"Births vs Deaths in {clinic}")
    st.altair_chart(birth_death_chart, use_container_width=True)
else:
    st.warning("No data available for this selection.")

# Findings
st.write("""
**Findings:** Mortality rates dropped dramatically after 1847 when hand-washing was introduced.
Clinic 1 had a much higher mortality rate before this intervention compared to Clinic 2.
""")