import pandas as pd

# helper functions
def try_loc(df, column, values_to_search:list):
    if values_to_search:
        return df.loc[df[column].isin(values_to_search)]
    else:
        return df

def sort_val(df, by:list, ascending:list):
    return df.sort_values(by=by, ascending=ascending)

# new function because df.pivot does not have the aggfunc
def pivot_val(df, values:list, index:list, columns:list, aggfunc:str, margins:bool=False):
    try:
        return pd.pivot_table(df, values, index, columns, aggfunc, margins)
    except Exception as error:
        print('Error producing pivot table: ' + repr(error))


def df_style(col_index:list, row_index:list):
    return [
        {"location": "body", "cols": col_index, "style": {"text-align": "right"}},
        {
            "location": "body",
            "rows": row_index,
            "style": {
                "background-color": "lightblue",
            },
        },
    ]

def flatten_columns(df):
    return [
        "_".join([str(c) for c in c_list if c not in ("", "std_amount_gbp")])
        for c_list in df.columns.values
    ]

def acctg_rows_to_highlight(df):
    ta_row = int(df.loc[df.BS_Flag == "Assets Total"].index[0])
    tl_row = int(df.loc[df.BS_Flag == "Liabilities & Equity Total"].index[0])

    return [ta_row, tl_row]
