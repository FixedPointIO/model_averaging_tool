
# Model Averaging Tool

## Overview

The Model Averaging Tool is a Python library designed to facilitate model averaging, data processing, and visualization for various analytical tasks. It includes functions for loading and preprocessing data, calculating weights and contributions, generating plots, and more.

## Features

- Load and preprocess data from CSV and JSON files.
- Calculate weights based on inverse NRMSE.
- Compute contributions, CPA, ROI, and pseudo R-squared metrics.
- Generate various plots for visualizing results.
- Configurable settings for data processing and plotting.

## Installation (Colab)

To install the library, clone the repository and install the required dependencies:

```bash
!pip install -q git+https://github.com/FixedPointIO/model_averaging_tool.git

```

#### Import the Library and Load Data

Import the necessary functions from the library and load your data:

```python
from model_averaging_tool import (
    load_json, read_csv, preprocess_data, filter_data_by_date,
    calculate_weights, compute_contributions, calculate_cpa, calculate_roi,
    plot_contributions, plot_roi, plot_cpa, plot_effect_vs_paid_media_spends,
    plot_depvar_vs_depvarhat, plot_trend_season_holiday
)

# Load and preprocess data
raw_data_path = 'data/raw_data.csv'
pareto_aggregated_path = 'data/pareto_aggregated.csv'
pareto_alldecomp_matrix_path = 'data/pareto_alldecomp_matrix.csv'
dictionary_url = 'https://github.com/FixedPointIO/utils/blob/main/Dictionary3.csv?raw=true'

raw_data, pareto_aggregated, pareto_alldecomp_matrix = preprocess_data(
    raw_data_path, pareto_aggregated_path, pareto_alldecomp_matrix_path, dictionary_url
)
```

#### Filter Data by Date

Filter the data based on a specified date range:

```python
date_column = 'DATE'
window_start = '2022-01-01'
window_end = '2022-12-31'
filtered_data = filter_data_by_date(raw_data, date_column, window_start, window_end)
```

#### Calculate Weights and Contributions

Calculate weights and contributions:

```python
# Calculate weights
weights_df = calculate_weights(pareto_aggregated)

# Compute contributions
decomp_table = pareto_aggregated[['rn', 'coef', 'xDecompAgg', 'weights']]
total_spend_df = raw_data[['rn', 'Total Spend']]
sample_size = len(filtered_data)
contributions_table = compute_contributions(decomp_table, total_spend_df, sample_size)
```

#### Calculate CPA and ROI

Calculate Cost per Acquisition (CPA) and Return on Investment (ROI):

```python
cpa_table = calculate_cpa(contributions_table)
roi_table = calculate_roi(contributions_table)
```

#### Generate Plots

Generate various plots to visualize the results:

```python
plot_contributions(contributions_table)
plot_roi(roi_table)
plot_cpa(cpa_table)
```

## Configuration

You can configure various settings in the `config.py` file:

```python
import os

# Base directory for data files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory for storing data files
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

# Directory for storing output files
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'output')

# Directory for storing example scripts
EXAMPLES_DIR = os.path.join(BASE_DIR, '..', 'examples')

# Directory for storing test files
TESTS_DIR = os.path.join(BASE_DIR, '..', 'tests')

# Configuration for logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# Example file paths for testing purposes (can be replaced with actual paths)
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw_data.csv')
PARETO_AGGREGATED_PATH = os.path.join(DATA_DIR, 'pareto_aggregated.csv')
PARETO_ALLDECOMP_MATRIX_PATH = os.path.join(DATA_DIR, 'pareto_alldecomp_matrix.csv')
DICTIONARY_URL = 'https://github.com/FixedPointIO/utils/blob/main/Dictionary3.csv?raw=true'

# Configuration for plotting
PLOT_CONFIG = {
    'image_format': 'png',
    'dpi': 300,
    'figsize': (12, 5),
    'color_palette': 'husl'
}

# Configuration for data processing
DATA_PROCESSING_CONFIG = {
    'date_format': '%d/%m/%Y/',
    'encoding': 'utf-8',
    'ci_multiplier': 1.96
}
```

## Example Jupyter Notebook

You can also create a Jupyter notebook in Google Colab to demonstrate the usage of the library. Here's an example of what the notebook might look like.

First, clone the repository and install the required dependencies:

```python
!git clone https://github.com/yourusername/model_averaging_tool.git
%cd model_averaging_tool
!pip install -r requirements.txt
```

## Import the Library and Load Data

Import the necessary functions from the library and load your data:

```python
from model_averaging_tool import (
    load_json, read_csv, preprocess_data, filter_data_by_date,
    calculate_weights, compute_contributions, calculate_cpa, calculate_roi,
    plot_contributions, plot_roi, plot_cpa, plot_effect_vs_paid_media_spends,
    plot_depvar_vs_depvarhat, plot_trend_season_holiday
)

# Load and preprocess data
raw_data_path = 'data/raw_data.csv'
pareto_aggregated_path = 'data/pareto_aggregated.csv'
pareto_alldecomp_matrix_path = 'data/pareto_alldecomp_matrix.csv'
dictionary_url = 'https://github.com/FixedPointIO/utils/blob/main/Dictionary3.csv?raw=true'

raw_data, pareto_aggregated, pareto_alldecomp_matrix = preprocess_data(
    raw_data_path, pareto_aggregated_path, pareto_alldecomp_matrix_path, dictionary_url
)
```

## Filter Data by Date

Filter the data based on a specified date range:

```python
date_column = 'DATE'
window_start = '2022-01-01'
window_end = '2022-12-31'
filtered_data = filter_data_by_date(raw_data, date_column, window_start, window_end)
```

## Calculate Weights and Contributions

Calculate weights and contributions:

```python
# Calculate weights
weights_df = calculate_weights(pareto_aggregated)

# Compute contributions
decomp_table = pareto_aggregated[['rn', 'coef', 'xDecompAgg', 'weights']]
total_spend_df = raw_data[['rn', 'Total Spend']]
sample_size = len(filtered_data)
contributions_table = compute_contributions(decomp_table, total_spend_df, sample_size)
```

## Calculate CPA and ROI

Calculate Cost per Acquisition (CPA) and Return on Investment (ROI):

```python
cpa_table = calculate_cpa(contributions_table)
roi_table = calculate_roi(contributions_table)
```

## Generate Plots

Generate various plots to visualize the results:

```python
plot_contributions(contributions_table)
plot_roi(roi_table)
plot_cpa(cpa_table)
```

## Conclusion

This notebook demonstrated how to use the Model Averaging Tool library for model averaging, data processing, and visualization. You can customize the configuration settings in the `config.py` file and explore additional functionalities provided by the library.


