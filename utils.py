import abc
import logging
import os
import pandas as pd

class InputFetcher(abc.ABC):
    """
    Abstract class that fetches data from no matter what format and returns a pandas DataFrame.
    """
    @abc.abstractmethod
    def fetch_data(self, path: str) -> pd.DataFrame:
        """
        Method that should exist in all instantiations that will fetch the data from the input path.

        Returnss
        -------
        pd.DataFrame
            The data in a pandas DataFrame
        """
        raise NotImplementedError

class CSVInputFetcher(InputFetcher):
    """
    Fetcher for CSV formatted input wher the first 3 rows are metadata
    """
    def fetch_data(self, path: str) -> pd.DataFrame:
        """
        Public class method that fetches the data from the csv file from the input path.

        Parameters
        ----------
        path : str
            The path to the csv file.

        Returns
        -------
        pd.DataFrame
            The data in a pandas DataFrame
        """
        logging.info(f"Fetching data from {path}.")

        file_name = os.path.join(path)
        if not os.path.exists(file_name):
            logging.error(f"File {file_name} does not exist.")
            raise FileNotFoundError
        
        data = pd.read_csv(file_name, header=3)

        logging.info(f"Data fetched from {path}.")
        return data

    def city_filename_prefix(self, city: str) -> str:
        """
        Public class method that returns the prefix of the filename of the csv file for the city.

        Parameters
        ----------
        city : str
            The city name.

        Returns
        -------
        str
            The prefix of the filename of the csv file for the city.
        """
        if city == "Jakarta":
            return "1980-2023 renewable energy data/ninja_pv_-7.2623_112.7361_"
            
        elif city == "Brisbane":
            return "1980-2023 renewable energy data/ninja_pv_-27.4665_153.0260_1986.csv"
        
        elif city == "Tokyo":
            return "1980-2023 renewable energy data/ninja_pv_35.2474_140.4001_"
        
        else:
            logging.error(f"City {city} is not supported.")
            raise ValueError
        
    def fetch_aggregated_data(self, path: str, year_range: list) -> pd.DataFrame:
        """
        Public class method that fetches the data from multiple csv files from the input path and aggregates them into one DataFrame.

        Parameters
        ----------
        path : str
            The path to the csv files.
        year_range : list
            The range of years to fetch the data from.

        Returns
        -------
        pd.DataFrame
            The data in a pandas DataFrame
        """
        logging.info(f"Fetching aggregated data from {path} for years {year_range[0]} to {year_range[1]}.")

        data = pd.DataFrame()
        
        for year in range(year_range[0], year_range[1]):
            file_name = os.path.join(path, f"{year}.csv")
            if not os.path.exists(file_name):
                logging.error(f"File {file_name} does not exist.")
                raise FileNotFoundError

            data = pd.concat([data, pd.read_csv(file_name, header=3)], ignore_index=True)

        logging.info(f"Aggregated data fetched from {path} for years {year_range[0]} to {year_range[1]}.")

        return data
    

class EDA():
    """
    Class that performs exploratory data analysis.
    """

    def __init__(self, city:str):
        """
        Constructor for the EDA class.

        Parameters
        ----------
        city : str
            The city name.
        """
        self.city = city

    def calculate_monthly_means(city:str):
        """
        Public class method that calculates the monthly means of the data and saves the data to monthly sheet in the excel file.

        Parameters
        ----------
        city : str
            The city name.

        Returns
        -------
        None
        """
        logging.info(f"Calculating monthly means for {city}.")

        data = CSVInputFetcher().fetch_aggregated_data(CSVInputFetcher().city_filename_prefix(city), [1980, 2023])

        data.drop(columns=['time'], inplace=True)
        data['local_time'] = pd.to_datetime(data['local_time'])

        monthly_means = {}

        for month in range(1,13):
            for hour in range(24):
                monthly_means[(month, hour)] = [data[(data['local_time'].dt.year == year) & (data['local_time'].dt.month == month) & (data['local_time'].dt.hour == hour)]['electricity'].mean() for year in range(1981, 2024)]

        monthly_means = pd.DataFrame(monthly_means, index=range(1980, 2024))

        month_to_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        monthly_means.xs(1, level=0, axis=1).to_excel(f'transformed_data/{city}/monthly_means.xlsx', sheet_name='January')
        for month in range(2, 13):
            # write to the same excel file
            with pd.ExcelWriter(f'transformed_data/{city}/monthly_means.xlsx', engine='openpyxl', mode='a') as writer:
                monthly_means.xs(month, level=0, axis=1).to_excel(writer, sheet_name=month_to_name[month])

        logging.info(f"Monthly means for {city} calculated and saved to transformed_data/{city}/monthly_means.xlsx.")


    def hourly_control_charts(city:str):
        """
        Public class method that plots hourly control charts for the data and saves the plots to visualizations folder.

        Parameters
        ----------
        city : str
            The city name.

        Returns
        -------
        None
        """

        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np

        logging.info(f"Plotting hourly control charts for {city}.")

        def make_sigma_plot(data, col, month):
            # Calculate mean and standard deviation
            mean = data[col].mean()
            std = data[col].std()

            # Set Seaborn style
            sns.set(style="whitegrid")
            plt.figure(figsize=(14, 8))

            # Plot the data
            plt.plot(data[col], color='blue', lw=1.5, label='Data')

            # Plot mean line
            plt.axhline(mean, color='red', linestyle='--', linewidth=2, label='Mean')
            
            # Plot upper and lower control limits (UCL and LCL)
            plt.axhline(mean + 3*std, color='green', linestyle='--', linewidth=2, label='+3σ Limit')
            plt.axhline(mean - 3*std, color='green', linestyle='--', linewidth=2, label='-3σ Limit')

            # Highlight and annotate outliers
            outliers = data[col][(data[col] > mean + 3*std) | (data[col] < mean - 3*std)]
            plt.scatter(outliers.index, outliers, color='red', zorder=5, s=50, marker='o')

            # Annotate outliers
            for i, value in outliers.items():
                plt.text(i, value, f'{i}', fontsize=9, ha='right', va='bottom', color='red', rotation=45)

            # Set titles and labels with increased font size
            plt.title(f'{col}th Hour Control Chart', fontsize=16, fontweight='bold')
            plt.xlabel('Year', fontsize=14)
            plt.ylabel('Electricity (in kW)', fontsize=14)

            # Add legend
            plt.legend(loc='upper left', fontsize=12)

            # Save the figure
            plt.tight_layout()
            plt.savefig(f'visualizations/{city}/sigma_plots/{month}_{col}th_hour.png')
            plt.close()

        sheet_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        for sheet in sheet_names:
            data = pd.read_excel(f'transformed_data/{city}/monthly_means.xlsx', sheet_name=sheet, index_col=0)
            for col in data.columns:
                make_sigma_plot(data, col, sheet)        

        logging.info(f"Hourly control charts for {city} plotted and saved to visualizations/sigma_plots.")


    def hourly_box_plots(city:str):
        """
        Public class method that plots hourly box plots for the data and saves the plots to visualizations folder.

        Parameters
        ----------
        city : str
            The city name.

        Returns
        -------
        None
        """
        import matplotlib.pyplot as plt
        import seaborn as sns

        logging.info(f"Plotting hourly box plots for {city}.")

        sheet_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        for sheet in sheet_names:
            data = pd.read_excel(f'transformed_data/{city}/monthly_means.xlsx', sheet_name=sheet, index_col=0)
            plt.figure(figsize=(14, 8))
            sns.boxplot(data=data, palette='Set3')
            plt.title(f'Hourly Box Plots for {sheet}', fontsize=16, fontweight='bold')
            plt.xlabel('Hour', fontsize=14)
            plt.ylabel('Electricity (in kW)', fontsize=14)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'visualizations/{city}/box_plots/{sheet}_box_plot.png')
            plt.close

        logging.info(f"Hourly box plots for {city} plotted and saved to visualizations/box_plots.")

