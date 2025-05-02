import pandas as pd

def load_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_json(uploaded_file)

def export_csv(df):
    return df.to_csv(index=False).encode('utf-8')
