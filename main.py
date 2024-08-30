import pandas as pd
import numpy as np
import os
import logging

from utils import *
from eda_utils import *
from anova_utils import *
from ttest_utils import *

# print logging messages to the console
logging.basicConfig(level=logging.INFO)

def main():
    city = 'Brisbane'

    File_Map(city)

    data = CSVInputFetcher.fetch_aggregated_data(CSVInputFetcher.city_filename_prefix(city), [1980, 2023])

    data.drop(columns=['time'], inplace=True)
    data['local_time'] = pd.to_datetime(data['local_time'])

    logging.info(f"Performing EDA for {city}")

    # EDA.calculate_monthly_means(city, data, 'hourly')
    # EDA.hourly_control_charts(city)
    # EDA.hourly_box_plots(city)

    # EDA.calculate_monthly_means(city, data, 'daily')
    EDA.daily_mean_plots(city)

    # EDA.yearly_plots(city, data, 1)
    # EDA.yearly_plots(city, data, 4)
    # EDA.yearly_plots(city, data, 5)

    # logging.info(f"Performing ANOVA tests for {city}")
    # ANOVA.normal_anova(city, data, 'hourly')
    # ANOVA.fourYblocks_anova(city, data, 'hourly')
    # ANOVA.elevenYblocks_anova(city, data, 'hourly')

    # ANOVA.normal_anova(city, data, 'daily')
    # ANOVA.fourYblocks_anova(city, data, 'daily')
    # ANOVA.elevenYblocks_anova(city, data, 'daily')

    # logging.info(f"Performing t-tests for {city}")
    # TTest(city).ttest_results(data, 4)
    TTest(city).ttest_results(data, 11)


if __name__ == "__main__":
    main()