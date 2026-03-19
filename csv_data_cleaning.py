import pandas as pd
import logging

logging.basicConfig(
    filename='csv_data_cleaning.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

def handle_duplicates(df):
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    logging.info(f"Duplicates removed: {before - after} rows dropped. Rows remaining: {after}")
    return df

def handle_nulls(df):
    null_count = df.isnull().sum()
    nulls_found = null_count[null_count > 0]
    if len(nulls_found) > 0:
        logging.info(f"Null values found:\n{nulls_found}")
    else:
        logging.info("No null values found.")
    for col in df.columns:
        num = pd.api.types.is_numeric_dtype(df[col])
        txt = pd.api.types.is_string_dtype(df[col])
        if num == True:
            df[col] = df[col].fillna(df[col].mean())
        elif txt == True:
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            logging.warning(f"Column '{col}' skipped — unrecognized dtype")
    logging.info("Null values handled.")
    return df

def handle_outliers(df):
    total_outliers = 0
    for col in df.columns:
        num = pd.api.types.is_numeric_dtype(df[col])
        if num == True:
            Q1 = df[col].quantile(0.25)
            Q2 = round(df[col].median())
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - (1.5 * IQR)
            upper_bound = Q3 + (1.5 * IQR)
            outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
            count = outliers.sum()
            if count > 0:
                logging.info(f"Outliers in '{col}': {count} replaced with median ({Q2})")
                total_outliers += count
            df.loc[outliers, col] = Q2
    logging.info(f"Total outliers replaced: {total_outliers}")
    return df

def handle_inconsistency(df):
    for col in df.columns:
        txt = pd.api.types.is_string_dtype(df[col])
        if txt == True:
            unique_before = df[col].nunique()
            df[col] = df[col].str.title()
            unique_after = df[col].nunique()
            if unique_before != unique_after:
                logging.info(f"Inconsistency fixed in '{col}': {unique_before} variants to {unique_after}")
    return df

def clean_data(filepath):
    try:
        df = pd.read_csv(filepath)
        logging.info(f"File loaded: {filepath} | Shape: {df.shape}")
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return

    df = handle_duplicates(df)
    df = handle_nulls(df)
    df = handle_outliers(df)
    df = handle_inconsistency(df)

    df.to_csv('Final_Data.csv', index=False)
    logging.info("Cleaned data saved to Final_Data.csv")

clean_data(r'S:\Python\Python Scripts\DataChecker\data2.csv')