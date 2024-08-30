import pandas as pd
import numpy as np
import logging

class TTest():
    """
    Class that performs a t-test on the data.
    """
    def __init__(self, city:str):
        """
        Constructor for the class.
        
        Parameters
        ----------
        city : str
            The city name.
        """
        self.city = city

    def onetailed_paired_ttest(data1, data2):
        """
        Perform a one-tailed paired t-test on the data.
        Null hypothesis: The mean of data1 is less than or equal to the mean of data2.
        Alternative hypothesis: The mean of data1 is greater than the mean of data2.

        Parameters
        ----------
        data1 : pd.Series
            The first data to perform the t-test on.
        data2 : pd.Series
            The second data to perform the t-test on.

        Returns
        -------
        float
            The t-statistic of the t-test.
        float
            The p-value of the t-test.
        """
        from scipy.stats import ttest_rel
        t_stat, p_value = ttest_rel(data1, data2, alternative='greater')
        return t_stat, p_value

    def ttest_results(self, data, agg:int):
        """
        Perform a t-test on the data and save the results to results folder.
        
        Parameters
        ----------
        data : pd.DataFrame
            The data to perform the t-test on.
        agg : int
            The yearly aggregation level of the data. Can be 4 or 11.
            
        Returns
        -------
        None
        """

        logging.info(f"Performing t-test on {self.city} data.")

        data['local_time'] = data['local_time'].dt.year
        data = data.groupby('local_time').sum()
        #data.reset_index(inplace=True)
        data = data.iloc[:-1,:] # remove 2024 data

        if agg == 4:
            data_4Y = {}

            for i in range(1980, 2024, 4):
                data_4Y[f'{i}-{i+3}'] = data.loc[i:i+3, 'electricity'].values.tolist()

            table_4Y = {
                'Block1': [],
                'Block2': [],
                'B1_mean': [],
                'B2_mean': [],
                'B2-B1': [],
                't_stat': [],
                'p_value': [],
                'Reject H0': []
            }

            for i in range(0, 10):
                block1 = data_4Y[f'{1980 + i * 4}-{1983 + i * 4}']
                block2 = data_4Y[f'{1984 + i * 4}-{1987 + i * 4}']
                t_stat, p_value = TTest.onetailed_paired_ttest(block1, block2)
                reject_H0 = p_value < 0.05
                table_4Y['Block1'].append(f'{1980 + i * 4}-{1983 + i * 4}')
                table_4Y['Block2'].append(f'{1984 + i * 4}-{1987 + i * 4}')
                table_4Y['B1_mean'].append(np.mean(block1))
                table_4Y['B2_mean'].append(np.mean(block2))
                table_4Y['B2-B1'].append(np.mean(block2) - np.mean(block1))
                table_4Y['t_stat'].append(t_stat)
                table_4Y['p_value'].append(p_value)
                table_4Y['Reject H0'].append(reject_H0)

            table_4Y = pd.DataFrame(table_4Y)

            table_4Y.to_excel(f'results/{self.city}/ttest_4Y.xlsx', index=False)
            logging.info(f"t-test results saved to results/{self.city}/ttest_4Y.xlsx.")

        elif agg == 11:
            data_11Y = {}

            for i in range(1980, 2024, 11):
                data_11Y[f'{i}-{i+10}'] = data.loc[i:i+10, 'electricity'].values.tolist()

            table_11Y = {
                'Block1': [],
                'Block2': [],
                'B1_mean': [],
                'B2_mean': [],
                'B2-B1': [],
                't_stat': [],
                'p_value': [],
                'Reject H0': []
            }

            for i in range(0, 2):
                block1 = data_11Y[f'{1980 + i * 11}-{1990 + i * 11}']
                block2 = data_11Y[f'{1991 + i * 11}-{2001 + i * 11}']
                t_stat, p_value = TTest.onetailed_paired_ttest(block1, block2)
                reject_H0 = p_value < 0.05
                table_11Y['Block1'].append(f'{1980 + i * 11}-{1990 + i * 11}')
                table_11Y['Block2'].append(f'{1991 + i * 11}-{2001 + i * 11}')
                table_11Y['B1_mean'].append(np.mean(block1))
                table_11Y['B2_mean'].append(np.mean(block2))
                table_11Y['B2-B1'].append(np.mean(block2) - np.mean(block1))
                table_11Y['t_stat'].append(t_stat)
                table_11Y['p_value'].append(p_value)
                table_11Y['Reject H0'].append(reject_H0)

            table_11Y = pd.DataFrame(table_11Y)

            table_11Y.to_excel(f'results/{self.city}/ttest_11Y.xlsx', index=False)
            logging.info(f"t-test results saved to results/{self.city}/ttest_11Y.xlsx.")

        else:
            logging.error(f"Aggregation level {agg} is not supported.")
            raise ValueError