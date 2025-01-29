import pandas as pd

def preprocess(df, region_df):
    # Filtering for summer Olympics
    df = df[df['Season'] == 'Summer']
    # Merging with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # Dropping duplicates
    df.drop_duplicates(inplace=True)
    # One-hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df
