import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

import seaborn as sns
import textwrap
from matplotlib.colors import ListedColormap
from data_cleaning import all_ages


df = pd.read_pickle("data/cleaned_dataframe.pkl")

# Set the title of the app
st.title("Visualizing CDC Cause of Death Data by Age Demographic")

intro_text = '''
The CDC provides data on the leading causes of death for Americans every year by age group. The figure shown below is straight from the CDC website itself. Immediately you notice that a very large category is "Unintentional Injury", which is the most common cause of death for ages 1-44. 

What exactly is "Unintentional Injury"? Well, its a host of many different types of causes, but the most common is **Motor Vehicle's**. What would this plot look like if we separated out **Motor Vehicle's** as their own cause of death?
'''

st.markdown(intro_text)

image = Image.open('assets/WISQARS_original_data.jpeg')

st.image(image, caption='Original CDC data visualization from here: https://wisqars.cdc.gov/data/lcd/home')


transition_text = '''
We pull the [CDC's own data](https://wonder.cdc.gov/controller/saved/D76/D316F097) to recreate the above plot. The only difference is that we separate out **Motor Vehicle's** from "Unintentional Injury". Small discrepancies exist due to updates to the dataset and discrepancies in coding.
'''

st.markdown(transition_text)

cats,texts = np.load("data/cats.npy"),np.load("texts.npy")

fig, ax = plt.subplots(figsize=(35,15))
fig.suptitle(f"{n_largest} Leading Causes of Death, United States",fontsize=28)
ax.set_title("2020, Both Sexes, All Ages, All Races",fontsize=20,pad=30)
ax.tick_params(left=False, right=False) 
cmap = ListedColormap(['lightgray','coral','mediumseagreen','deepskyblue','royalblue'])
bounds = [-2,-0.5,0.5,1.5,2.5,3.5,4.5]
ax = sns.heatmap(cats,
                 annot=texts,
                 fmt="",
                 cbar=False,
                 cmap=cmap,linewidths=5,square=True, annot_kws={"size":14})
ax.set_xticklabels(all_ages,fontsize=20)
ax.set_yticks([])
ax.xaxis.tick_top()
ax.tick_params(top=False,bottom=False,right=False,left=False)
st.write(fig)
# Create the dropdown menu
options = ["1-4", "5-14", "15-24", "25-34","35-44","45-54"," 55-64","65-74","75-84","85+"]
selected_age = st.selectbox("Select Age Range", options)

data = df[df['Ten-Year Age Groups Code']==selected_age][['Ten-Year Age Groups Code','ICD Sub-Chapter','Deaths']]

st.altair_chart(alt.Chart(data).mark_bar().encode(
    x=alt.X('ICD Sub-Chapter', sort=None, axis=alt.Axis(labelAngle=-45)),
    y='Deaths',
).properties(title={"text":f"Top {n_largest} Causes of Death for Ages {selected_age}, United States","subtitle":'Based on data from CDC'}), use_container_width=True)

# Add a section at the bottom of the app
st.markdown("---")
st.markdown('<div align="center">This is a work in progress! Feedback and feature ideas are welcome on <a href="https://github.com/charlesxjyang/CDCmortality/issues">Github</a></div>',unsafe_allow_html=True)
# Add links to your GitHub and Twitter profiles
st.markdown('<div align="center">Created by <a href="http://charlesyang.io">Charles Yang</a></div>',unsafe_allow_html=True)
