# model_averaging_tool/constants.py

# Date format for parsing dates
DATE_FORMAT = '%d/%m/%Y/'

# Image format for saving plots
IMAGE_FORMAT = 'png'

# Number of decimal places for rounding numbers
NDP = 2

# Length for separators in print statements
LENGTH = 100

# Options for handling variables in data processing
OPTION_KEEP = "keep"
OPTION_DROP = "drop"

# Default encoding for reading CSV files
DEFAULT_ENCODING = 'utf-8'

# Confidence interval multiplier (95% confidence interval)
CI_MULTIPLIER = 1.96

# Allowed values for Prophet-related parameters
PROPHET_VARS_OPTS = ["trend", "season", "monthly", "weekday", "holiday"]
PROPHET_SIGNS_OPTS = ["default", "positive", "negative"]

# Example URLs for sample data (can be replaced with actual URLs or paths)
EXAMPLE_PROPHET_URL = "https://github.com/FixedPointIO/utils/blob/main/holidays.csv?raw=true"
EXAMPLE_DICTIONARY_URL = "https://github.com/FixedPointIO/utils/blob/main/Dictionary3.csv?raw=true"

# Example configuration for plotting colors
PAID_MEDIA_COLOR = '#5778a4'
CONTEXT_VAR_COLOR = '#967662'
SEASONALITY_COLOR = '#d1615d'
BASE_COLOR = '#32a852'

# Example settings for displaying base variables in contributions share
SHOW_BASE_YES = "Yes"
SHOW_BASE_NO = "No"

# Example MinMaxScaler range for normalization
SCALER_RANGE = (0, 1)

# Example file paths for testing purposes (can be replaced with actual paths)
RAW_DATA_PATH = 'path/to/raw_data.csv'
PARETO_AGGREGATED_PATH = 'path/to/pareto_aggregated.csv'
PARETO_ALLDECOMP_MATRIX_PATH = 'path/to/pareto_alldecomp_matrix.csv'
DICTIONARY_URL = 'https://github.com/FixedPointIO/utils/blob/main/Dictionary3.csv?raw=true'

# Other constants can be added here as needed

# Example usage
if __name__ == "__main__":
    print(f"Date Format: {DATE_FORMAT}")
    print(f"Image Format: {IMAGE_FORMAT}")
    print(f"Number of Decimal Places: {NDP}")
    print(f"Separator Length: {LENGTH}")
    print(f"Option Keep: {OPTION_KEEP}")
    print(f"Option Drop: {OPTION_DROP}")
    print(f"Default Encoding: {DEFAULT_ENCODING}")
    print(f"Confidence Interval Multiplier: {CI_MULTIPLIER}")
    print(f"Prophet Variables Options: {PROPHET_VARS_OPTS}")
    print(f"Prophet Signs Options: {PROPHET_SIGNS_OPTS}")
    print(f"Example Prophet URL: {EXAMPLE_PROPHET_URL}")
    print(f"Example Dictionary URL: {EXAMPLE_DICTIONARY_URL}")
    print(f"Paid Media Color: {PAID_MEDIA_COLOR}")
    print(f"Context Variable Color: {CONTEXT_VAR_COLOR}")
    print(f"Seasonality Color: {SEASONALITY_COLOR}")
    print(f"Base Color: {BASE_COLOR}")
    print(f"Show Base Yes: {SHOW_BASE_YES}")
    print(f"Show Base No: {SHOW_BASE_NO}")
    print(f"Scaler Range: {SCALER_RANGE}")
    print(f"Raw Data Path: {RAW_DATA_PATH}")
    print(f"Pareto Aggregated Path: {PARETO_AGGREGATED_PATH}")
    print(f"Pareto AllDecomp Matrix Path: {PARETO_ALLDECOMP_MATRIX_PATH}")
    print(f"Dictionary URL: {DICTIONARY_URL}")