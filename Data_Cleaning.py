import pandas as pd
import numpy as np
import logging

logging.basicConfig(
    filename='data_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

def header_cleaner(df):
    before = df.columns.tolist()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    after = df.columns.tolist()
    logging.info(f"Headers before: {before}")
    logging.info(f"Headers after: {after}")
    return df

def duplicate_column_cleaner(df):
    before = df.shape[1]
    df = df.loc[:, ~df.columns.duplicated()]
    after = df.shape[1]
    logging.info(f"Duplicate columns removed: {before - after}. Columns remaining: {after}")
    return df

def symbol_cleaner(df):
    for col in df.columns:
        dollar_mask = df[col].astype(str).str.contains(r'[$%,]')
        if dollar_mask.any():
            cleaned = df[col].str.replace(r'[$%,]', '', regex=True)
            converted = pd.to_numeric(cleaned, errors='coerce')
            df[col] = converted
            logging.info(f"Symbols removed from column: '{col}'")
    return df

def datatype_fixing(df):
    logging.info(f"Dtypes before fixing:\n{df.dtypes}")
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]) == True:
            uniqueness = df[col].nunique() / len(df)
            if uniqueness > 0.9:
                continue
            check_num = pd.to_numeric(df[col], errors='coerce')
            converted = check_num.notna().sum() / len(df)
            if converted > 0.5:
                df[col] = check_num
                logging.info(f"Column '{col}' converted to numeric")
    return df

def duplicate_cleaner(df):
    before = len(df)
    if df.duplicated().any() == True:
        df = df.drop_duplicates()
    after = len(df)
    logging.info(f"Duplicates removed: {before - after} rows dropped. Rows remaining: {after}")
    return df

def null_cleaner(df):
    null_count = df.isnull().sum()
    nulls_found = null_count[null_count > 0]
    if len(nulls_found) > 0:
        logging.info(f"Null values found:\n{nulls_found}")
    else:
        logging.info("No null values found.")
    for col in df.columns.tolist():
        num = pd.api.types.is_numeric_dtype(df[col])
        txt = pd.api.types.is_string_dtype(df[col])
        if df[col].isnull().sum() / len(df) > 0.5:
            df = df.drop(columns=[col])
            logging.warning(f"Column '{col}' dropped - more than 50% values were null")
            continue
        elif num == True:
            df[col] = df[col].fillna(df[col].median())
        elif txt == True:
            uniqueness = df[col].nunique() / len(df)
            if uniqueness > 0.9:
                if df[col].isnull().any():
                    df = df.dropna(subset=[col])
                    logging.info(f"Rows with null '{col}' dropped - high cardinality column")
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].ffill()
        else:
            logging.warning(f"Column '{col}' skipped - unrecognized dtype")
    logging.info("Null values handled.")
    return df

def outlier_cleaner(df):
    total_outliers = 0
    for col in df.columns:
        num = pd.api.types.is_numeric_dtype(df[col])
        if num == True and not pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(float)
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - (1.5 * IQR)
            upper_bound = Q3 + (1.5 * IQR)
            outliers_low = df[col] < lower_bound
            outliers_high = df[col] > upper_bound
            count = outliers_low.sum() + outliers_high.sum()
            if count > 0:
                logging.info(f"Outliers in '{col}': {count} values winsorized")
                total_outliers += count
            df.loc[outliers_low, col] = lower_bound
            df.loc[outliers_high, col] = upper_bound
    logging.info(f"Total outliers handled: {total_outliers}")
    return df

def inconsistency_cleaner(df):
    for col in df.columns:
        txt = pd.api.types.is_string_dtype(df[col])
        if txt == True:
            uniqueness = df[col].nunique() / len(df)
            if uniqueness > 0.9:
                continue  # skip ID/name columns
            unique_before = df[col].nunique()
            df[col] = df[col].str.title()
            unique_after = df[col].nunique()
            if unique_before != unique_after:
                logging.info(f"Inconsistency fixed in '{col}': {unique_before} variants to {unique_after}")
    return df

def date_cleaner(df):
    for col in df.columns:
        date_keywords = ['date', 'time', 'timestamp']
        if any(keyword in col for keyword in date_keywords):
            if pd.api.types.is_string_dtype(df[col]):
                converted = pd.to_datetime(df[col], format='mixed', errors='coerce')
                if converted.notna().sum() / len(df) > 0.5:
                    df[col] = converted
                    logging.info(f"Column '{col}' converted to datetime")
    return df

def clean_data(filepath):
    try:
        df = pd.read_csv(filepath)
        logging.info(f"File loaded: {filepath} | Shape: {df.shape}")
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return

    df = header_cleaner(df)
    df = duplicate_column_cleaner(df)
    df = symbol_cleaner(df)
    df = datatype_fixing(df)
    df = date_cleaner(df)
    df = duplicate_cleaner(df)
    df = null_cleaner(df)
    df = outlier_cleaner(df)
    df = inconsistency_cleaner(df)

    df.to_csv('Final_Data.csv', index=False)
    logging.info("Cleaned data saved to Final_Data.csv")
    print("Done. Check data_cleaning.log for details.")

clean_data(r'S:\Python\Python Scripts\DataCleaner\Data_Cleaning_Adv\sample_datasets\marketing_campaign_data_messy.csv')