# model_averaging_tool/data_processing.py

import pandas as pd
import json

def load_json(file_path):
    """
    Load JSON data from a file.
    
    Parameters:
    - file_path (str): Path to the JSON file.
    
    Returns:
    - dict: Parsed JSON data.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def read_csv(file_path, encoding='utf-8'):
    """
    Read a CSV file into a DataFrame.
    
    Parameters:
    - file_path (str): Path to the CSV file.
    - encoding (str): Encoding to use for reading the file. Default is 'utf-8'.
    
    Returns:
    - DataFrame: Loaded data.
    """
    try:
        return pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        print(f"Error reading the file: {file_path}")
        return None

def preprocess_data(raw_data_path, pareto_aggregated_path, pareto_alldecomp_matrix_path, dictionary_url):
    """
    Preprocess data by reading raw data and renaming variables using a dictionary.
    
    Parameters:
    - raw_data_path (str): Path to the raw data CSV file.
    - pareto_aggregated_path (str): Path to the Pareto aggregated CSV file.
    - pareto_alldecomp_matrix_path (str): Path to the Pareto all decomposition matrix CSV file.
    - dictionary_url (str): URL to the dictionary CSV file.
    
    Returns:
    - tuple: Processed data (raw_data, pareto_aggregated, pareto_alldecomp_matrix).
    """
    # Try reading the files
    try:
        raw_data = pd.read_csv(raw_data_path)
        pareto_aggregated = pd.read_csv(pareto_aggregated_path)
        pareto_alldecomp_matrix = pd.read_csv(pareto_alldecomp_matrix_path)
    except UnicodeDecodeError as e:
        print(f"Error reading the file: {e}")
        return None, None, None

    # Load the dictionary
    dictionary = pd.read_csv(dictionary_url)
    variable_mapping = dictionary.set_index('variable')['mapping'].to_dict()

    # Rename variables in pareto_aggregated
    pareto_aggregated['rn'] = pareto_aggregated['rn'].replace("(Intercept)", "intercept")
    exceptions_agg = ["intercept", "holiday", "trend", "season"]
    pareto_aggregated['rn'] = pareto_aggregated['rn'].apply(lambda x: variable_mapping.get(x.lower(), x) if x.lower() not in exceptions_agg else x)

    # Rename variables in pareto_alldecomp_matrix
    exceptions_matrix = ["solID", "xDecompAgg", "depVarHat", "holiday", "trend", "season", "ds", "top_sol", "cluster", "intercept"]
    pareto_alldecomp_matrix.columns = [variable_mapping.get(col.lower(), col) if col.lower() not in exceptions_matrix else col for col in pareto_alldecomp_matrix.columns]

    # Convert column names of pareto_alldecomp_matrix to upper case
    pareto_alldecomp_matrix.columns = pareto_alldecomp_matrix.columns.str.upper()

    # Convert all column names in raw_data to upper case
    raw_data.columns = raw_data.columns.str.upper()

    # Convert all entries in the "rn" column of pareto_aggregated to upper case
    pareto_aggregated['rn'] = pareto_aggregated['rn'].str.upper()

    return raw_data, pareto_aggregated, pareto_alldecomp_matrix

def filter_data_by_date(data, date_column, window_start, window_end):
    """
    Filter data based on a date range.
    
    Parameters:
    - data (DataFrame): Input data.
    - date_column (str): Name of the date column.
    - window_start (str): Start date in 'YYYY-MM-DD' format.
    - window_end (str): End date in 'YYYY-MM-DD' format.
    
    Returns:
    - DataFrame: Filtered data.
    """
    # Convert to datetime format
    data[date_column] = pd.to_datetime(data[date_column])
    window_start = pd.to_datetime(window_start, format="%Y-%m-%d")
    window_end = pd.to_datetime(window_end, format="%Y-%m-%d")
    # Filter the data
    filtered_data = data[(data[date_column] >= window_start) & (data[date_column] <= window_end)]
    
    return filtered_data

def rename_columns_using_dictionary(data, dictionary_url):
    """
    Rename columns in a DataFrame using a dictionary from a CSV file.
    
    Parameters:
    - data (DataFrame): Input data.
    - dictionary_url (str): URL to the dictionary CSV file.
    
    Returns:
    - DataFrame: Data with renamed columns.
    """
    # Load the dictionary
    dictionary = pd.read_csv(dictionary_url)
    variable_mapping = dictionary.set_index('variable')['mapping'].to_dict()

    # Rename columns using the dictionary
    data.columns = [variable_mapping.get(col.lower(), col) for col in data.columns]
    
    return data

def calculate_sample_size(df):
    """
    Calculate the sample size of a DataFrame.
    
    Parameters:
    - df (DataFrame): Input data.
    
    Returns:
    - int: Sample size.
    """
    return len(df)

def determine_data_frequency(data, date_column):
    """
    Determine the frequency of the data based on the date column.
    
    Parameters:
    - data (DataFrame): Input data.
    - date_column (str): Name of the date column.
    
    Returns:
    - str: Data frequency ('W' for weekly, 'D' for daily, 'irregular' otherwise).
    """
    date_diff = data[date_column].diff().dt.days.dropna()
    
    if (date_diff == 7).all():
        return 'W'
    elif (date_diff == 1).all():
        return 'D'
    else:
        return 'irregular'

def check_missing_dates(data, date_column):
    """
    Check for missing dates in daily data.
    
    Parameters:
    - data (DataFrame): Input data.
    - date_column (str): Name of the date column.
    
    Returns:
    - list: List of missing dates.
    """
    date_diff = data[date_column].diff().dt.days.dropna()
    
    if (date_diff == 1).all():
        min_date = data[date_column].min()
        max_date = data[date_column].max()
        
        all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
        missing_dates = all_dates.difference(data[date_column])
        
        return missing_dates
    else:
        return []

# Example usage
if __name__ == "__main__":
    raw_data_path = 'path/to/raw_data.csv'
    pareto_aggregated_path = 'path/to/pareto_aggregated.csv'
    pareto_alldecomp_matrix_path = 'path/to/pareto_alldecomp_matrix.csv'
    dictionary_url = 'https://github.com/FixedPointIO/utils/blob/main/Dictionary3.csv?raw=true'
    
    raw_data, pareto_aggregated, pareto_alldecomp_matrix = preprocess_data(
        raw_data_path, pareto_aggregated_path, pareto_alldecomp_matrix_path, dictionary_url
    )
    
    date_column = 'DATE'
    window_start = '2022-01-01'
    window_end = '2022-12-31'
    
    filtered_data = filter_data_by_date(raw_data, date_column, window_start, window_end)
    print(filtered_data.head())