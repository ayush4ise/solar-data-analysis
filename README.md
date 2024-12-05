# Solar Data Analysis 🌞

This repository contains a Python script (`main.py`) for analyzing solar energy data from 1980 to 2023. The script performs Exploratory Data Analysis (EDA), ANOVA, and t-tests to investigate seasonal trends, outliers, and variations in solar energy generation across three cities: Jakarta, Tokyo, and Brisbane.

## Project Details
The analysis was supervised by Professor S. Viswanathan, focusing on evaluating the seasonal trends and significant differences in solar energy generation. Statistical methods, including ANOVA and t-tests, were applied to understand the variations in energy production across different years, months, and hours.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ayush4ise/solar-data-analysis.git
    ```

2. Navigate to the project directory:
    ```bash
    cd solar-data-analysis
    ```

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the analysis, execute the `main.py` script:

```bash
python main.py
```

This will perform the following actions for the selected city (default is Tokyo):
- Load and preprocess data
- Conduct EDA, including monthly means, hourly control charts, and box plots
- Perform ANOVA and t-tests to identify statistical differences in solar power generation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Data sourced from solar energy datasets for Jakarta, Tokyo, and Brisbane.