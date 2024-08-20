# model_averaging_tool/analysis.py

import pandas as pd
import numpy as np

def calculate_weights(pareto_aggregated):
    """
    Calculate weights based on the inverse of NRMSE.
    
    Parameters:
    - pareto_aggregated (DataFrame): Input data containing 'solID', 'rsq_train', and 'nrmse'.
    
    Returns:
    - DataFrame: Data with calculated weights.
    """
    # Extract necessary columns and drop duplicate rows
    pareto_unique = pareto_aggregated[['solID', 'rsq_train', 'nrmse']].drop_duplicates()
    
    # Calculate 'inverse_nrmse'
    pareto_unique['inverse_nrmse'] = 1 / pareto_unique['nrmse']
    
    # Calculate 'weights'
    pareto_unique['weights'] = pareto_unique['inverse_nrmse'] / pareto_unique['inverse_nrmse'].sum()
    
    return pareto_unique

def compute_contributions(decomp_table, total_spend_df, sample_size):
    """
    Compute weighted average, standard deviation, and confidence intervals for decomposed effects.
    
    Parameters:
    - decomp_table (DataFrame): Decomposed effects data.
    - total_spend_df (DataFrame): Total spend data.
    - sample_size (int): Sample size of the data.
    
    Returns:
    - DataFrame: Table with computed contributions and confidence intervals.
    """
    # Calculate weighted average and weighted standard deviation for 'coef'
    df_coef = decomp_table.groupby('rn').apply(lambda x: pd.Series({
        'wtd_avg': np.average(x['coef'], weights=x['weights']),
        'wtd_stddev': np.sqrt(np.average((x['coef'] - np.average(x['coef'], weights=x['weights']))**2, weights=x['weights']))
    })).sort_index()
    
    # Calculate weighted average and weighted standard deviation for 'xDecompAgg'
    df_xDecompAgg = decomp_table.groupby('rn').apply(lambda x: pd.Series({
        'wtd_avg': np.average(x['xDecompAgg'], weights=x['weights']),
        'wtd_stddev': np.sqrt(np.average((x['xDecompAgg'] - np.average(x['xDecompAgg'], weights=x['weights']))**2, weights=x['weights']))
    })).sort_index()
    
    # Calculate the 95% confidence interval for the weighted average
    df_xDecompAgg['ci95_lo'] = df_xDecompAgg['wtd_avg'] - (1.96 * df_xDecompAgg['wtd_stddev'] / np.sqrt(sample_size))
    df_xDecompAgg['ci95_hi'] = df_xDecompAgg['wtd_avg'] + (1.96 * df_xDecompAgg['wtd_stddev'] / np.sqrt(sample_size))
    
    # Merge with spend totals
    decompplusspend_table = pd.merge(df_xDecompAgg, total_spend_df, on='rn', how='left')
    
    # Replace NaN in 'Total Spend' with 0
    decompplusspend_table['Total Spend'].fillna(0, inplace=True)
    
    return decompplusspend_table

def calculate_cpa(decompplusspend_table):
    """
    Calculate Cost per Acquisition (CPA) metrics for paid media spends.
    
    Parameters:
    - decompplusspend_table (DataFrame): Table with decomposed effects and spend data.
    
    Returns:
    - DataFrame: Table with CPA metrics.
    """
    decompplusspend_table['cpa_wtd_avg'] = decompplusspend_table['Total Spend'] / decompplusspend_table['wtd_avg']
    decompplusspend_table['cpa_ci95_lo'] = decompplusspend_table['Total Spend'] / decompplusspend_table['ci95_lo']
    decompplusspend_table['cpa_ci95_hi'] = decompplusspend_table['Total Spend'] / decompplusspend_table['ci95_hi']
    
    # Filter out rows where 'Total Spend' is zero
    cpa_table = decompplusspend_table[decompplusspend_table['Total Spend'] > 0]
    
    return cpa_table

def calculate_roi(decompplusspend_table):
    """
    Calculate Return on Investment (ROI) metrics for paid media spends.
    
    Parameters:
    - decompplusspend_table (DataFrame): Table with     decomposed effects and spend data.
    
    Returns:
    - DataFrame: Table with ROI metrics.
    """
    decompplusspend_table['roi_wtd_avg'] = decompplusspend_table['wtd_avg'] / decompplusspend_table['Total Spend']
    decompplusspend_table['roi_ci95_lo'] = decompplusspend_table['ci95_lo'] / decompplusspend_table['Total Spend']
    decompplusspend_table['roi_ci95_hi'] = decompplusspend_table['ci95_hi'] / decompplusspend_table['Total Spend']
    
    # Filter out rows where 'Total Spend' is zero
    roi_table = decompplusspend_table[decompplusspend_table['Total Spend'] > 0]
    
    return roi_table

def calculate_contributions(decompplusspend_table):
    """
    Calculate contributions share for each variable.
    
    Parameters:
    - decompplusspend_table (DataFrame): Table with decomposed effects and spend data.
    
    Returns:
    - DataFrame: Table with contributions share.
    """
    # Calculate totals for weighted average, ci95_lo, and ci95_hi
    total_wtd_avg = decompplusspend_table['wtd_avg'].sum()
    total_ci95_lo = decompplusspend_table['ci95_lo'].sum()
    total_ci95_hi = decompplusspend_table['ci95_hi'].sum()
    
    # Calculate the share of each variable
    decompplusspend_table['wtd_avg_share'] = (decompplusspend_table['wtd_avg'] / total_wtd_avg) * 100
    decompplusspend_table['ci95_lo_share'] = (decompplusspend_table['ci95_lo'] / total_ci95_lo) * 100
    decompplusspend_table['ci95_hi_share'] = (decompplusspend_table['ci95_hi'] / total_ci95_hi) * 100
    
    # Create a new table for contributions share
    contributions_share_table = decompplusspend_table[['rn', 'wtd_avg_share', 'ci95_lo_share', 'ci95_hi_share']]
    
    return contributions_share_table

def calculate_pseudo_r_squared(data, dep_var_col, dep_var_hat_col, sample_size, num_hyperparameters, num_betas):
    """
    Calculate pseudo R-squared and adjusted pseudo R-squared for model averaging.
    
    Parameters:
    - data (DataFrame): Input data containing actual and predicted values.
    - dep_var_col (str): Column name for the dependent variable.
    - dep_var_hat_col (str): Column name for the predicted values.
    - sample_size (int): Sample size of the data.
    - num_hyperparameters (int): Number of hyperparameters in the model.
    - num_betas (int): Number of beta coefficients in the model.
    
    Returns:
    - tuple: Pseudo R-squared and adjusted pseudo R-squared.
    """
    data['avg_dep_var'] = data[dep_var_col].mean()
    
    # Calculate sum of squared residuals (SSR) and total sum of squares (TSS)
    data['ssr'] = (data[dep_var_col] - data[dep_var_hat_col]).pow(2)
    data['tss'] = (data[dep_var_col] - data['avg_dep_var']).pow(2)
    
    pseudo_r_sqd = 1 - (data['ssr'].sum() / data['tss'].sum())
    
    degrees_of_freedom_pseudo = sample_size - num_hyperparameters - num_betas
    pseudo_r_sqd_adj = 1 - (((1 - pseudo_r_sqd) * (sample_size - 1)) / degrees_of_freedom_pseudo)
    
    return pseudo_r_sqd, pseudo_r_sqd_adj

# Example usage
if __name__ == "__main__":
    # Sample data for testing purposes
    pareto_aggregated_path = 'path/to/pareto_aggregated.csv'
    pareto_aggregated = pd.read_csv(pareto_aggregated_path)
    
    weights_df = calculate_weights(pareto_aggregated)
    print(weights_df.head())
    
    # Assuming decomp_table and total_spend_df are defined elsewhere
    decomp_table = pd.DataFrame({
        'rn': ['var1', 'var2', 'var3'],
        'coef': [0.5, 0.3, 0.2],
        'xDecompAgg': [0.4, 0.3, 0.3],
        'weights': [0.5, 0.3, 0.2]
    })
    
    total_spend_df = pd.DataFrame({
        'rn': ['var1', 'var2', 'var3'],
        'Total Spend': [1000, 2000, 1500]
    })
    
    sample_size = 100
    
    decompplusspend_table = compute_contributions(decomp_table, total_spend_df, sample_size)
    print(decompplusspend_table.head())
    
    cpa_table = calculate_cpa(decompplusspend_table)
    print(cpa_table.head())
    
    roi_table = calculate_roi(decompplusspend_table)
    print(roi_table.head())
    
    contributions_share_table = calculate_contributions(decompplusspend_table)
    print(contributions_share_table.head())
    
    # Assuming data, dep_var_col, dep_var_hat_col, num_hyperparameters, and num_betas are defined elsewhere
    data = pd.DataFrame({
        'DEP_VAR': np.random.rand(sample_size),
        'DEPVARHAT': np.random.rand(sample_size)
    })
    
    num_hyperparameters = 5
    num_betas = 10
    
    pseudo_r_sqd, pseudo_r_sqd_adj = calculate_pseudo_r_squared(data, 'DEP_VAR', 'DEPVARHAT', sample_size, num_hyperparameters, num_betas)
    print(f"Pseudo R-squared: {pseudo_r_sqd}")
    print(f"Adjusted Pseudo R-squared: {pseudo_r_sqd_adj}")