from pathlib import Path

import pandas as pd
import numpy as np

app_dir = Path(__file__).parent

bs_all = pd.read_csv('data-raw/balance_sheet_model.csv')

# select only relevant columns
columns_to_show = ['year', 'quarter_name', 'month_name', 'month', 'bs_flag', 'category', 'ns_bs_flag', 'ns_category', 'account_name', 'std_amount_gbp']

bs_all= bs_all[columns_to_show]
date_filters = pd.read_csv('data-raw/date_filters.csv')

bs_all['BS_Flag'] = np.where(bs_all['bs_flag']=='Assets', 'Assets', 'Liabilities and Equity')
bs_all['NS_BS_Flag'] = np.where(bs_all['ns_bs_flag']=='Assets', 'Assets', 'Liabilities and Equity')

# initial filters
yr_filters = date_filters.year.drop_duplicates().sort_values(ascending=False, ignore_index=True)

yr_initial_select = yr_filters[0]

qtr_filters = date_filters.quarter_name.drop_duplicates().sort_values(ascending=False, ignore_index=True)
month_filters = date_filters.month_name.drop_duplicates()

bs_initial = bs_all.loc[bs_all.year == yr_initial_select]
bs_initial = pd.pivot_table(bs_initial, values=['std_amount_gbp'], index=['BS_Flag', 'category'],
                columns=['year', 'quarter_name', 'month_name'], aggfunc='sum'
                ).reset_index(drop=False)
