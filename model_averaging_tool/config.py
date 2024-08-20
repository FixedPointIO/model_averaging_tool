# model_averaging_tool/config.py

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

# Example usage
if __name__ == "__main__":
    print(f"Base Directory: {BASE_DIR}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Examples Directory: {EXAMPLES_DIR}")
    print(f"Tests Directory: {TESTS_DIR}")
    print(f"Raw Data Path: {RAW_DATA_PATH}")
    print(f"Pareto Aggregated Path: {PARETO_AGGREGATED_PATH}")
    print(f"Pareto AllDecomp Matrix Path: {PARETO_ALLDECOMP_MATRIX_PATH}")
    print(f"Dictionary URL: {DICTIONARY_URL}")
    print(f"Plot Config: {PLOT_CONFIG}")
    print(f"Data Processing Config: {DATA_PROCESSING_CONFIG}")