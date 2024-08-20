# model_averaging_tool/plotting.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from prettytable import PrettyTable
from matplotlib.ticker import AutoMinorLocator
import matplotlib.dates as mdates

def df_to_prettytable(df):
    """
    Convert a DataFrame to PrettyTable.
    
    Parameters:
    - df (DataFrame): Input data.
    
    Returns:
    - PrettyTable: Formatted table.
    """
    table = PrettyTable()
    table.field_names = df.columns.tolist()

    # Setting alignment for each column to right
    for field in table.field_names:
        table.align[field] = "r"

    for index, row in df.iterrows():
        # Rounding each value in the row to two decimal points
        formatted_row = ['{:.2f}'.format(val) if isinstance(val, float) else val for val in row]
        table.add_row(formatted_row)
    return table

def plot_contributions(contributions_share_table_mod, image_format='png'):
    """
    Plot the share of contributions.
    
    Parameters:
    - contributions_share_table_mod (DataFrame): Table with contributions share.
    - image_format (str): Format to save the image. Default is 'png'.
    
    Returns:
    - None: Displays and saves the plot.
    """
    # Check if DataFrame is not empty
    if not contributions_share_table_mod.empty:
        # If 'rn' is a column in the DataFrame, set it as index
        if 'rn' in contributions_share_table_mod.columns:
            contributions_share_table_mod.set_index('rn', inplace=True)

        # Calculate the error for error bars
        error_lower = abs(contributions_share_table_mod['wtd_avg_share'] - contributions_share_table_mod['ci95_lo_share'])
        error_upper = abs(contributions_share_table_mod['ci95_hi_share'] - contributions_share_table_mod['wtd_avg_share'])
        error = [error_lower, error_upper]

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 5))
        contributions_share_table_mod['wtd_avg_share'].plot(kind='barh', ax=ax, alpha=0.9, xerr=error, capsize=2)

        ax.set_title('Share of Contribution')
        ax.set_xlabel('Share Percentage (%)')
        ax.set_ylabel('Variables')

        plt.tight_layout()

        # Save the figure to a file
        image_name = f'share_contribution_graph.{image_format}'
        fig.savefig(image_name)

        # Display the plot
        plt.show()
    else:
        print("No data available for plotting.")

def plot_roi(roi_table, image_format='png'):
    """
    Plot Return on Investment (ROI).
    
    Parameters:
    - roi_table (DataFrame): Table with ROI metrics.
    - image_format (str): Format to save the image. Default is 'png'.
    
    Returns:
    - None: Displays and saves the plot.
    """
    if not roi_table.empty:
        # ROI Plot
        fig, ax = plt.subplots(figsize=(12, 5))
        error_roi_lower = abs(roi_table['roi_wtd_avg'] - roi_table['roi_ci95_lo'])
        error_roi_upper = abs(roi_table['roi_ci95_hi'] - roi_table['roi_wtd_avg'])
        error_roi = [error_roi_lower, error_roi_upper]

        roi_table.plot(x='rn', y='roi_wtd_avg', kind='barh', ax=ax, xerr=error_roi, capsize=4, label='ROI')
        ax.set_title('Return on Investment (ROI)')
        ax.set_ylabel('ROI')
        ax.set_xlabel('Variables')

        # Display the legend
        ax.legend()

        plt.tight_layout()
        plt.show()
        fig.savefig(f'ROI_graph.{image_format}')

def plot_cpa(cpa_table, image_format='png'):
    """
    Plot Cost per Acquisition (CPA).
    
    Parameters:
    - cpa_table (DataFrame): Table with CPA metrics.
    - image_format (str): Format to save the image. Default is 'png'.
    
    Returns:
    - None: Displays and saves the plot.
    """
    if not cpa_table.empty:
        # CPA Plot
        fig, ax = plt.subplots(figsize=(12, 5))
        error_cpa_lower = abs(cpa_table['cpa_wtd_avg'] - cpa_table['cpa_ci95_lo'])
        error_cpa_upper = abs(cpa_table['cpa_ci95_hi'] - cpa_table['cpa_wtd_avg'])
        error_cpa = [error_cpa_lower, error_cpa_upper]

        cpa_table.plot(x='rn', y='cpa_wtd_avg', kind='barh', ax=ax, xerr=error_cpa, capsize=4, label='CPA')
        ax.set_title('Cost per Acquisition (CPA)')
        ax.set_ylabel('Channels')
        ax.set_xlabel('CPA')

        # Display the legend
        ax.legend()

        plt.tight_layout()
        plt.show()
        fig.savefig(f'CPA_graph.{image_format}')


def plot_effect_vs_paid_media_spends(best_model_data, paid_media_spends, solID_min_nrmse, image_format='png'):
    """
    Plot Paid Media Spends vs Effect.
    
    Parameters:
    - best_model_data (DataFrame): Data for the best model.
    - paid_media_spends (list): List of paid media spend variables.
    - solID_min_nrmse (str): Solution ID with the minimum NRMSE.
    - image_format (str): Format to save the image. Default is 'png'.
    
    Returns:
    - None: Displays and saves the plot.
    """
    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(12, 5))

    # Create a list of colors for each media type
    colors = sns.color_palette('husl', len(paid_media_spends))

    # Filter only those channels that exist in best_model_data.columns
    channels_to_plot = [channel for channel in paid_media_spends if channel in best_model_data.columns]

    # Plotting the stacked line chart using `stackplot`
    ax1.stackplot(best_model_data['DS'],
                  *[best_model_data[channel] for channel in channels_to_plot],
                  labels=channels_to_plot, colors=colors, alpha=0.5)

    # Format x-axis to show date in MM-YYYY format every 3rd month
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax1.xaxis.set_minor_locator(AutoMinorLocator())

    # Rotate x-axis dates by 45 degrees
    plt.xticks(rotation=45)

    # Create a second y-axis
    ax2 = ax1.twinx()
    ax2.plot(best_model_data['DS'], best_model_data['DEP_VAR'], color='#002147', linewidth=2)

    # Set plot title and labels
    ax1.set_title('Paid Media Spends vs Effect')
    ax1.set_xlabel('Date')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
    ax1.set_ylabel('Paid Media Spends')
    ax2.set_ylabel('Dependent Variable')

    # Make the legend with smaller font and smaller box
    # Place the legend to the right of the plot
    ax1.legend(loc='center left', bbox_to_anchor=(1.1, 0.5), prop={'size': 8})

    # Adjust the space on the right side for the legend
    plt.subplots_adjust(right=0.75)

    # Save the figure to a file
    image_name = f'plot_effect_vs_paid_media_spends.{image_format}'
    fig.savefig(image_name, format=image_format, dpi=300)

    # Display the plot
    plt.show()

def plot_depvar_vs_depvarhat(best_model_data, dep_var_col, dep_var_hat_col, best_model_R2_percentage, best_model_NRMSE_percentage, image_format='png'):
    """
    Plot Dependent Variable vs Model Fitted Values over Time.
    
    Parameters:
    - best_model_data (DataFrame): Data for the best model.
    - dep_var_col (str): Column name for the dependent variable.
    - dep_var_hat_col (str): Column name for the predicted values.
    - best_model_R2_percentage (str): Best model R-squared percentage.
    - best_model_NRMSE_percentage (str): Best model NRMSE percentage.
    - image_format (str): Format to save the image. Default is 'png'.
    
    Returns:
    - None: Displays and saves the plot.
    """
    # Create a figure and axis with larger width
    fig, ax1 = plt.subplots(figsize=(12, 5))

    # Plot dep_var and depVarHat
    ax1.plot(best_model_data['DS'], best_model_data[dep_var_col], color='#5778a4', linewidth=2, label='Response variable')
    ax1.plot(best_model_data['DS'], best_model_data[dep_var_hat_col], color='#d1615d', label='Model fitted')

    # Format x-axis to show date in MM-YYYY format every 3rd month
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

    # Rotate x-axis dates by 45 degrees
    plt.xticks(rotation=45)

    # Set plot title and labels
    ax1.set_title('DepVar and DepVarHat over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Values')

    # Annotate the plot with the R2 and NRMSE values (you can adjust the coordinates to your liking)
    ax1.text(0.01, 0.98, f"Adjusted R²: {best_model_R2_percentage}", transform=ax1.transAxes, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.3', facecolor='#b8b0ac', edgecolor='black'))
    ax1.text(0.01, 0.92, f"NRMSE: {best_model_NRMSE_percentage}", transform=ax1.transAxes, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.3', facecolor='#b8b0ac', edgecolor='black'))

    # Adjust the space on the right side for the legend
    plt.subplots_adjust(right=0.75)

    # Make the legend with smaller font and smaller box
    # Place the legend to the right of the plot
    ax1.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 8})

    # Save the figure to a file
    image_name = f'plot_DepVar_vs_DepVarHat.{image_format}'
    fig.savefig(image_name, format=image_format, dpi=300)

    # Display the plot
    plt.tight_layout()
    plt.show()

def plot_trend_season_holiday(best_model_data, variables=['TREND', 'SEASON', 'HOLIDAY'], image_format='png'):
    """
    Plot trend, season, and holiday effects over time.
    
    Parameters:
    - best_model_data (DataFrame): Data for the best model.
    - variables (list): List of variables to plot. Default is ['TREND', 'SEASON', 'HOLIDAY'].
    - image_format (str): Format to save the image. Default is 'png'.
    
    Returns:
    - None: Displays and saves the plots.
    """
    from sklearn.preprocessing import MinMaxScaler

    # Create a MinMaxScaler object
    scaler = MinMaxScaler()

    # Create a figure with subplots, one for each variable
    fig, axs = plt.subplots(len(variables), figsize=(16, 10))

    # Loop over each subplot and each variable
    for ax, var in zip(axs, variables):
        # Normalize the variable to lie between 0 and 1
        best_model_data[var] = scaler.fit_transform(best_model_data[[var]])

        # Format x-axis to show date in MM-YYYY format every 3rd month
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

        # Rotate x-axis dates by 45 degrees
        ax.tick_params(axis='x', rotation=45)

        # Plot the normalized variable
        ax.plot(best_model_data['DS'], best_model_data[var], label=var)

        # Set plot title and labels
        ax.set_title(f'{var.capitalize()} over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Values')

        # Place the legend
        ax.legend()

    # Adjust the space between subplots
    plt.subplots_adjust(hspace=0.4)

    # Save the figure
    image_name = f'plot_normed_trend_season_holiday.{image_format}'
    fig.savefig(image_name, format=image_format, dpi=300)

    # Display the plot
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Sample data for testing purposes
    contributions_share_table_mod = pd.DataFrame({
        'rn': ['var1', 'var2', 'var3'],
        'wtd_avg_share': [30, 50, 20],
        'ci95_lo_share': [25, 45, 15],
        'ci95_hi_share': [35, 55, 25]
    })

    roi_table = pd.DataFrame({
        'rn': ['var1', 'var2', 'var3'],
        'roi_wtd_avg': [1.5, 2.0, 1.8],
        'roi_ci95_lo': [1.2, 1.7, 1.5],
        'roi_ci95_hi': [1.8, 2.3, 2.1]
    })

    cpa_table = pd.DataFrame({
        'rn': ['var1', 'var2', 'var3'],
        'cpa_wtd_avg': [200, 150, 180],
        'cpa_ci95_lo': [180, 130, 160],
        'cpa_ci95_hi': [220, 170, 200]
    })

    best_model_data = pd.DataFrame({
        'DS': pd.date_range(start='2022-01-01', periods=10, freq='M'),
        'DEP_VAR': np.random.rand(10),
        'DEPVARHAT': np.random.rand(10),
        'TREND': np.random.rand(10),
        'SEASON': np.random.rand(10),
        'HOLIDAY': np.random.rand(10),
        'var1': np.random.rand(10),
        'var2': np.random.rand(10),
        'var3': np.random.rand(10)
    })

    paid_media_spends = ['var1', 'var2', 'var3']
    solID_min_nrmse = 'sol1'
    best_model_R2_percentage = "85.00%"
    best_model_NRMSE_percentage = "15.00%"

    plot_contributions(contributions_share_table_mod)
    plot_roi(roi_table)
    plot_cpa(cpa_table)
    plot_effect_vs_paid_media_spends(best_model_data, paid_media_spends, solID_min_nrmse)
    plot_depvar_vs_depvarhat(best_model_data, 'DEP_VAR', 'DEPVARHAT', best_model_R2_percentage, best_model_NRMSE_percentage)
    plot_trend_season_holiday(best_model_data)
