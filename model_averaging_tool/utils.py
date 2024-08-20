# model_averaging_tool/utils.py

import numpy as np
import pandas as pd

def check_nas(df):
    """
    Check for missing (NA) values in the DataFrame.
    
    Parameters:
    - df (DataFrame): Input data.
    
    Returns:
    - None: Prints out columns with missing values and their percentages.
    """
    name = getattr(df, 'name', 'DataFrame')
    na_vals = df.isna().sum()
    na_vals = na_vals[na_vals > 0]  # Filter for variables with missing values greater than zero
    
    if len(na_vals) > 0:
        na_vals_percentage = ((na_vals / len(df)) * 100).round(2)  # Round off to two decimal places
        strs = [f"{var} ({missing} | {missingness}%)"
                for var, missing, missingness in zip(na_vals.index, na_vals, na_vals_percentage)]
        print(f"Dataset {name} contains missing (NA) values. "
              f"These values must be removed or fixed for proper functioning.\n  Missing values: "
              f"{', '.join(strs)}")
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    have_inf = df[numeric_columns].apply(lambda x: np.isinf(x).sum())
    
    if any(have_inf > 0):
        print(f"Dataset {name} contains Inf values. "
              f"These values must be removed or fixed for proper functioning.\n  Check: "
              f"{', '.join(have_inf[have_inf > 0].index)}")

def check_novar(dt_input):
    """
    Check for columns with no variance in the DataFrame.
    
    Parameters:
    - dt_input (DataFrame): Input data.
    
    Returns:
    - None: Prints out columns with no variance.
    """
    novar = dt_input.loc[:, dt_input.apply(lambda x: x.nunique() == 1)].columns
    if len(novar) > 0:
        msg = f"There are {len(novar)} column(s) with no-variance: {', '.join(novar)}. \nConsider removing the variable(s) to proceed..."
        print(msg)

def check_daterange(date_min, date_max, dates):
    """
    Check if the provided date range is within the dataset's date range.
    
    Parameters:
    - date_min (str): Minimum date in 'YYYY-MM-DD' format.
    - date_max (str): Maximum date in 'YYYY-MM-DD' format.
    - dates (Series): Series of dates from the dataset.
    
    Returns:
    - None: Prints warnings if the provided date range is outside the dataset's date range.
    """
    if date_min is not None:
        date_min = pd.to_datetime(date_min)
        if date_min < min(dates):
            print(f"Parameter 'date_min' not in your data's date range. Changed to '{min(dates)}'")
    
    if date_max is not None:
        date_max = pd.to_datetime(date_max)
        if date_max > max(dates):
            print(f"Parameter 'date_max' not in your data's date range. Changed to '{max(dates)}'")

def check_depvar(dt_input, dep_var, dep_var_type):
    """
    Check the validity of the dependent variable.
    
    Parameters:
    - dt_input (DataFrame): Input data.
    - dep_var (str): Name of the dependent variable.
    - dep_var_type (str): Type of the dependent variable ('conversion' or 'revenue').
    
    Returns:
    - None: Prints warnings if the dependent variable is invalid.
    """
    if dep_var is None or len(dep_var) > 1 or dep_var not in dt_input.columns:
        print("You must provide only 1 correct dependent variable name for 'dep_var'")
    
    if not np.issubdtype(dt_input[dep_var].dtype, np.number):
        print("'dep_var' must be a numeric or integer variable")
    
    if dep_var_type is None or len(dep_var_type) != 1 or dep_var_type not in ["conversion", "revenue"]:
        print("'dep_var_type' must be 'conversion' or 'revenue'")

def check_prophet(dt_holidays, prophet_vars, prophet_signs, date_diff):
    """
    Check the validity of Prophet-related parameters.
    
    Parameters:
    - dt_holidays (DataFrame): Holidays data.
    - prophet_vars (list): List of Prophet variables.
    - prophet_signs (list): List of signs for Prophet variables.
    - date_diff (Series): Series of date differences to determine data granularity.
    
    Returns:
    - None: Prints warnings if Prophet-related parameters are invalid.
    """
    OPTS_PDN = ["default", "positive", "negative"]  # Allowed values for 'prophet_signs'
    
    if dt_holidays is None or prophet_vars is None:
        return None
    else:
        prophet_vars = [var.lower() for var in prophet_vars]
        opts = ["trend", "season", "monthly", "weekday", "holiday"]
        
        if not all(var in opts for var in prophet_vars):
            print(f"Allowed values for 'prophet_vars' are: {', '.join(opts)}")
        
        if "weekday" in prophet_vars and date_diff.max() > 7:
            print("Ignoring prophet_vars = 'weekday' input given your data granularity")
        
        if prophet_signs is None:
            prophet_signs = ["default"] * len(prophet_vars)
        
        if not all(sign in OPTS_PDN for sign in prophet_signs):
            print(f"Allowed values for 'prophet_signs' are: {', '.join(OPTS_PDN)}")
        
        if len(prophet_signs) != len(prophet_vars):
            print("'prophet_signs' must have same length as 'prophet_vars'")

def get_sample_size(df):
    """
    Get the sample size of a DataFrame.
    
    Parameters:
    - df (DataFrame): Input data.
    
 Returns:
    - int: Sample size of the DataFrame.
    """
    return len(df)

def identify_date_column(data):
    """
    Identify the date column in the DataFrame irrespective of case.
    
    Parameters:
    - data (DataFrame): Input data.
    
    Returns:
    - str: Name of the date column.
    """
    for column in data.columns:
        if column.lower() == 'date':
            return column
    raise ValueError("No date column found.")

# Example usage
if __name__ == "__main__":
    # Sample data for testing purposes
    sample_data = pd.DataFrame({
        'date': pd.date_range(start='2022-01-01', periods=10, freq='D'),
        'value': np.random.rand(10),
        'constant': [1] * 10
    })
    
    check_nas(sample_data)
    check_novar(sample_data)
    check_daterange('2022-01-01', '2022-12-31', sample_data['date'])
    dep_var = 'value'
    dep_var_type = 'revenue'
    check_depvar(sample_data, dep_var, dep_var_type)
    
    # Assuming dt_holidays and prophet_vars are defined elsewhere
    dt_holidays = pd.DataFrame({'holiday': ['New Year', 'Christmas'], 'date': ['2022-01-01', '2022-12-25']})
    prophet_vars = ['trend', 'season']
    prophet_signs = ['positive', 'negative']
    date_diff = sample_data['date'].diff().dt.days.dropna()
    check_prophet(dt_holidays, prophet_vars, prophet_signs, date_diff)