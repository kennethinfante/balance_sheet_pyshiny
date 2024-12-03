from shared import app_dir, bs_all, yr_filters, yr_initial_select, \
    qtr_filters, month_filters, bs_initial
from utils import *

from datetime import datetime
# from shiny import App, render, ui
from shiny.express import input, render, ui

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
    bs_update = bs_all.pipe(try_loc, "year", input.chk_year()
                ).pipe(try_loc, "quarter_name", input.chk_quarter()
                ).pipe(try_loc, "month_name", input.chk_month()
                ).pipe(sort_val, by=['year', 'quarter_name', 'month'])

    # pd.pivot_table is different from df.pivot
    bs_pivot = bs_update.pipe(pivot_val, values=['std_amount_gbp'], index=['BS_Flag', 'category'],
                columns=['year', 'quarter_name', 'month_name'], aggfunc='sum'
                ).reset_index(drop=False)

    print(bs_pivot.columns)
    bs_pivot.columns = [ '_'.join([str(c) for c in c_list if c not in ('', 'std_amount_gbp')]) for c_list in bs_pivot.columns.values ]
    update_str = "Updated on " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    return bs_pivot