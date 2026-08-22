## Analysis Scripts

Scripts used for data cleaning, analysis and visualisations. 

- `load_data.py`  
  Loads the extracted Evidence_Table data into Python for analysis and visualisation.  

- `clean_data.py`  
  Cleans and standardises the dataset, including intervention characteristics and outcome-reporting categories, so that the data can be analysed consistently.  

- `evidence_map.py`  
  Creates the evidence map summarising the distribution of included studies according to their intervention components and reported outcomes.  

- `evidence_map_bubble_chart.py`  
  Produces a bubble-chart version of the evidence map, allowing the number of studies within each intervention–outcome category to be displayed visually.  

- `visualisations.py`  
  Generates the remaining summary figures used in the review, including visualisations of intervention duration, intervention frequency, outcome effects, sample size and dropout patterns.  

## Workflow:

The scripts should generally be run in the following order:

1. Load the extracted data using `load_data.py`.
2. Clean and prepare the dataset using `clean_data.py`.
3. Generate the evidence maps using `evidence_map.py` and `evidence_map_bubble_chart.py`.
4. Generate the remaining figures using `visualisations.py`.

Figures are saved in the /figures folder.
