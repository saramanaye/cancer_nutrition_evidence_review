import re
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from load_data import load_evidence_table


#select columns to keep
columns_to_keep = [
    "Author",
    "Year",
    "Study Design",
    "Sample size (dropouts)",
    "Cancer Type",
    "Aerobic exercise",
    "Resistance training",
    "Respiratory Muscle Training",
    "Protein supplementation",
    "Dietary councelling",
    "Complete Oral Nutritional Supplement",
    "Micronutrients supplementation",
    "Psychological interventions",
    "Duration of Intervention",
    "Primary Outcome",
    "Functional Capacity",
    "Post-operative complications",
    "Length of hospital stay",
    "Nutritional Status",
    "Quality of Life",
    "Neoadjuvant chemotherapy adherence",
    "Overall Risk of bias",
    "Concerning domain(s)"
]                            


interventions = [
    "Aerobic exercise",
    "Resistance training",
    "Respiratory Muscle Training",
    "Protein supplementation",
    "Dietary councelling",
    "Complete Oral Nutritional Supplement",
    "Micronutrients supplementation",
    "Psychological interventions",
]

outcomes = [
    "Functional Capacity",
    "Post-operative complications",
    "Length of hospital stay",
    "Nutritional Status",
    "Quality of Life",
    "Neoadjuvant chemotherapy adherence",
]

# Data cleaning 

# Remove white space/new lines on any string
def strip_str(x):
    if isinstance(x,str):
        return re.sub(r"\s+"," ",x.strip())
    return x

# Covert intervention labels to 'Yes'/'No'/'Not reported'
def normalise_intervention(x):
    if pd.isna(x):
        return "Not reported"
    x=str(x).strip().lower()
    if x.startswith("yes"):
        return "Yes"
    if x.startswith("no") and "not" not in x:
        return "No"
    return "Not reported"

# Convert outcome labels to 'Improved'/'No effect'/'Not reported'
def normalise_outcome(x):
    if pd.isna(x):
        return "Not reported"
    x=str(x).strip().lower()
    if x.startswith("improv"):
        return "Improved"
    if x.startswith("no effect"):
        return "No effect"
    return "Not reported"

# Convert risk of bias labels to 'Low'/'High'/'Some concerns'
def normalise_rob(x):
    if pd.isna(x):
        return "Unclear"
    x=str(x).strip().lower()
    if x.startswith("low"):
        return "Low"
    if x.startswith("high"):
        return "High"
    if "some concerns" in x:
        return "Some concerns"
    return "Unclear"

# Combine sample size and dropouts for all intervention/control groups
def combine_sample_and_dropouts(x):
    if pd.isna(x):
        return pd.Series({"n_enrolled":np.nan,
                          "n_dropouts":np.nan})
    pairs=re.findall(r"(\d+)\s*\((\d+)\s*\)",str(x))
    if not pairs:
        return pd.Series({"n_enrolled":np.nan,
                          "n_dropouts":np.nan})
    enrolled=sum(int(p[0]) for p in pairs)
    dropouts=sum(int(p[1]) for p in pairs)
    return pd.Series({"n_enrolled":enrolled,
                      "n_dropouts":dropouts})


def clean_data(df):
    # remove whitespace from column names and each cell
    df.columns=[c.strip() for c in df.columns]
    df = df.map(strip_str)

    # select only required columns from evidence table
    df = df[columns_to_keep].copy()

    # convert year to numeric
    df["Year"]=pd.to_numeric(df["Year"], errors="coerce")

    # apply consistent levels in interventions, outcome and rob
    for col in interventions:
        df[col]=df[col].map(normalise_intervention)
    for col in outcomes:
        df[col]=df[col].map(normalise_outcome)
    df["Overall Risk of bias"]= df["Overall Risk of bias"].map(
        normalise_rob)

    df=pd.concat([df,df["Sample size (dropouts)"].apply(combine_sample_and_dropouts)],
                 axis=1)
    
    return df


#get dataframe from load_data.py
df = load_evidence_table()

#clean df
df = clean_data(df)

# Save cleaned data as CSV
output_path = "data/cleaned_evidence_table.csv"
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved to",output_path)
print("\nFirst 5 rows of cleaned dataset\n")
print(df.head())