# Data Files

This folder contains the study-level data used to support the systematic review, *Optimal Delivery of Multimodal Prehabilitation for Adults Undergoing Major Cancer Surgery*.

All data were extracted from published studies included in the review. No individual participant data are included.

## Files

| File | Description |
|---|---|
| `Evidence_Table.xlsx` | The main evidence table containing extracted study characteristics, intervention components, programme duration, comparator details, adherence information and reported outcomes. |
| `cleaned_evidence_table.csv` | A cleaned, analysis-ready version of the evidence table used by the Python scripts to generate the review visualisations. |
| `risk_of_bias_rob2.xlsx` | The completed Cochrane Risk of Bias 2 (RoB 2) assessment for the primary outcome of each included study. |

## Data Processing

The `Evidence_Table.xlsx` file was used as the source dataset for the review analyses. It was cleaned and prepared using the Python scripts in the /scripts folder, producing `cleaned_evidence_table.csv`.

The cleaned CSV file was used to create the evidence maps and other summary visualisations included in the /figures folder.

## Risk-of-Bias Data

Risk of bias was assessed using the Cochrane RoB 2 tool.  
Each study was assigned an overall judgement of low risk of bias, some concerns, or high risk of bias. The `risk_of_bias_rob2.xlsx` file can be uploaded to the ROBVIS online visualisation tool to reproduce the RoB 2 traffic-light figure.


