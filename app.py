from shared import * 
from utils import *

from datetime import datetime
import time

from shiny import App, reactive, render, ui

# initial data
bs_initial = bs_all.loc[bs_all.year == yr_initial_select]

# format
# bs_pivot.style.format('${:,.0f}'.format)

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_checkbox(
            "chk_year_all",
            "Year",
        ),
        ui.input_checkbox_group(
            "chk_year",
            "",
            [yr for yr in yr_filters],
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
        ui.busy_indicators.use(),
        ui.output_data_frame("initial_balance_sheet"),
        ui.output_data_frame("update_balance_sheet"),
    ),
    title="Balance Sheet",
    fillable=True,
)

def server(input, output, session):
    @reactive.effect
    @reactive.event(input.chk_year)
    def update_chk_quarter():
        print(input.chk_year())
        year_selected = [int(y) for y in input.chk_year()]
        qtr_filters = date_filters.pipe(try_loc, 'year', year_selected
                        ).quarter_name.drop_duplicates()
        # note that the choices cannot be just the Series, otherwise the underlying value will be the indices
        ui.update_checkbox_group("chk_quarter", choices=[qtr for qtr in qtr_filters], selected=input.chk_quarter() if input.chk_quarter() else None)

    @reactive.effect
    @reactive.event(input.chk_year, input.chk_quarter)
    def update_chk_month():
        year_selected = [int(y) for y in input.chk_year()]
        month_filters = date_filters.pipe(try_loc, 'year', year_selected
                        ).pipe(try_loc, 'quarter_name', input.chk_quarter()
                        ).month_name.drop_duplicates()
        ui.update_checkbox_group("chk_month", choices=[mo for mo in month_filters], selected=input.chk_month() if input.chk_month() else None)

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
            )

        # insert the totals
        bs_initial_pivot.loc[("Liabilities & Equity Total", ""), :] = bs_initial_pivot.loc[
            "Liabilities & Equity"
        ].sum()
        bs_initial_pivot.loc[("Assets Total", ""), :] = bs_initial_pivot.loc[
            "Assets"
        ].sum()

        bs_initial_flat = bs_initial_pivot.reset_index().sort_values(by=['BS_Flag', 'category']).reset_index(drop=True)

        bs_initial_flat.columns = flatten_columns(bs_initial_flat)

        amount_cols = {
            k: v
            for k, v in enumerate(bs_initial_flat.columns)
            if v not in ("BS_Flag", "category")
        }

        # numbers converted to string to retain format
        for col in amount_cols.values():
            bs_initial_flat[str(col)] = bs_initial_flat[str(col)].map(
                "£ {:,.0f}".format
            )

        # use css to align the str-formatted numbers
        cols_to_align = list(amount_cols.keys())

        rows_to_highlight = acctg_rows_to_highlight(bs_initial_flat)

        return render.DataGrid(bs_initial_flat, styles=df_style(cols_to_align, rows_to_highlight))

    @output
    @render.data_frame
    @reactive.event(input.apply)
    def update_balance_sheet():
        # print(input.apply._value)
        # time.sleep(3) # test spinner
        yr_selected = [int(y) for y in input.chk_year()]
        qtr_selected = input.chk_quarter()
        mo_selected = input.chk_month()

        # note that in if-elif only one condition is run
        # it returns early as much as possible
        cols_to_pivot = []
        if yr_selected: cols_to_pivot.append('year')
        if qtr_selected: cols_to_pivot.append('quarter_name')
        if mo_selected: cols_to_pivot.append('month_num_name')

        # invalid combination of rows to pivot
        if (cols_to_pivot == []) or (cols_to_pivot == ['quarter_name', 'month_num_name']):
            ui.remove_ui("#initial_balance_sheet")
            return pd.DataFrame()

        # filter to the appropriate row only - equivalent of DAX
        if cols_to_pivot == ["year"]:
            bs_filtered = bs_all[bs_all.is_year_end == 1]
        elif cols_to_pivot == ["year", "quarter_name"]:
            bs_filtered = bs_all[bs_all.is_quarter_end == 1]
        else:
            bs_filtered = bs_all

        bs_update = bs_filtered.pipe(try_loc, "year", yr_selected
                    ).pipe(try_loc, "quarter_name", qtr_selected
                    ).pipe(try_loc, "month_name", mo_selected)

        # pd.pivot_table is different from df.pivot
        bs_pivot = bs_update.pipe(pivot_val, values=['std_amount_gbp'], index=['BS_Flag', 'category'],
                    columns=cols_to_pivot, aggfunc='sum'
                    )

        # insert the totals - note that Assets Totals instead of Total Assets to help with sorting
        # it is easier to add totals before flatting the pivot table
        bs_pivot.loc[("Liabilities & Equity Total", ""), :] = (
            bs_pivot.loc["Liabilities & Equity"].sum()
        )
        bs_pivot.loc[("Assets Total", ""), :] = bs_pivot.loc[
            "Assets"
        ].sum()

        bs_flat = (
            bs_pivot.reset_index()
            .sort_values(by=["BS_Flag", "category"])
            .reset_index(drop=True) # do not add the old index as new col
        )

        bs_flat.columns = flatten_columns(bs_flat)

        amount_cols = {
            k: v
            for k, v in enumerate(bs_flat.columns)
            if v not in ("BS_Flag", "category")
        }

        for col in amount_cols.values():
            bs_flat[str(col)] = bs_flat[str(col)].map("£ {:,.0f}".format)

        ui.remove_ui("#initial_balance_sheet")

        # use css to align the str-formatted numbers
        cols_to_align = list(amount_cols.keys())

        rows_to_highlight = acctg_rows_to_highlight(bs_flat)

        return render.DataGrid(
            bs_flat, styles=df_style(cols_to_align, rows_to_highlight)
        )

    @output
    @render.text
    @reactive.event(input.apply)
    def last_update():
        update_str = "Updated on " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return update_str

app = App(app_ui, server)
