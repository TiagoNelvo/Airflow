import pandas as pd


AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

def le_arquivo():
    df = pd.read_csv(f"{AIRFLOW_HOME}/data/arquivo.csv", header=None)
    return df
    
def mascara_senha(df):
    df[2] = '********'
    return df

def salva_arquivo(df):
    df.to_csv(f"{AIRFLOW_HOME}/data/arquivo_final.csv", index=False)







