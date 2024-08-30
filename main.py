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
    EDA.calculate_monthly_means(city, data)
    EDA.hourly_control_charts(city)
    EDA.hourly_box_plots(city)

    logging.info(f"Performing ANOVA tests for {city}")
    ANOVA.hourly_anova(city, data)
    ANOVA.fourYblocks_anova(city, data)
    ANOVA.elevenYblocks_anova(city, data)


if __name__ == "__main__":
    main()