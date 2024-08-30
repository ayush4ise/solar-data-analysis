import abc
import logging
import os
import pandas as pd

class InputFetcher(abc.ABC):
    """
    Abstract class that fetches data from no matter what format and returns a pandas DataFrame.
    """
    @abc.abstractmethod
    def fetch_data(path: str) -> pd.DataFrame:
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
    def fetch_data(path: str) -> pd.DataFrame:
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

    def city_filename_prefix(city: str) -> str:
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
            return "1980-2023 renewable energy data/ninja_pv_-27.4665_153.0260_"
        
        elif city == "Tokyo":
            return "1980-2023 renewable energy data/ninja_pv_35.2474_140.4001_"
        
        else:
            logging.error(f"City {city} is not supported.")
            raise ValueError
        
    def fetch_aggregated_data(path: str, year_range: list) -> pd.DataFrame:
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
        
        for year in range(year_range[0], year_range[1]+1):
            file_name = path + f"{year}.csv"
            if not os.path.exists(file_name):
                logging.error(f"File {file_name} does not exist.")
                raise FileNotFoundError

            data = pd.concat([data, pd.read_csv(file_name, header=3)], ignore_index=True)

        logging.info(f"Aggregated data fetched from {path} for years {year_range[0]} to {year_range[1]}.")

        return data
    

def File_Map(city:str):
    """
    This function creates the necessare folder structure for a given city, so that all the results can be saved in the correct folders.

    Parameters
    ----------
    city : str

    Returns
    -------
    None
    """
    # visualizations/
    # {city}/
    # daily_mean_plots/
    # box_plots/
    # sigma_plots/


    # transformed_data/
    # {city}/

    # results/
    # {city}/

    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')
    if not os.path.exists(f'visualizations/{city}'):
        os.makedirs(f'visualizations/{city}')
    if not os.path.exists(f'visualizations/{city}/daily_mean_plots'):
        os.makedirs(f'visualizations/{city}/daily_mean_plots')
    if not os.path.exists(f'visualizations/{city}/box_plots'):
        os.makedirs(f'visualizations/{city}/box_plots')
    if not os.path.exists(f'visualizations/{city}/sigma_plots'):
        os.makedirs(f'visualizations/{city}/sigma_plots')

    if not os.path.exists('transformed_data'):
        os.makedirs('transformed_data')
    if not os.path.exists(f'transformed_data/{city}'):
        os.makedirs(f'transformed_data/{city}')

    if not os.path.exists('results'):
        os.makedirs('results')
    if not os.path.exists(f'results/{city}'):
        os.makedirs(f'results/{city}')

    logging.info(f"Folder structure created for {city}.")