import pandas as pd 

def load_evidence_table():
    df= pd.read_excel("data/Evidence_Table.xlsx")

    print("\nNumber of rows:", df.shape[0])
    print("Number of columns:", df.shape[1])

    #column names
    print("\nColumn names:", df.columns.tolist())

    #missing values
    print("\nMissing values:\n", df.isnull().sum())

    #view data
    print("\nFirst 5 rows:")
    print(df.head())

    return df 

if __name__=="__main__":
    load_evidence_table()