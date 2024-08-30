import logging
import os
import pandas as pd

class ANOVA():
    """
    Class that performs ANOVA analysis.
    """

    def __init__(self, city:str):
        """
        Constructor for the ANOVA class.

        Parameters
        ----------
        city : str
            The city name.
        """
        self.city = city

    def normal_anova(city:str, data:pd.DataFrame, agg:str='hourly'):
        """
        Public class method that performs ANOVA analysis on the data to check if the means of the data are different for different years
        and saves the results to results folder.

        Parameters
        ----------
        city : str
            The city name.
        data : pd.DataFrame
            The data in a pandas DataFrame.
        agg : str
            The aggregation level of the data. Default is 'hourly'. Can be 'daily' or 'hourly'.

        Returns
        -------
        None
        """
        from scipy.stats import f_oneway

        data = data.copy()

        logging.info(f"Performing ANOVA for {agg} data for {city}.")

        data_anova = {}

        if agg == 'hourly':
            for month in range(1, 13):
                data_anova[month] = []
                for hour in range(24):
                    data_list = [list(data[(data['local_time'].dt.year == year) & (data['local_time'].dt.month == month) & (data['local_time'].dt.hour == hour)]['electricity']) for year in range(1980, 2024)]
                    f, p = f_oneway(*data_list)
                    data_anova[month].append([f, p])

            data_anova = pd.DataFrame(data_anova, index=range(24))

            # store f-values in one sheet and p-values in another
            f_values = data_anova.applymap(lambda x: x[0])
            p_values = data_anova.applymap(lambda x: x[1])

            f_values.to_excel(f'results/{city}/{agg}_anova.xlsx', sheet_name='F-Values')

            with pd.ExcelWriter(f'results/{city}/{agg}_anova.xlsx', engine='openpyxl', mode='a') as writer:
                p_values.to_excel(writer, sheet_name='P-Values')

            logging.info(f"ANOVA for {agg} data for {city} performed and results saved to results/{city}/{agg}_anova.xlsx.")

        elif agg == 'daily':
            data['local_time'] = data['local_time'].dt.date
            data = data.groupby('local_time').sum()
            data.reset_index(inplace=True)
            data['local_time'] = pd.to_datetime(data['local_time'])

            for month in range(1, 13):
                data_list = [list(data[(data['local_time'].dt.year == year) & (data['local_time'].dt.month == month)]['electricity']) for year in range(1980, 2024)]
                f, p = f_oneway(*data_list)
                data_anova[month] = {'f': f, 'p': p}

            pd.DataFrame(data_anova).to_excel(f'results/{city}/{agg}_anova.xlsx')

            logging.info(f"ANOVA for {agg} data for {city} performed and results saved to results/{city}/{agg}_anova.xlsx.")
            
        else:
            logging.error(f"Aggregation level {agg} is not supported.")
            raise ValueError


    def fourYblocks_anova(city:str, data:pd.DataFrame, agg:str='hourly'):
        """
        Public class method that performs ANOVA analysis on the data to check if the means of the data (for a given 4-year block) are different for different years
        and saves the results to results folder.

        Parameters
        ----------
        city : str
            The city name.
        data : pd.DataFrame
            The data in a pandas DataFrame.
        agg : str
            The aggregation level of the data. Default is 'hourly'. Can be 'daily' or 'hourly'.

        Returns
        -------
        None
        """
        from scipy.stats import f_oneway

        logging.info(f"Performing ANOVA for 4-year blocks for {city} for {agg} data.")

        data = data.copy()

        data_anova = {}

        if agg == 'hourly':
            for month in range(1, 13):
                data_anova[month] = []
                for hour in range(24):
                    data_list = [list(data[(data['local_time'].dt.year == year) & (data['local_time'].dt.month == month) & (data['local_time'].dt.hour == hour)]['electricity']) for year in range(1980, 2024)]
                    # make further 4 year groups in the data
                    # each year element is already in a list, so make a big list with the 4 year data
                    data_list = [data_list[i]+data_list[i+1]+data_list[i+2]+data_list[i+3] for i in range(0, len(data_list), 4)]

                    f, p = f_oneway(*data_list)
                    data_anova[month].append([f, p])

            data_anova = pd.DataFrame(data_anova, index=range(24))

            # store f-values in one sheet and p-values in another
            f_values = data_anova.applymap(lambda x: x[0])
            p_values = data_anova.applymap(lambda x: x[1])

            f_values.to_excel(f'results/{city}/4Yblocks_{agg}_anova.xlsx', sheet_name='F-Values')
                            
            with pd.ExcelWriter(f'results/{city}/4Yblocks_{agg}_anova.xlsx', engine='openpyxl', mode='a') as writer:
                p_values.to_excel(writer, sheet_name='P-Values')

            logging.info(f"ANOVA ({agg}) for 4-year blocks for {city} performed and results saved to results folder.")

        elif agg == 'daily':
            data['local_time'] = data['local_time'].dt.date
            data = data.groupby('local_time').sum()
            data.reset_index(inplace=True)
            data['local_time'] = pd.to_datetime(data['local_time'])

            data_anova = {}

            for month in range(1, 13):
                data_list = [list(data[(data['local_time'].dt.year == year) & (data['local_time'].dt.month == month)]['electricity']) for year in range(1980, 2024)]
                # make further 4 year groups in the data
                # each year element is already in a list, so make a big list with the 4 year data
                data_list = [data_list[i]+data_list[i+1]+data_list[i+2]+data_list[i+3] for i in range(0, len(data_list), 4)]

                f, p = f_oneway(*data_list)
                data_anova[month] = {'f': f, 'p': p}

            pd.DataFrame(data_anova).to_excel(f'results/{city}/4Yblocks_{agg}_anova.xlsx')

            logging.info(f"ANOVA ({agg}) for 4-year blocks for {city} performed and results saved to results folder.")

        else:
            logging.error(f"Aggregation level {agg} is not supported.")
            raise ValueError


    def elevenYblocks_anova(city:str, data:pd.DataFrame, agg:str='hourly'):
        """
        Public class method that performs ANOVA analysis on the data to check if the means of the data (for a given 11-year block) are different for different years
        and saves the results to results folder.

        Parameters
        ----------
        city : str
            The city name.
        data : pd.DataFrame
            The data in a pandas DataFrame.
        agg : str
            The aggregation level of the data. Default is 'hourly'. Can be 'daily' or 'hourly'.

        Returns
        -------
        None
        """
        from scipy.stats import f_oneway

        logging.info(f"Performing ANOVA for 11-year blocks for {city} for {agg} data.")

        data = data.copy()

        data_anova = {}

        if agg == 'hourly':
            for month in range(1, 13):
                data_anova[month] = []
                for hour in range(24):
                    data_list = [list(data[(data['local_time'].dt.year == year) & (data['local_time'].dt.month == month) & (data['local_time'].dt.hour == hour)]['electricity']) for year in range(1980, 2024)]
                    # make further 11 year groups in the data
                    # each year element is already in a list, so make a big list with the 11 year data
                    data_list = [data_list[i]+data_list[i+1]+data_list[i+2]+data_list[i+3]+data_list[i+4]+data_list[i+5]+data_list[i+6]+data_list[i+7]+data_list[i+8]+data_list[i+9]+data_list[i+10] for i in range(0, len(data_list), 11)]

                    f, p = f_oneway(*data_list)
                    data_anova[month].append([f, p])

            data_anova = pd.DataFrame(data_anova, index=range(24))

            # store f-values in one sheet and p-values in another
            f_values = data_anova.applymap(lambda x: x[0])
            p_values = data_anova.applymap(lambda x: x[1])

            f_values.to_excel(f'results/{city}/11Yblocks_{agg}_anova.xlsx', sheet_name='F-Values')
                            
            with pd.ExcelWriter(f'results/{city}/11Yblocks_{agg}_anova.xlsx', engine='openpyxl', mode='a') as writer:
                p_values.to_excel(writer, sheet_name='P-Values')

            logging.info(f"ANOVA ({agg}) for 11-year blocks for {city} performed and results saved to results/{city}/11Yblocks_anova.xlsx.")

        elif agg == 'daily':
            data['local_time'] = data['local_time'].dt.date
            data = data.groupby('local_time').sum()
            data.reset_index(inplace=True)
            data['local_time'] = pd.to_datetime(data['local_time'])

            data_anova = {}

            for month in range(1, 13):
                data_list = [list(data[(data['local_time'].dt.year == year) & (data['local_time'].dt.month == month)]['electricity']) for year in range(1980, 2024)]
                # make further 11 year groups in the data
                # each year element is already in a list, so make a big list with the 11 year data
                data_list = [data_list[i]+data_list[i+1]+data_list[i+2]+data_list[i+3]+data_list[i+4]+data_list[i+5]+data_list[i+6]+data_list[i+7]+data_list[i+8]+data_list[i+9]+data_list[i+10] for i in range(0, len(data_list), 11)]

                f, p = f_oneway(*data_list)
                data_anova[month] = {'f': f, 'p': p}

            pd.DataFrame(data_anova).to_excel(f'results/{city}/11Yblocks_{agg}_anova.xlsx')

            logging.info(f"ANOVA ({agg}) for 11-year blocks for {city} performed and results saved to results/{city}/11Yblocks_anova.xlsx.")

        else:
            logging.error(f"Aggregation level {agg} is not supported.")
            raise ValueError