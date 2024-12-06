from shared import * 
from utils import *

from datetime import datetime
# from shiny import App, render, ui
from shiny.express import input, render, ui

# initial data
bs_initial = bs_all.loc[bs_all.year == yr_initial_select
                ]
bs_initial = bs_initial.pipe(pivot_val, values=['std_amount_gbp'], index=['BS_Flag', 'category'],
                columns=['year', 'quarter_name', 'month_num_name'], aggfunc='sum'
                ).reset_index(drop=False)

with ui.sidebar(open="desktop"):

    ui.input_checkbox_group(  
        "chk_year",  
        "Year",  
        {yr:yr for yr in yr_filters},
    )  
    ui.input_checkbox_group(  
        "chk_quarter",  
        "Quarter",  
        {qtr:qtr for qtr in qtr_filters},
    )  
    ui.input_checkbox_group(  
        "chk_month",  
        "Month",  
        {mo:mo for mo in month_filters},
    )

@render.data_frame
def update_balance_sheet():

    year_selected = [int(y) for y in input.chk_year()]
    
    bs_update = bs_all.pipe(try_loc, "year", year_selected
                ).pipe(try_loc, "quarter_name", input.chk_quarter()
                ).pipe(try_loc, "month_name", input.chk_month())
                # ).pipe(sort_val, by=['year', 'quarter_name', 'month_num_name'], ascending=[False, True, True])

    # pd.pivot_table is different from df.pivot
    bs_pivot = bs_update.pipe(pivot_val, values=['std_amount_gbp'], index=['BS_Flag', 'category'],
                columns=['year', 'quarter_name', 'month_num_name'], aggfunc='sum'
                ).reset_index(drop=False)

    bs_pivot.columns = [ '_'.join([str(c) for c in c_list if c not in ('', 'std_amount_gbp')]) for c_list in bs_pivot.columns.values ]

    update_str = "Updated on " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    return bs_pivot