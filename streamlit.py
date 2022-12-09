import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

import seaborn as sns
from data_cleaning import display_ages, n_largest, create_heatmap

df = pd.read_pickle("data/cleaned_dataframe.pkl")

# Set the title of the app
st.title("CDC Leading Cause's of Death Data and Cars")

intro_text = '''
The [CDC provides data on the leading causes of death for Americans every year by age group](https://wisqars.cdc.gov/data/lcd/home). The figure shown below is a snipped version from the CDC website. Immediately you notice that a very large category is `Unintentional Injury`, which is the most common cause of death for ages 1-44. 

What exactly constitutes an `Unintentional Injury`? Well, it serves as a bucket category for many different types of causes, but the most common cause of death contained within `Unintentional Injury` is `Motor vehicle, traffic`, that is, deaths that result from being in a car or hit by a car. What would this plot look like if we separated out `Motor Vehicles` as their own cause of death?
'''

st.markdown(intro_text)

image = Image.open('assets/WISQARS_original_data_snip.jpeg')
st.image(
  image,
  caption=
  'Original CDC data visualization from here: https://wisqars.cdc.gov/data/lcd/home'
)

transition_text = '''
I pulled the [CDC's own data](https://wonder.cdc.gov/controller/saved/D76/D316F097) to recreate the above plot. The only difference is that we separate out `Motor Vehicles` from `Unintentional Injury`. Small discrepancies exist due to updates to the dataset and discrepancies in coding.
'''

st.markdown(transition_text)

fig = create_heatmap(df)
st.write(fig)

# Create the dropdown menu

bar_chart_text = '''
You can also plot the number of deaths from each cause by age group here below:
'''

st.markdown(bar_chart_text)

selected_age = st.selectbox("Select Age Range", display_ages)

data = df[df['Ten-Year Age Groups Code'] == selected_age][[
  'Ten-Year Age Groups Code', 'ICD Sub-Chapter', 'Deaths'
]]

st.altair_chart(alt.Chart(data).mark_bar().encode(
  x=alt.X('ICD Sub-Chapter',
          sort=None,
          axis=alt.Axis(labelAngle=-45, title="Cause of Death")),
  y='Deaths',
).properties(
  title={
    "text":
    f"Top {n_largest} Causes of Death for Ages {selected_age}, United States",
    "subtitle": 'Based on data from CDC'
  }),
                use_container_width=True)

# Add a section at the bottom of the app
st.markdown("---")
st.markdown(
  '<div align="center">This is a work in progress! Feedback and feature ideas are welcome on <a href="https://github.com/charlesxjyang/CDCmortality/issues">Github</a>. You can play around with the data cleaning and plotting on <a href="https://replit.com/@charlesxjyang/CDCmortality">Replit</a> </div>',
  unsafe_allow_html=True)
st.markdown(
  '<div align="center">Created by <a href="http://charlesyang.io">Charles Yang</a></div>',
  unsafe_allow_html=True)
