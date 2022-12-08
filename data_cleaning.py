import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap
from matplotlib.colors import ListedColormap

### Constants

path_to_data = "data/Underlying Cause of Death, 1999-2020.txt"

n_largest = 5

keep_ages_under_1 = False
  
all_ages = [
    "1-4", "5-14", "15-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75-84",
    "85+"
  ]

if keep_ages_under_1:
    all_ages.insert(0, "1")

display_ages = ["1-4", "5-14", "15-24", "25-34", "35-44", "45-54", "55-64"]

#### load data and data cleaning
df = pd.read_csv(path_to_data, sep='\t', lineterminator='\r')
index = df[df['Notes'] != '\n'].index
df = df.drop(index, axis=0)
index = df[df['Ten-Year Age Groups Code'] == 'NS'].index
df = df.drop(index, axis=0)
#dropping infants because too complicated
if not keep_ages_under_1:
  index = df[df['Ten-Year Age Groups Code'] == '1'].index
  df = df.drop(index, axis=0)

df = df.drop(["Ten-Year Age Groups", "Population", "Notes"], axis=1)
df = df.head(1538)  #remove readme stuff at end
df[['Deaths']] = df[['Deaths']].astype(int)
### Remove Traffic Deaths


def combine_data(df, features_code, new_code, new_chapter):

  for age in df['Ten-Year Age Groups Code'].unique():
    sub_df = df[df['Ten-Year Age Groups Code'] == age]
    initialize = sub_df['ICD Sub-Chapter Code'] == features_code[0]
    for feat in features_code:
      initialize = (initialize | (sub_df["ICD Sub-Chapter Code"] == feat))
    rows = initialize
    deaths = sub_df[rows]['Deaths'].sum()
    sub_df.loc[rows, 'Crude Rate'] = pd.to_numeric(
      sub_df[rows]['Crude Rate'],
      errors='coerce')  # just ignore unreliable entries
    crude_rate = sub_df[rows]['Crude Rate'].sum(skipna=True)

    df = pd.concat([
      df,
      pd.DataFrame(
        {
          "Ten-Year Age Groups Code": age,
          "ICD Sub-Chapter": new_chapter,
          "ICD Sub-Chapter Code": new_code,
          "Deaths": deaths,
          "Crude Rate": crude_rate
        },
        index=[0])
    ],
                   axis=0,
                   ignore_index=True)
  for feat in features_code:
    df = df.drop(df[(df["ICD Sub-Chapter Code"] == feat)].index, axis=0)
  return df


#### Engineer Other Data
df = combine_data(df, ["W00-X59", "Y85-Y89"], "W00-X59,Y85-Y89",
                  'Unintentional Deaths besides Motor Vehicles')

#based off of this reference: https://www.cdc.gov/injury/wisqars/fatal_help/causes_icd10.html

df = combine_data(df, ["D50-D53", "D55-D59", "D60-D64"], "D50-D64", 'Anaemia')

df = combine_data(df, ["D00-D09", "D10-D36", "D37-D48"], "D00-D48",
                  'Benign neoplasm')

df = combine_data(df, [
  "O00-O07", "O10-O16", "O20-O29", "O30-O48", "O60-O75", "O85-O92", "O95-O99"
], "O00-O99", 'Complicated Pregnancy')

df = combine_data(df, [
  "Q00-Q07", "Q20-Q28", "Q30-Q34", "Q38-Q45", "Q60-Q64", "Q65-Q79", "Q80-Q89",
  "Q90-Q99"
], "Q00-Q99", 'Congenital Anomalies')

df = combine_data(
  df, ["I00-I02", "I05-I09", "I10-I15", "I20-I25", "I26-I28", "I30-I51"],
  "I00-I51", 'Heart Disease')

df = combine_data(df, ["N00-N07", "N10-N15", "N17-N19", "N25-N28"], "N00-I28",
                  'Nephritis')

df = combine_data(df, ["E40-E46", "E50-E64"], "E40-E64",
                  'Nutritional Deficiency')

df = combine_data(
  df, ["P00-P04", "P10-P15", "P20-P29", "P35-P39", "P50-61", "P90-P96"],
  "P00-P96", 'Perinatal Period')


## Shortening names
def rename_data(df, code, new_name):
  df.loc[df['ICD Sub-Chapter Code'] == code, 'ICD Sub-Chapter'] = new_name
  return df


df = rename_data(df, "G30-G31", 'Alzheimers')

df = rename_data(df, "U00-U49", 'COVID-19*')

df = rename_data(df, "B20-B24", 'HIV')

df = rename_data(df, "X60-X84", 'Suicide')

df = rename_data(df, "X85-Y09", 'Homocide')

df = rename_data(df, "V01-V99", 'Motor Vehicles')

## Only keep n_largest causes of death and save dataframe

df = df.groupby('Ten-Year Age Groups Code').apply(
  lambda grp: grp.nlargest(n_largest, "Deaths")).reset_index(drop=True)

df[['Crude Rate']] = df[['Crude Rate']].astype(float)

df.to_pickle("data/cleaned_dataframe.pkl")

#11 distinct age groups

def create_heatmap(df):
    
  texts,cats = np.empty(
    (n_largest, len(display_ages)), dtype=object),np.empty((n_largest,len(display_ages))) 
  
  def one_hot_encode_category(sub_chapter):
    if sub_chapter == "Homocide":
      return 0
    elif sub_chapter == 'Suicide':
      return 1
    elif sub_chapter == 'Motor Vehicles':
      return 2
    elif sub_chapter == 'Unintentional Deaths besides Motor Vehicles':
      return 3
    else:
      return -1
    
  for idx, age in enumerate(display_ages):
    sub_df = df[df['Ten-Year Age Groups Code'] == age]
    vals = sub_df['Deaths'].values
    codes = sub_df['ICD Sub-Chapter']
    assert len(vals) == n_largest
    assert len(codes) == n_largest
    new_codes = [textwrap.fill(c,16) + "\n" + "{:,}".format(v) for v,c in zip(vals,codes)]
    texts[:, idx] = new_codes
    cats[:,idx] = [one_hot_encode_category(c) for c in codes]
    
  
  fig, ax = plt.subplots(figsize=(35,15))
  ax.tick_params(left=False, right=False) 
  cmap = ListedColormap(['lightgray','coral','mediumseagreen','deepskyblue','royalblue'])
  bounds = [-2,-0.5,0.5,1.5,2.5,3.5,4.5]
  ax = sns.heatmap(cats,
                   annot=texts,
                   fmt="",
                   cbar=False,
                   cmap=cmap,linewidths=5,square=True, annot_kws={"size":19})
  ax.set_xticklabels(display_ages,fontsize=20)
  ax.set_yticks([])
  ax.xaxis.tick_top()
  
  ax.tick_params(top=False,bottom=False,right=False,left=False)
  return fig
fig = create_heatmap(df)
fig.savefig("assets/heatmap.png")
