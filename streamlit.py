import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


df = pd.read_pickle("data/cleaned_dataframe.pkl")

# Set the title of the app
st.title("Visualizing CDC Cause of Death Data by Age Demographic")

intro_text = '''
The CDC provides data on the leading causes of death for Americans every year by age group. The figure shown below is straight from the CDC website itself. Immediately you notice that a very large category is "Unintentional Injury", which is the most common cause of death for ages 1-44. 

What exactly is "Unintentional Injury"? Well, its a host of many different types of causes, but the most common is **Motor Vehicle Traffic**. This website uses CDC data to show what their own figure would look like if **Motor Vehicle Traffic** was its own cause of death.  
'''

st.markdown(intro_text)

image = Image.open('assets/WISQARS_original_data.jpeg')

st.image(image, caption='Original CDC data visualization from here: https://wisqars.cdc.gov/data/lcd/home')

st.dataframe(df)

# Create the dropdown menu
options = ["1-4", "5-14", "15-24", "25-34","35-44","45-54"," 55-64","65-74","75-84","85+"]
selected_age = st.selectbox("Select Age Range", options)

data = df[df['Ten-Year Age Groups Code']==selected_age][['Ten-Year Age Groups Code','ICD Sub-Chapter','Deaths']]

st.write(data)
st.altair_chart(alt.Chart(data).mark_bar().encode(
    x=alt.X('ICD Sub-Chapter', sort=None),
    y='Deaths',
), use_container_width=True)

# Add a section at the bottom of the app
st.markdown("---")
st.markdown('<div align="center">This is a work in progress! Feedback and feature ideas are welcome on [Github](https://github.com/charlesxjyang/CDCmortality/issues)</div>',unsafe_allow_html=True)
# Add links to your GitHub and Twitter profiles
st.markdown('<div align="center">Created by [Charles Yang](http://charlesyang.io)</div>',unsafe_allow_html=True)
