import pandas as pd
import numpy as np
import os
import logging

from utils import *

def main():
    city = 'Brisbane'

    data = CSVInputFetcher.fetch_aggregated_data(CSVInputFetcher.city_filename_prefix(city), [1980, 2023])

    data.drop(columns=['time'], inplace=True)
    data['local_time'] = pd.to_datetime(data['local_time'])

    logging.info(f"Performing EDA for {city}")

    EDA.calculate_monthly_means(city, data, 'hourly')
    EDA.hourly_control_charts(city)
    EDA.hourly_box_plots(city)

    EDA.calculate_monthly_means(city, data, 'daily')
    EDA.daily_mean_plots(city)

    logging.info(f"Performing ANOVA tests for {city}")
    ANOVA.normal_anova(city, data, 'hourly')
    ANOVA.fourYblocks_anova(city, data, 'hourly')
    ANOVA.elevenYblocks_anova(city, data, 'hourly')

    ANOVA.normal_anova(city, data, 'daily')
    ANOVA.fourYblocks_anova(city, data, 'daily')
    ANOVA.elevenYblocks_anova(city, data, 'daily')


if __name__ == "__main__":
    main()