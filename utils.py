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
        file_name = os.path.join(path)
        if not os.path.exists(file_name):
            logging.error(f"File {file_name} does not exist.")
            raise FileNotFoundError
        
        data = pd.read_csv(file_name, header=3)

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
        data = pd.DataFrame()
        
        for year in range(year_range[0], year_range[1]):
            file_name = os.path.join(path, f"{year}.csv")
            if not os.path.exists(file_name):
                logging.error(f"File {file_name} does not exist.")
                raise FileNotFoundError

            data = pd.concat([data, pd.read_csv(file_name, header=3)], ignore_index=True)

        return data
    

class EDA():
    """
    Class that performs exploratory data analysis.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Constructor for the EDA class.

        Parameters
        ----------
        data : pd.DataFrame
            The data to be analyzed.
        """
        self.data = data

    def calculate_monthly_means