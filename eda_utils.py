import logging
import os
import pandas as pd

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

    def calculate_monthly_means(city:str, data:pd.DataFrame, agg:str='hourly'):
        """
        Public class method that calculates the monthly means of the data and saves the data to monthly sheet in the excel file.

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
        logging.info(f"Calculating monthly {agg} means for {city}.")

        monthly_means = {}

        if agg == 'hourly':
            for month in range(1,13):
                for hour in range(24):
                    monthly_means[(month, hour)] = [data[(data['local_time'].dt.month == month) & (data['local_time'].dt.hour == hour)]['electricity'].mean() for year in range(1980, 2024)]
            
            monthly_means = pd.DataFrame(monthly_means, index=range(1980, 2024))

            month_to_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

            monthly_means.xs(1, level=0, axis=1).to_excel(f'transformed_data/{city}/monthly_{agg}_means.xlsx', sheet_name='January')
            for month in range(2, 13):
                # write to the same excel file
                with pd.ExcelWriter(f'transformed_data/{city}/monthly_{agg}_means.xlsx', engine='openpyxl', mode='a') as writer:
                    monthly_means.xs(month, level=0, axis=1).to_excel(writer, sheet_name=month_to_name[month])

            logging.info(f"Monthly {agg} means for {city} calculated and saved to transformed_data/{city}/monthly_{agg}_means.xlsx.")

        elif agg == 'daily':
            data['local_time'] = data['local_time'].dt.date
            data = data.groupby('local_time').sum()
            data.reset_index(inplace=True)
            data['local_time'] = pd.to_datetime(data['local_time'])

            for month in range(1,13):
                monthly_means[month] = [data[(data['local_time'].dt.year == year) & (data['local_time'].dt.month == month)]['electricity'].mean() for year in range(1980, 2024)]

            monthly_means = pd.DataFrame(monthly_means, index=range(1980, 2024))

            monthly_means.to_excel(f'transformed_data/{city}/monthly_{agg}_means.xlsx')

            logging.info(f"Monthly {agg} means for {city} calculated and saved to transformed_data/{city}/monthly_{agg}_means.xlsx.")

        else:
            logging.error(f"Aggregation level {agg} is not supported.")
            raise ValueError


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
            data = pd.read_excel(f'transformed_data/{city}/monthly_hourly_means.xlsx', sheet_name=sheet, index_col=0)
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
            data = pd.read_excel(f'transformed_data/{city}/monthly_hourly_means.xlsx', sheet_name=sheet, index_col=0)
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

    def daily_mean_plots(city:str):
        """
        Public class method that plots daily mean plots for the data and saves the plots to visualizations folder.

        Parameters
        ----------
        city : str
            The city name.

        Returns
        -------
        None
        """     
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns

        logging.info(f"Plotting daily mean plots for {city}.")

        monthly_means = pd.read_excel(f'transformed_data/{city}/monthly_daily_means.xlsx')

        month_to_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        for month in range(1, 13):
            name = month_to_name[month]
            plt.figure(figsize=(10, 6))
            plt.plot(monthly_means[month], label=name, color='blue', linestyle='-', linewidth=2, marker='o', markersize=6)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.xlabel('Year', fontsize=14, fontweight='bold')
            plt.ylabel('Electricity (kWh)', fontsize=14, fontweight='bold')
            plt.title(f'Average Daily Electricity Production in Jakarta [{name}]', fontsize=16, fontweight='bold')
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.ylim(0, 10000)
            plt.savefig(f'visualizations/{city}/daily_mean_plots/{month}.png')
            plt.close()

        logging.info(f"Daily mean plots for {city} plotted and saved to visualizations folder.")

    def yearly_plots(city:str, data:pd.DataFrame, agg:int = 1):
        """
        Public class method that plots hourly box plots for the data and saves the plots to visualizations folder.

        Parameters
        ----------
        city : str
            The city name.
        data : pd.DataFrame
            The data in a pandas DataFrame.
        agg : int
            The aggregation level of the data. Default is 1. Can be 1 , 4 or 5.

        Returns
        -------
        None
        """
        import matplotlib.pyplot as plt

        logging.info(f"Plotting yearly plots for {city} with {agg} yearly aggregation.")

        data['local_time'] = data['local_time'].dt.year
        data = data.groupby('local_time').sum()
        #data.reset_index(inplace=True)
        data = data.iloc[:-1,:]

        if agg == 1:
            data = data

        elif agg == 4:
            data_4Y = {}

            for i in range(1980, 2024, 4):
                data_4Y[f'{i}-{i+3}'] = data.loc[i:i+3, 'electricity'].mean()
            data_4Y = pd.Series(data_4Y)
            data = data_4Y

        elif agg == 5:
            data_5Y = {}

            for i in range(1984, 2024, 5):
                data_5Y[f'{i}-{i+4}'] = data.loc[i:i+4, 'electricity'].mean()
            data_5Y = pd.Series(data_5Y)
            data = data_5Y

        else:
            logging.error(f"Aggregation level {agg} is not supported.")
            raise ValueError

        # Create the plot with a larger figure size
        plt.figure(figsize=(20,10))

        # Plotting the data with customizations
        plt.plot(data['electricity'], color='blue', linestyle='-', linewidth=2, marker='o', markersize=6)

        # Adding grid lines
        plt.grid(True, linestyle='--', alpha=0.6)

        # Customizing the labels and title
        plt.xlabel('Year', fontsize=14, fontweight='bold')
        plt.ylabel('Electricity ($10^6$ kWh)', fontsize=14, fontweight='bold')
        plt.title(f'{agg} - Yearly Electricity Production in {city}', fontsize=16, fontweight='bold')

        # Adjusting the ticks
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        # Adding limit to the y-axis
        plt.ylim(0, 2500000)

        # Save the plot
        plt.savefig(f'visualizations/{city}/{agg}_yearly_plot.png')
        plt.close()

        logging.info(f"Yearly plot with {agg} yearly aggregation for {city} plotted and saved to visualizations folder.")