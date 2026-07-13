import re
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from load_data import load_evidence_table


# Select columns to retain from the evidence table

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
    "Neoadjuvant chemotherapy adherence"
]                            

# Interventions and Outcome categories

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

# DATA CLEANING FUCTIONS

# Remove white space, multiple spaces and new lines on any string

def strip_str(x):
    if isinstance(x,str):
        return re.sub(r"\s+"," ",x.strip())
    return x

# Standardise intervention labels to 'Yes'/'No'/'Not reported'

def normalise_intervention(x):
    if pd.isna(x):
        return "Not reported"
    x=str(x).strip().lower()
    if x.startswith("yes"):
        return "Yes"
    if x.startswith("no") and "not" not in x:
        return "No"
    return "Not reported"

# Standardise outcome labels to 'Improved'/'No effect'/'Not reported'

def normalise_outcome(x):
    if pd.isna(x):
        return "Not reported"
    x=str(x).strip().lower()
    if x.startswith("improv"):
        return "Improved"
    if x.startswith("no effect"):
        return "No effect"
    return "Not reported"

# Extract sample size and dropouts 

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

# Convert intervention duration to weeks

def duration_to_weeks(x):
    if pd.isna(x):
        return np.nan

    x = str(x).lower().strip()
    numbers = re.findall(r"\d+\.?\d*", x)
    if not numbers:
        return np.nan

    # If it the value is a range like 3-6 weeks, use the midpoint
    if len(numbers) >= 2 and "-" in x:
        value = (float(numbers[0]) + float(numbers[1])) / 2
    else:
        value = float(numbers[0])

    # Convert days to weeks
    if "day" in x:
        return round(value / 7, 1)

    # Keep weeks as weeks
    if "week" in x:
        return round(value, 1)

    return np.nan

# DATA CLEANING PIPELINE

def clean_data(df):
    # Remove whitespace from column names and each cell
    df.columns=[c.strip() for c in df.columns]
    df = df.map(strip_str)

    # Select only required columns 
    df = df[columns_to_keep].copy()

    # Convert year to numeric
    df["Year"]=pd.to_numeric(df["Year"], errors="coerce")

    # Apply consistent levels in interventions and outcome 
    for col in interventions:
        df[col]=df[col].map(normalise_intervention)
    for col in outcomes:
        df[col]=df[col].map(normalise_outcome)

    df=pd.concat([df,df["Sample size (dropouts)"].apply(combine_sample_and_dropouts)],
                 axis=1)
    df["Duration_weeks"] = df["Duration of Intervention"].map(duration_to_weeks)
    
    return df


# LOAD DATA
df = load_evidence_table()

# CLEAN DATA
df = clean_data(df)

# EXPORT CLEANED DATA AS CSV
output_path = "data/cleaned_evidence_table.csv"
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved to",output_path)
print("\nFirst 5 rows of cleaned dataset\n")
print(df.head())