from pathlib import Path

import pandas as pd
import numpy as np

app_dir = Path(__file__).parent

pd.options.display.float_format = '${:,.0f}'.format

bs_all = pd.read_csv('data-raw/balance_sheet_model.csv')

# custom columns
bs_all['BS_Flag'] = np.where(bs_all['bs_flag']=='Assets', 'Assets', 'Liabilities & Equity')
bs_all['NS_BS_Flag'] = np.where(bs_all['ns_bs_flag']=='Assets', 'Assets', 'Liabilities & Equity')
bs_all['month_num_name'] = bs_all['month'].astype('str') + bs_all['month_name']

# select only relevant columns
# month is still needed for filtering
columns_to_show = ['year', 'quarter_name', 'month_name', 'month_num_name', 'BS_Flag', 'category', 'NS_BS_Flag', 'ns_category', 'account_name', 'std_amount_gbp', 'is_year_end', 'is_quarter_end']

bs_all= bs_all[columns_to_show]
date_filters = pd.read_csv('data-raw/date_filters.csv')

# sort date filters before using them in the checkboxes
date_filters = date_filters.sort_values(by=['year', 'quarter_name', 'month'], ascending=[False, True, True], ignore_index=True)

# initial filters
yr_filters = date_filters.year.drop_duplicates().sort_values(
    ascending=False, ignore_index=True
)

yr_initial_select = yr_filters[0]
