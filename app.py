from shared import * 
from utils import *

from datetime import datetime

from shiny import App, reactive, render, ui

# initial data
bs_initial = bs_all.loc[bs_all.year == yr_initial_select]
is_updated = 0

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_checkbox_group(  
            "chk_year",  
            "Year",  
            {yr:yr for yr in yr_filters},
        ),
        ui.input_checkbox_group(  
            "chk_quarter",  
            "Quarter",  
            {},
        ),
        ui.input_checkbox_group(  
            "chk_month",  
            "Month",  
            {},
        ),
        ui.input_action_button("apply", "Apply"),
        ui.input_action_button("reset", "Reset"),
        open="always",
        width=200,
    ),
    ui.card(
        ui.card_header("As Adjusted"),
        ui.output_text("last_update"),
        ui.output_data_frame("initial_balance_sheet"),
        ui.output_data_frame("update_balance_sheet")
    ),
    title="Balance Sheet",
    fillable=True,
)

def server(input, output, session):
    @reactive.effect
    @reactive.event(input.chk_year)
    def update_chk_quarter():
        year_selected = [int(y) for y in input.chk_year()]
        qtr_filters = date_filters.pipe(try_loc, 'year', year_selected
                        ).quarter_name.drop_duplicates()
        ui.update_checkbox_group("chk_quarter", choices={qtr:qtr for qtr in qtr_filters})

    @reactive.effect
    @reactive.event(input.chk_year, input.chk_quarter)
    def update_chk_month():
        year_selected = [int(y) for y in input.chk_year()]
        month_filters = date_filters.pipe(try_loc, 'year', year_selected
                        ).pipe(try_loc, 'quarter_name', input.chk_quarter()
                        ).month_name.drop_duplicates()
        ui.update_checkbox_group("chk_month", choices={mo:mo for mo in month_filters})

    @reactive.effect
    @reactive.event(input.reset)
    def reset_filters():
        ui.update_checkbox_group("chk_year", selected=[])
        ui.update_checkbox_group("chk_quarter", selected=[])
        ui.update_checkbox_group("chk_month", selected=[])

    @output
    @render.data_frame
    def initial_balance_sheet():
        bs_initial_pivot = bs_initial.pipe(pivot_val, values=['std_amount_gbp'], index=['BS_Flag', 'category'],
            columns=['year', 'quarter_name', 'month_num_name'], aggfunc='sum'
            ).reset_index(drop=False)
        
        bs_initial_pivot.columns = [ '_'.join([str(c) for c in c_list if c not in ('', 'std_amount_gbp')]) for c_list in bs_initial_pivot.columns.values ]
        
        # return bs_initial_pivot
        return render.DataGrid(bs_initial_pivot)

    @output
    @render.data_frame
    @reactive.event(input.apply)
    def update_balance_sheet():
        # print(input.apply._value)
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

        ui.remove_ui("#initial_balance_sheet")
        return render.DataGrid(bs_pivot)
    
    @output
    @render.text
    @reactive.event(input.apply)
    def last_update():
        update_str = "Updated on " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return update_str
    
app = App(app_ui, server)